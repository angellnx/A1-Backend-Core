# System Architecture

This document describes the architectural structure of the **A1 Backend Core**.

The project follows a **layered architecture** designed to separate responsibilities and keep business logic independent from infrastructure concerns.

The goal of this architecture is to ensure:

- maintainability
- scalability
- testability
- clear separation of responsibilities

---

# Architectural Overview

The backend is structured in layers:

Client  
↓  
Router Layer  
↓  
Service Layer  
↓  
Repository Layer  
↓  
Domain Models  

Each layer has a specific responsibility.

---

# Technology Stack

The project uses the following technologies:

## Core Framework
- **FastAPI**: Modern Python web framework for building APIs
- **Uvicorn**: ASGI server for running the application

## Data Validation and Configuration
- **Pydantic**: Data validation using Python type hints
- **Pydantic Settings**: Configuration management with environment variables
- **python-dotenv**: Environment variable loading from .env files

## Database and ORM
- **SQLAlchemy**: SQL toolkit (prepared for future database integration)
- Current implementation: In-memory repositories
- Future support: SQLite, PostgreSQL

## Testing
- **pytest**: Testing framework

---

# Router Layer

The **router layer** handles HTTP requests and exposes the API endpoints.

This layer is implemented using **FastAPI** and is responsible for:

- receiving HTTP requests
- validating input data
- returning HTTP responses
- calling the appropriate service

Routers should remain thin and avoid implementing business logic.

Example endpoint:

```
POST /transactions
```

Routers delegate processing to the service layer.

---

# Service Layer

The **service layer** contains the core business logic of the system.

This layer is responsible for:

- applying business rules
- coordinating repositories
- validating domain logic
- processing financial operations

Example responsibilities include:

- transaction normalization
- validation of financial operations
- coordination of persistence operations

Keeping business logic inside services helps maintain a clean separation between API logic and domain rules.

---

# Repository Layer

The **repository layer** is responsible for data persistence.

Repositories provide an abstraction between the business logic and the data storage mechanism.

Current implementation:

- In-memory repositories for early development

Planned future implementations:

- SQLite
- PostgreSQL
- SQLAlchemy ORM

Using repositories allows the persistence strategy to evolve without affecting business logic.

---

# Domain Models

Domain models represent the core business entities of the system.

The system includes the following core entities:

- **User**: Represents system users managing their financial operations
- **Transaction**: Records financial movements (income, expense, transfer)
- **TransactionType**: Categorizes transactions (e.g., income, expense, investment)
- **Item**: Represents physical or digital assets/products
- **ItemType**: Categorizes items into types

These models are implemented using **Pydantic** for validation and serialization. They define the structure of financial data and form the foundation of the system.

Validation rules are applied at the model level to ensure data integrity.

The domain layer should remain independent from infrastructure concerns.

---

# Design Principles

The architecture follows several software engineering principles.

### Separation of Concerns

Each layer has a clear responsibility.

### Maintainability

The structure makes it easier to modify or extend specific parts of the system.

### Testability

Business logic in the service layer can be tested independently.

### Scalability

The architecture allows the system to evolve with additional features such as:

- investment tracking
- financial analytics
- machine learning components

---

# Future Architectural Evolution

As the project evolves, additional architectural components may be introduced.

Possible future improvements include:

- database migrations
- caching layers
- background job processing
- event-driven components
- analytics pipelines

These changes can be integrated while preserving the current layered structure.

---

# Project Structure

```
core_app/
├── main.py                    # Application entry point
├── core/
│   ├── config.py             # Settings and configuration
│   └── __init__.py
├── domain/
│   └── models/               # Domain entities
│       ├── user.py
│       ├── transaction.py
│       ├── transaction_type.py
│       ├── item.py
│       └── type_item.py
├── repositories/             # Data access layer
│   ├── user_repository.py
│   ├── transaction_repository.py
│   ├── transaction_type_repository.py
│   ├── item_repository.py
│   └── item_type_repository.py
├── services/                 # Business logic layer
│   ├── user_service.py
│   ├── transaction_service.py
│   ├── transaction_type_service.py
│   ├── item_service.py
│   ├── item_type_service.py
│   └── __init__.py
├── routers/                  # HTTP endpoint layer
│   ├── user_router.py
│   ├── transaction_router.py
│   └── transaction_type_router.py
└── docs/
    └── architecture.md       # This file
```

---

# Getting Started

## Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

## Running the Application

```bash
# Using run.sh script
./run.sh

# Or manually
uvicorn core_app.main:app --reload
```

## Accessing API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

