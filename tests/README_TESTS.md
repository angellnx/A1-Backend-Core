# 🧪 Test Suite

Comprehensive test suite for A1 Backend Core, covering the Service, Repository, and API layers.

The suite validates business rules, persistence, authentication, authorization, filtering, pagination, and error handling — while ensuring the production database is never touched.

---

## ▶️ Running the Tests

Install the required dependencies:

```bash
pip install pytest fastapi[all] httpx2 --break-system-packages
```

Run the full test suite:

```bash
pytest tests/ -v
```

---

## 🔒 Test Isolation

The suite is split into unit and integration tests.

**Unit tests**
Located under `tests/unit/`. Validate business logic in complete isolation — repositories are fully mocked, so no database or external I/O is performed.

**Integration tests**
Located under `tests/integration/repositories/` and `tests/integration/api/`. Use an in-memory SQLite database provided by the `engine` and `db_session` fixtures defined in `tests/conftest.py`.

As a result:
* The production database (`a1.db`) is never modified or accessed
* Every test starts from a clean database state

---

## 📂 Test Structure

```text
tests/
├── conftest.py
│
├── unit/
│   └── services/
│       ├── test_account_service.py
│       ├── test_budget_service.py
│       ├── test_category_service.py
│       ├── test_currency_service.py
│       ├── test_item_service.py
│       ├── test_transaction_type_service.py
│       └── test_transaction_service_listing.py
│
└── integration/
    ├── repositories/
    │   ├── test_user_repository.py
    │   ├── test_account_repository.py
    │   ├── test_category_repository.py
    │   ├── test_currency_repository.py
    │   ├── test_item_repository.py
    │   ├── test_transaction_type_repository.py
    │   ├── test_budget_repository.py
    │   └── test_transaction_repository.py
    │
    └── api/
        ├── conftest.py
        ├── test_auth_flow.py
        ├── test_ownership.py
        ├── test_pagination_and_filters.py
        └── test_error_handling.py
```

---

## ✅ Coverage

The test suite covers:

* Service layer business logic
* Repository persistence using SQLAlchemy
* Domain-to-database mappings
* JWT authentication flow
* Resource ownership enforcement
* Pagination and filtering
* Database constraints
* Error handling and authorization rules

---

## ⚠️ API Test Notes

The API tests were written based on the project's architecture and available source code at the time. During development, the following layers were available:

* Domain Models
* Services
* Repositories
* Database
* Dependencies
* Security
* Application entry point

The Router and Schema layers were not available at the time, so some request and response contracts were inferred from the existing implementation. Current assumptions include:

* `POST /auth/register` accepts the fields required by `UserService.create_user`
* `POST /auth/login` uses `OAuth2PasswordRequestForm`
* Request payloads follow the project's Domain Models

If the Router and Schema contracts change, these tests should be revisited to match the exact endpoint contracts — the testing infrastructure itself won't need to change.

---

## 💡 Testing Philosophy

The test suite follows the same layered architecture as the application:

* **Unit tests** verify business rules in complete isolation
* **Repository integration tests** validate persistence using a real in-memory SQLAlchemy database
* **API integration tests** validate the complete request lifecycle, including authentication, authorization, dependency injection, and persistence

Together, these layers provide confidence that the application behaves correctly from the Domain Layer to the REST API.
