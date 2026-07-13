"""API integration tests for resource-ownership enforcement (403 Forbidden).

Assumes JSON bodies for account/budget creation match the domain model
fields described in the README. Adjust field names if your schemas differ.
"""
from tests.integration.api.conftest import login, register_user


def second_user_headers(client):
    register_user(client, email="bob@example.com", username="bob", password="secret123")
    response = login(client, username="bob", password="secret123")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestAccountOwnership:
    def test_cannot_access_another_users_account(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/accounts/",
            json={"name": "Nubank", "account_type": "Checking"},
            headers=auth_headers,
        )
        assert create_resp.status_code in (200, 201), create_resp.text
        account_id = create_resp.json()["id"]

        other_headers = second_user_headers(client)
        get_resp = client.get(f"/api/v1/accounts/{account_id}", headers=other_headers)

        assert get_resp.status_code == 403

    def test_cannot_delete_another_users_account(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/accounts/",
            json={"name": "Nubank", "account_type": "Checking"},
            headers=auth_headers,
        )
        account_id = create_resp.json()["id"]

        other_headers = second_user_headers(client)
        delete_resp = client.delete(f"/api/v1/accounts/{account_id}", headers=other_headers)

        assert delete_resp.status_code == 403

    def test_owner_can_access_own_account(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/accounts/",
            json={"name": "Nubank", "account_type": "Checking"},
            headers=auth_headers,
        )
        account_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/v1/accounts/{account_id}", headers=auth_headers)

        assert get_resp.status_code == 200
