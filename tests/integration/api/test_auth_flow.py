"""API integration tests for the register -> login -> bearer token flow.

NOTE: written against the assumed request/response shapes documented in
conftest.py. Adjust field names if your actual auth router differs.
"""
from tests.integration.api.conftest import login, register_user


class TestRegister:
    def test_register_returns_created_user_without_password(self, client):
        response = register_user(client)

        assert response.status_code in (200, 201)
        body = response.json()
        assert body["email"] == "alice@example.com"
        assert body["username"] == "alice"
        assert "password" not in body
        assert "_password_hash" not in body

    def test_register_duplicate_username_is_rejected(self, client):
        register_user(client, email="a1@example.com", username="alice")
        response = register_user(client, email="a2@example.com", username="alice")

        assert response.status_code in (400, 409)

    def test_register_duplicate_email_is_rejected(self, client):
        register_user(client, email="dup@example.com", username="user1")
        response = register_user(client, email="dup@example.com", username="user2")

        assert response.status_code in (400, 409)


class TestLogin:
    def test_login_with_valid_credentials_returns_token(self, client):
        register_user(client)
        response = login(client)

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body.get("token_type", "bearer").lower() == "bearer"

    def test_login_with_wrong_password_is_rejected(self, client):
        register_user(client)
        response = login(client, password="wrong-password")

        assert response.status_code == 401

    def test_login_with_unknown_username_is_rejected(self, client):
        response = login(client, username="ghost")

        assert response.status_code == 401


class TestProtectedRoutes:
    def test_request_without_token_is_rejected(self, client):
        response = client.get("/api/v1/accounts/me")
        assert response.status_code == 401

    def test_request_with_valid_token_is_accepted(self, client, auth_headers):
        response = client.get("/api/v1/accounts/me", headers=auth_headers)
        assert response.status_code == 200
