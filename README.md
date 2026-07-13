# 🚀 A1 Backend Core

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Architecture](https://img.shields.io/badge/architecture-layered-blue)
[![License](https://img.shields.io/badge/license-Anthropoi%20License%20v1.0-blue)](https://github.com/angellnx/A1-Backend-Core/blob/main/LICENSE)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![API](https://img.shields.io/badge/API-REST-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)


REST API for personal finance management — built with FastAPI, layered architecture, and rich domain models.

Designed with a social mission: making financial organization accessible to low and middle-income users who have historically been excluded from financial tools.

🔗 **Live API:** https://a1-backend-core.onrender.com/docs

---

## 🛠 Tech Stack

**Current:**
* Python 3.12
* FastAPI 0.115
* Pydantic 2.10
* Uvicorn 0.24
* SQLAlchemy 2.0
* SQLite
* JWT Authentication (python-jose)
* Bcrypt password hashing (passlib)
* Pytest (unit, repository and API integration tests)
* httpx2 (test client for API integration tests)

**Planned:**
* Docker
* PostgreSQL
* N8N

---

## ▶️ Running the Project

```bash
git clone https://github.com/angellnx/A1-Backend-Core
cd A1-Backend-Core
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn core_app.main:app --reload
```

Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
```

Access: http://127.0.0.1:8000/docs

All endpoints are versioned under `/api/v1`.

---

## 🏗 Architecture

```
Client
↓
Router Layer (FastAPI)
↓
Service Layer
↓
Domain Models
↓
Repository Layer (SQLAlchemy)
↓
Database (SQLite)
```

### Domain Models
Core business entities implemented as Python `@dataclass`. Business rules live inside the models — not scattered across services.

Key decision: **Rich Model over Anemic Model**. The `Transaction` model automatically normalizes its value on creation based on the transaction type's `is_positive` flag. The `User` model encapsulates password hashing internally. No external layer can create an inconsistent state.

Current entities:
* `User` — system user with encapsulated bcrypt password hashing
* `Transaction` — financial movement with automatic value normalization
* `TransactionType` — categorizes transactions via `is_positive` business rule
* `Account` — user financial account with dynamically calculated balance
* `Budget` — spending limit per category, currency, and month/year
* `Item` — line item associated with a transaction
* `Category` — groups items and budgets; uses name as primary key
* `Currency` — monetary unit following ISO 4217 standard

### Repository Layer
Handles data persistence through SQLAlchemy ORM-backed classes. Each repository converts between Domain Models (pure business objects) and ORM Models (SQLAlchemy mapped classes), keeping the domain layer completely free of infrastructure concerns. Queries are scoped per authenticated user where relevant (accounts, budgets, transactions), with support for filtering and pagination.

### Service Layer
Contains the core business logic. Receives repositories via **dependency injection** — never instantiates them directly. Responsible for validating inputs, resolving entity relationships, enforcing resource ownership, and coordinating persistence.

### Router Layer
Exposes REST API endpoints using FastAPI, versioned under `/api/v1`. Uses **Pydantic schemas** to validate incoming requests and control outgoing responses. Schemas are strictly separated from Domain Models — sensitive data like passwords are never exposed in responses.

---

## 🔐 Authentication & Authorization

The API uses **JWT (JSON Web Token)** authentication via Bearer tokens.

**Flow:**
1. Register a user via `POST /api/v1/auth/register`
2. Authenticate via `POST /api/v1/auth/login` to receive an access token
3. Include the token in the `Authorization: Bearer <token>` header on protected routes

All routes that handle user financial data are protected and require a valid token. Beyond authentication, the API enforces **resource ownership**: a user can only access, modify, or delete their own accounts, budgets, and transactions — even with a valid token, attempting to access another user's resource returns `403 Forbidden`.

User-scoped listing endpoints use the authenticated identity directly (`GET /accounts/me`, `GET /budgets/me`) rather than accepting a `user_id` in the URL, eliminating the possibility of ID-based access to other users' data.

---

## 🧠 Core Concept

The system is designed around **financial transactions**.

Each transaction is associated with a user, an account, an item, and a transaction type. The transaction type carries an `is_positive` flag that determines whether the value represents an income or an expense. The `user_id` is always inferred from the authenticated token, never accepted from the client.

Accounts aggregate transactions and expose a dynamic balance calculated from all linked movements. Budgets define spending limits per category, currency, and month/year — enforcing a composite uniqueness constraint that prevents duplicate budget definitions.

To simplify data entry, the API automatically normalizes transaction values. Users always provide **positive values**, and the system determines the correct sign internally.

**Request:**
```json
{
  "account_id": 1,
  "item_id": 1,
  "transaction_type_name": "Expense",
  "currency_code": "BRL",
  "value": 200
}
```

**Response:**
```json
{
  "id": 1,
  "value": -200,
  "transaction_type_name": "Expense",
  "user_id": 1,
  "account_id": 1,
  "item_id": 1,
  "currency_code": "BRL",
  "date": "2026-03-19T14:00:00",
  "notes": null
}
```

---

## 🔍 Filtering, Pagination & Error Handling

Listing endpoints support pagination via `skip` and `limit` query parameters (defaults: `skip=0`, `limit=20`).

The `GET /transactions/` endpoint additionally supports optional filters:
* `transaction_type_name` — filter by transaction type
* `currency_code` — filter by currency
* `date_from` / `date_to` — filter by date range (ISO 8601)

Results are always scoped to the authenticated user and ordered by most recent first.

**Global error handling:** unhandled database integrity violations (e.g. unique constraint conflicts) are caught by a global exception handler and converted into clean `409 Conflict` responses, instead of exposing raw stack traces to the client.

---

## 🧪 Testing

The project has a full test suite covering the Service, Repository, and API layers: unit tests with mocked repositories, repository integration tests against an in-memory SQLite database, and API integration tests covering authentication, resource ownership, pagination, filtering, and the global error handler.

Tests never touch the production database (`a1.db`) or real environment config — everything runs isolated.

```bash
pip install pytest fastapi[all] httpx2 --break-system-packages
pytest tests/ -v
```

See [tests/README.md](./tests/README.md) for full details on structure, coverage, and testing philosophy.

---

## 📂 Project Structure

```
A1-Backend-Core/
│
├── core_app/
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models/
│   ├── domain/
│   │   └── models/
│   ├── repositories/
│   ├── services/
│   ├── routers/
│   ├── schemas/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── services/
│   └── integration/
│       ├── repositories/
│       └── api/
│
├── .env.example
├── requirements.txt
└── README.md
```

* **domain/models** → business entities with encapsulated rules
* **database/** → SQLAlchemy setup, including session, base, and ORM models
* **repositories** → database-backed persistence with domain/ORM conversion, filtering, and pagination
* **services** → business logic with dependency injection and ownership enforcement
* **routers** → versioned REST endpoints with request/response schemas
* **schemas** → Pydantic contracts separating API layer from domain
* **core/security.py** → JWT token creation and validation
* **tests/** → unit, repository, and API integration tests (see [tests/README.md](./tests/README.md))

---

## 📡 API Endpoints

All endpoints are prefixed with `/api/v1`.

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate and receive JWT token |

### Users
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/users/` | Create a new user | ✅ |
| GET | `/users/` | List all users | ✅ |
| GET | `/users/{id}` | Get user by id (own data only) | ✅ |
| DELETE | `/users/{id}` | Delete user (own data only) | ✅ |

### Accounts
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/accounts/` | Create an account | ✅ |
| GET | `/accounts/me` | List authenticated user's accounts (paginated) | ✅ |
| GET | `/accounts/{id}` | Get account by id (own data only) | ✅ |
| DELETE | `/accounts/{id}` | Delete account (own data only) | ✅ |

### Transaction Types
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/transaction-types/` | Create a transaction type | ✅ |
| GET | `/transaction-types/` | List all transaction types | ✅ |
| GET | `/transaction-types/{name}` | Get transaction type by name | ✅ |
| DELETE | `/transaction-types/{name}` | Delete transaction type | ✅ |

### Categories
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/categories/` | Create a category | ✅ |
| GET | `/categories/` | List all categories | ✅ |
| GET | `/categories/{name}` | Get category by name | ✅ |
| DELETE | `/categories/{name}` | Delete category | ✅ |

### Items
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/items/` | Create an item | ✅ |
| GET | `/items/` | List all items | ✅ |
| GET | `/items/{id}` | Get item by id | ✅ |
| DELETE | `/items/{id}` | Delete item | ✅ |

### Currencies
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/currencies/` | Create a currency | ✅ |
| GET | `/currencies/` | List all currencies | ✅ |
| GET | `/currencies/{code}` | Get currency by code | ✅ |
| DELETE | `/currencies/{code}` | Delete currency | ✅ |

### Budgets
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/budgets/` | Create a budget | ✅ |
| GET | `/budgets/me` | List authenticated user's budgets (paginated) | ✅ |
| GET | `/budgets/{id}` | Get budget by id (own data only) | ✅ |
| DELETE | `/budgets/{id}` | Delete budget (own data only) | ✅ |

### Transactions
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/transactions/` | Create a transaction | ✅ |
| GET | `/transactions/` | List authenticated user's transactions (paginated, filterable) | ✅ |
| GET | `/transactions/{id}` | Get transaction by id | ✅ |
| DELETE | `/transactions/{id}` | Delete transaction | ✅ |

---

## 🗺 Roadmap

### ✅ Sprint 1 — Core Domain Architecture
* Rich Domain Models with encapsulated business rules
* In-memory Repository Layer implemented as classes
* Service Layer with dependency injection
* REST API Routers with Pydantic schemas
* Request/response contracts separating API layer from domain

### ✅ Sprint 2 — Persistence Layer
* Integrated SQLite with SQLAlchemy ORM and typed mappings
* Replaced in-memory repositories with database-backed persistence
* Replaced ItemType with Category entity across all layers
* Added Account entity with user-scoped queries
* Added Budget entity with composite uniqueness constraint
* Added Currency entity with ISO 4217 normalization
* Added structured docstrings across all layers
* Set up session management and FastAPI dependency injection

### ✅ Sprint 3 — API Improvements
* Pagination (`skip`/`limit`) on all listing endpoints
* Filtering on transactions (type, currency, date range)
* `/me` endpoints replacing `user_id`-in-URL patterns to prevent ID-based access
* Global exception handler for database integrity violations (409 Conflict)
* API versioning under `/api/v1`

### ✅ Sprint 4 — Authentication & Security
* JWT authentication via python-jose
* Login and registration endpoints
* Protected routes with Bearer token validation
* Bcrypt password hashing via passlib
* Resource ownership enforcement (403 on unauthorized access to another user's data)
* SECRET_KEY via environment variable

### ✅ Sprint 5 — Testing
* Unit tests for all 8 services (Account, Budget, Category, Currency, Item, Transaction, TransactionType, User) with mocked repositories
* Repository integration tests against an in-memory SQLite database, covering persistence, pagination, and the Budget composite uniqueness constraint
* API integration tests covering the auth flow, resource ownership (403 on cross-user access), pagination/filtering, and the global 409 error handler
* Migrated `core/config.py` from class-based `Config` to Pydantic v2's `SettingsConfigDict`
* Bug fixes uncovered while writing tests:
  * Fixed an indentation bug in `BudgetService.delete_budget` (method was defined outside the class, making it uncallable)
  * Fixed `TransactionResponse` missing `account_id` in create/list/get transaction endpoints (was incorrectly passing `user_id`, a field not present in the schema)

### 🔲 Sprint 6 — Privacy & Data Protection
* User data deletion mechanisms
* Privacy policy structure
* Data minimization review
* Security and data protection improvements

### 🔲 Sprint 7 — Production Readiness
* Environment configuration
* Logging improvements
* Performance optimization

---

## 💡 Why This Project Exists

In Brazil and across the world, millions of people struggle not only with limited income — but with the absence of tools that help them understand their own financial reality.

For low and middle-income individuals, financial stress is often invisible: small daily expenses that accumulate unnoticed, harmful spending habits that are never identified, and financial decisions made without clarity or support. The result is a cycle that is difficult to break — not because people lack effort or discipline, but because they lack access.

Accessible financial tools have historically been designed for those who already have financial stability. Everyone else is left behind.

This project was born from the belief that **technology can change that**.

A1 Backend Core is the technical foundation for a platform that aims to give people — regardless of their income level — the visibility, organization, and awareness they need to take control of their financial lives.

The goal is not just to build a good API. The goal is to build infrastructure that supports tools capable of making a real difference in people's lives.

---

## 🎯 The Impact We Want to Create

Financial organization should not be a privilege.

This platform is being built to support tools that help people:

* Understand where their money is going — clearly and without complexity
* Identify spending habits that damage their financial health
* Track income and expenses in a simple and accessible way
* Make more informed financial decisions over time
* Build healthier financial habits gradually and sustainably

The long-term vision is a platform that reaches people who have never had access to structured financial guidance — and gives them the same visibility and control that has always been available only to those who could afford it.

Every architectural decision in this project — from how transactions are structured to how data is protected — is made with this mission in mind.

---

## 🔒 Privacy & Data Protection

Because this platform handles **personal financial data**, privacy and data protection are core design considerations — not afterthoughts.

The project follows principles inspired by the Brazilian **Lei Geral de Proteção de Dados Pessoais (LGPD)** and modern security best practices.

### Data Minimization
The system collects and stores only the information strictly necessary for the platform to function.

### Security by Design
Security is incorporated into the architecture from the beginning:
* Bcrypt password hashing
* JWT-protected API routes
* Token-based authentication
* Resource ownership enforcement on every sensitive endpoint
* SECRET_KEY managed via environment variables
* Global error handling that avoids leaking internal stack traces

### User Data Control
Future versions will include mechanisms allowing users to manage and delete their personal data.

### Transparency
Users will have clear information about how their financial data is used within the platform.

---

## 🌍 Long-Term Vision

The long-term goal is to evolve this backend into a **complete personal finance platform focused on social impact** — making financial management tools genuinely accessible to people who have historically been excluded from them.

Future components include:

* A **web application** for visualizing and managing financial activity — designed for clarity and simplicity
* A **mobile application** for quick and practical expense tracking in everyday situations
* **Investment monitoring tools** for portfolio tracking over time
* **Data-driven financial insights** to help users understand their spending patterns and financial behavior
* Intelligent features powered by **data analysis and AI** to identify risky financial habits and support better decision-making

Future infrastructure includes PostgreSQL, Redis caching, Docker containerization, CI/CD pipeline, and background processing.

---

## 👨‍💻 Author

Developer focused on **Python, Backend Engineering and Data Systems**, currently building the technical foundation for financial management platforms and data-driven financial tools.

🔗 GitHub: https://github.com/angellnx
🔗 LinkedIn: https://www.linkedin.com/in/angellnx/

---

## 📜 License

This project is licensed under the [Anthropoi License v1.0](./LICENSE) — a **source-available** license.

You are free to use, modify, and redistribute this project for personal, non-commercial purposes, provided that:

* This is used by an Individual, not on behalf of or for the benefit of an Organization
* The original copyright notice and license text are preserved
* Any modified versions clearly state the changes made
* No AI Service is integrated into the Software or a Derivative Work — only Local Models are permitted

See the [LICENSE](./LICENSE) file for the full license text.
