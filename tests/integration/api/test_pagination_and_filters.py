"""API integration tests for pagination and transaction filtering.

Assumes the request/response schema for transactions matches the example
in the README (account_id, item_id, transaction_type_name, currency_code,
value). Adjust field names if your schemas differ.
"""
import pytest


@pytest.fixture()
def setup_reference_data(client, auth_headers):
    """Create the category/item/currency/transaction-type/account a transaction needs."""
    client.post("/api/v1/categories/", json={"name": "Food", "color": "#FF5733"}, headers=auth_headers)
    item_resp = client.post(
        "/api/v1/items/", json={"name": "Apple", "category_name": "Food"}, headers=auth_headers
    )
    client.post(
        "/api/v1/currencies/", json={"code": "BRL", "name": "Real", "symbol": "R$"}, headers=auth_headers
    )
    client.post(
        "/api/v1/transaction-types/",
        json={"name": "Expense", "is_positive": False},
        headers=auth_headers,
    )
    account_resp = client.post(
        "/api/v1/accounts/", json={"name": "Nubank", "account_type": "Checking"}, headers=auth_headers
    )
    return {
        "item_id": item_resp.json()["id"],
        "account_id": account_resp.json()["id"],
    }


def create_transaction(client, headers, ref, value=100, currency_code="BRL", ttype="Expense"):
    return client.post(
        "/api/v1/transactions/",
        json={
            "account_id": ref["account_id"],
            "item_id": ref["item_id"],
            "transaction_type_name": ttype,
            "currency_code": currency_code,
            "value": value,
        },
        headers=headers,
    )


class TestPagination:
    def test_default_limit_is_20(self, client, auth_headers, setup_reference_data):
        for i in range(25):
            create_transaction(client, auth_headers, setup_reference_data, value=i + 1)

        response = client.get("/api/v1/transactions/", headers=auth_headers)

        assert response.status_code == 200
        assert len(response.json()) == 20

    def test_skip_and_limit_are_respected(self, client, auth_headers, setup_reference_data):
        for i in range(5):
            create_transaction(client, auth_headers, setup_reference_data, value=i + 1)

        response = client.get(
            "/api/v1/transactions/?skip=2&limit=2", headers=auth_headers
        )

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestFiltering:
    def test_filter_by_currency_code(self, client, auth_headers, setup_reference_data):
        client.post(
            "/api/v1/currencies/",
            json={"code": "USD", "name": "US Dollar", "symbol": "$"},
            headers=auth_headers,
        )
        create_transaction(client, auth_headers, setup_reference_data, currency_code="BRL")
        create_transaction(client, auth_headers, setup_reference_data, currency_code="USD")

        response = client.get(
            "/api/v1/transactions/?currency_code=USD", headers=auth_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert all(t["currency_code"] == "USD" for t in results)

    def test_filter_by_transaction_type(self, client, auth_headers, setup_reference_data):
        client.post(
            "/api/v1/transaction-types/",
            json={"name": "Salary", "is_positive": True},
            headers=auth_headers,
        )
        create_transaction(client, auth_headers, setup_reference_data, ttype="Expense")
        create_transaction(client, auth_headers, setup_reference_data, ttype="Salary")

        response = client.get(
            "/api/v1/transactions/?transaction_type_name=Salary", headers=auth_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert all(t["transaction_type_name"] == "Salary" for t in results)
