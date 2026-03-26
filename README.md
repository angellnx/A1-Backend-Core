# 🚀 A1 Backend Core

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Architecture](https://img.shields.io/badge/architecture-layered-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)
![API](https://img.shields.io/badge/API-REST-blue)

A1 Backend Core is the backend foundation for a **personal finance and investment management system** designed to help individuals better understand and control their financial activity.

The platform is being developed with a particular focus on **low and middle-income users**, who often lack access to accessible financial tools that help them organize their finances and identify harmful financial habits.

---

# 💡 Why This Project Exists

In Brazil and across the world, millions of people struggle not only with limited income — but with the absence of tools that help them understand their own financial reality.

For low and middle-income individuals, financial stress is often invisible: small daily expenses that accumulate unnoticed, harmful spending habits that are never identified, and financial decisions made without clarity or support. The result is a cycle that is difficult to break — not because people lack effort or discipline, but because they lack access.

Accessible financial tools have historically been designed for those who already have financial stability. Everyone else is left behind.

This project was born from the belief that **technology can change that**.

A1 Backend Core is the technical foundation for a platform that aims to give people — regardless of their income level — the visibility, organization, and awareness they need to take control of their financial lives.

The goal is not just to build a good API. The goal is to build infrastructure that supports tools capable of making a real difference in people's lives.

---

# 🎯 The Impact We Want to Create

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

# 🧠 Core Concept

The system is designed around **financial transactions**.

Each transaction is associated with a user, an item, and a transaction type. The transaction type carries an `is_positive` flag that determines whether the value represents an income or an expense.

To simplify data entry, the API automatically normalizes transaction values. Users always provide **positive values**, and the system determines the correct sign internally.

**Request:**
```json
{
  "user_id": 1,
  "item_id": 1,
  "transaction_type_name": "Expense",
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
  "item_id": 1,
  "date": "2026-03-19T14:00:00",
  "notes": null
}
```

The sign is determined by the transaction type — not by the user. This ensures consistent financial data while keeping the interface simple.

---

# 🔒 Privacy & Data Protection

Because this platform handles **personal financial data**, privacy and data protection are core design considerations — not afterthoughts.

The project follows principles inspired by the Brazilian **Lei Geral de Proteção de Dados Pessoais (LGPD)** and modern security best practices.

### Data Minimization
The system collects and stores only the information strictly necessary for the platform to function.

### Security by Design
Security is incorporated into the architecture from the beginning:
* Secure password hashing
* Protected API routes
* Authentication mechanisms
* Controlled data access

### User Data Control
Future versions will include mechanisms allowing users to manage and delete their personal data.

### Transparency
Users will have clear information about how their financial data is used within the platform.

---

# 🛠 Tech Stack

**Current:**
* Python 3.12
* FastAPI 0.104.1
* Pydantic 2.5.0
* Uvicorn 0.24.0
* SQLAlchemy 2.0.23
* SQLite

**Planned:**
* JWT Authentication
* Pytest
* Docker
* PostgreSQL (planned for production deployment)
* N8N 

---

# 🏗 Architecture

The backend follows a **layered architecture** designed to separate responsibilities and keep business rules isolated from infrastructure concerns.

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
### Notes on Persistence
* **Repository Layer** — repository Layer now uses SQLAlchemy for persistence, replacing the in-memory storage. Migration was seamless, preserving business rules and domain integrity..
* **database/** — contains SQLAlchemy setup, including `Base`, `Session`, and table models. Provides the infrastructure for persistent storage without affecting domain logic.

### Domain Models
Core business entities implemented as Python `@dataclass`. Business rules live inside the models — not scattered across services.

Key decision: **Rich Model over Anemic Model**. The `Transaction` model automatically normalizes its value on creation based on the transaction type's `is_positive` flag. The `User` model encapsulates password hashing internally. No external layer can create an inconsistent state.

Current entities:
* `User` — system user with encapsulated password hashing
* `Transaction` — financial movement with automatic value normalization
* `TransactionType` — categorizes transactions via `is_positive` business rule
* `Item` — asset or product associated with a transaction
* `ItemType` — categorizes items by type
* `Currency` — represents monetary units using ISO 4217 standard

### Repository Layer
Handles data persistence through classes that abstract the storage mechanism. Currently implemented with **in-memory storage**. Designed as classes to allow seamless migration to SQLAlchemy in Sprint 2 without changing any other layer.

### Service Layer
Contains the core business logic. Receives repositories via **dependency injection** — never instantiates them directly. Responsible for validating inputs, resolving entity relationships, and coordinating persistence.

### Router Layer
Exposes REST API endpoints using FastAPI. Uses **Pydantic schemas** to validate incoming requests and control outgoing responses. Schemas are strictly separated from Domain Models — sensitive data like passwords are never exposed in responses.

---

# 📂 Project Structure

```
A1-Backend-Core/
│
├── core_app/
│   ├── database/                  
│   │   ├── base.py                
│   │   ├── session.py             
│   │   └── models/                
│   │
│   ├── domain/
│   │   └── models/
│   │       ├── user.py
│   │       ├── transaction.py
│   │       ├── transaction_type.py
│   │       ├── item.py
│   │       └── item_type.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── transaction_repository.py
│   │   ├── transaction_type_repository.py
│   │   ├── item_repository.py
│   │   └── item_type_repository.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── transaction_service.py
│   │   ├── transaction_type_service.py
│   │   ├── item_service.py
│   │   └── item_type_service.py
│   │
│   ├── routers/
│   │   ├── user_router.py
│   │   ├── transaction_router.py
│   │   ├── transaction_type_router.py
│   │   ├── item_router.py
│   │   └── item_type_router.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── transaction_schema.py
│   │   ├── transaction_type_schema.py
│   │   ├── item_schema.py
│   │   └── item_type_schema.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── dependencies.py
│   └── main.py
│
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

* **domain/models** → business entities with encapsulated rules
* **repositories** → in-memory persistence, ready for database migration
* **database/** → SQLAlchemy setup, including session, base, and table models
* **services** → business logic with dependency injection
* **routers** → REST endpoints with request/response schemas
* **schemas** → Pydantic contracts separating API layer from domain

---

# 📡 API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user by id |
| DELETE | `/users/{id}` | Delete user |

### Transaction Types
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transaction-types/` | Create a transaction type |
| GET | `/transaction-types/` | List all transaction types |
| GET | `/transaction-types/{name}` | Get transaction type by name |
| DELETE | `/transaction-types/{name}` | Delete transaction type |

### Item Types
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/item-types/` | Create an item type |
| GET | `/item-types/` | List all item types |
| GET | `/item-types/{name}` | Get item type by name |
| DELETE | `/item-types/{name}` | Delete item type |

### Items
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items/` | Create an item |
| GET | `/items/` | List all items |
| GET | `/items/{id}` | Get item by id |
| DELETE | `/items/{id}` | Delete item |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/` | Create a transaction |
| GET | `/transactions/` | List all transactions |
| GET | `/transactions/{id}` | Get transaction by id |
| DELETE | `/transactions/{id}` | Delete transaction |

### Currencies
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/currencies/` | Create a currency |
| GET | `/currencies/` | List all currencies |
| GET | `/currencies/{code}` | Get currency by code |
| DELETE | `/currencies/{code}` | Delete currency |

---

# ▶️ Running the Project

Clone the repository:
```bash
git clone https://github.com/angellnx/A1-Backend-Core
```

Navigate to the project directory:
```bash
cd A1-Backend-Core
```

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
uvicorn core_app.main:app --reload
```

Access the interactive API documentation:
```
http://127.0.0.1:8000/docs
```

---

# 🗺 Roadmap

### ✅ Sprint 1 — Core Domain Architecture
* Rich Domain Models with encapsulated business rules
* In-memory Repository Layer implemented as classes
* Service Layer with dependency injection
* REST API Routers with Pydantic schemas
* Request/response contracts separating API from domain

### ✅ Sprint 2 — Persistence Layer
* Integrate SQLite
* Introduce SQLAlchemy ORM
* Replace in-memory repositories

### 🔲 Sprint 3 — API Improvements
* Pagination and filtering
* Better error handling
* API versioning

### 🔲 Sprint 4 — Authentication & Security
* JWT authentication
* Login and registration
* Protected routes
* Password hashing improvements (bcrypt/argon2)

### 🔲 Sprint 5 — Testing
* Unit tests for services
* Repository tests
* API integration tests

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

# 🌍 Long-Term Vision

The long-term goal is to evolve this backend into a **complete personal finance platform focused on social impact** — making financial management tools genuinely accessible to people who have historically been excluded from them.

This means not just building features, but building them in a way that is simple enough for anyone to use, secure enough to be trusted with sensitive financial data, and robust enough to scale to the people who need it most.

Future components include:

* A **web application** for visualizing and managing financial activity — designed for clarity and simplicity
* A **mobile application** for quick and practical expense tracking in everyday situations
* **Investment monitoring tools** for portfolio tracking over time
* **Data-driven financial insights** to help users understand their spending patterns and financial behavior
* Intelligent features powered by **data analysis and AI** to identify risky financial habits and support better decision-making

Future infrastructure includes PostgreSQL, Redis caching, Docker containerization, CI/CD pipeline, and background processing — all in service of a platform that can reach and support the people who need it most.

---

# 👨‍💻 Author

Developer focused on **Python, Backend Engineering and Data Systems**, currently building the technical foundation for financial management platforms and data-driven financial tools.

🔗 GitHub: https://github.com/angellnx
🔗 LinkedIn: https://www.linkedin.com/in/angellnx/

---

# 📜 License

This project is licensed under the **Apache License 2.0**.

You are free to use, modify, and distribute this project, provided that:

* The original copyright notice and attribution to the author are preserved
* Any modified versions clearly state the changes made
* The license text is included in any redistribution

This means that if you use this code in your own project, you must give appropriate credit to the original author in your code or documentation.

See the [LICENSE](./LICENSE) file for the full license text.
