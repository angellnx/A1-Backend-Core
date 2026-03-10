# 🚀 A1 Backend Core

![Python](https://img.shields.io/badge/python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-framework-green)
![Architecture](https://img.shields.io/badge/architecture-layered-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)
![API](https://img.shields.io/badge/API-REST-blue)

A1 Backend Core is the backend foundation for a **personal finance and investment management system** designed to help individuals better understand and control their financial activity.

The platform is being developed with a particular focus on **low and middle-income users**, who often lack access to accessible financial tools that help them organize their finances and identify harmful financial habits.

The goal of this project is to provide a structured API capable of supporting applications focused on **tracking income, expenses, investments, and financial behavior**, helping users improve their financial awareness and long-term financial well-being.

This repository focuses on building a **robust backend architecture** that can support such a system while remaining maintainable and scalable as new features are introduced.

---

# 💡 Why This Project Exists

Personal finance is an area where many people struggle to maintain clarity and organization.

For many individuals — especially in **low and middle-income contexts** — financial stress is often driven not only by limited income but also by the lack of accessible tools that help them understand their financial behavior.

This project was created to explore how a well-structured backend system can support tools that:

* help users organize their finances
* make financial information easier to understand
* identify harmful spending patterns
* encourage healthier financial habits over time

At the same time, the project serves as a technical foundation for experimenting with:

* financial data modeling
* backend architecture design
* scalable API development
* data-driven financial insights

The goal is to combine **solid backend engineering practices** with a broader mission of supporting tools that promote **financial awareness, autonomy, and better decision-making**.

---

# 🎯 Project Vision

Many people struggle to maintain a clear understanding of their finances.

The goal of this project is to support the development of tools that help users:

* Track income and expenses
* Monitor and organize investments
* Understand their financial behavior
* Identify harmful spending habits
* Organize transactions in a structured way
* Build healthier financial habits over time

By improving visibility into personal financial activity, the platform aims to help users gradually **improve their financial stability and quality of life**.

This backend API provides the **core infrastructure** for such a system.

---

# 🧠 Core Concept

The system is designed around **financial transactions**.

Each transaction represents a financial movement associated with a user and categorized by a transaction type.

Example:

* Income
* Expense

To simplify data entry for users, the API automatically normalizes transaction values.

Users always provide **positive values**, and the system determines the correct sign internally.

Example:

Input:

```

{
"amount": 200,
"transaction_type": "EXPENSE"
}

```

Stored internally:

```

-200

```

This ensures consistent financial data while keeping the interface simple for users.

As the system evolves, this transaction model will also support **investment-related financial operations**, maintaining consistency across financial records.

---

# 🔒 Privacy & Data Protection

Because this platform handles **personal financial data**, privacy and data protection are important design considerations.

The project is designed following principles inspired by the Brazilian **Lei Geral de Proteção de Dados Pessoais (LGPD)** and modern security best practices.

Key principles include:

### Data Minimization

The system should collect and store only the information strictly necessary for the platform to function.

### Security by Design

Security considerations are incorporated into the system architecture from the beginning, including:

* secure password hashing
* protected API routes
* authentication mechanisms
* controlled data access

### User Data Control

Future versions of the system are expected to include mechanisms allowing users to manage and delete their personal data.

### Transparency

Users should have clear information about how their financial data is used within the platform.

These principles help ensure the system evolves in a way that respects **privacy, security, and responsible data handling**.

---

# 🛠 Tech Stack

Current technologies used:

* Python 3
* FastAPI
* Pydantic
* Uvicorn

Planned technologies:

* SQLAlchemy
* SQLite / PostgreSQL
* JWT Authentication
* Pytest
* Docker

---

# 🏗 Architecture

The backend follows a layered architecture designed to separate responsibilities and keep business rules isolated from infrastructure concerns.

```

Client
↓
Router (FastAPI)
↓
Service Layer
↓
Repository Layer
↓
Domain Models

```

### Router

Handles HTTP requests and exposes API endpoints.

### Service Layer

Contains the **core business logic**, including financial rules and transaction processing.

### Repository Layer

Handles data persistence.

Currently implemented with **in-memory storage** during early development stages.

### Domain Models

Represent the core entities of the system:

* User
* Transaction
* TransactionType
* Item

These models form the basis for financial data management and will later support **investment tracking and portfolio-related features**.

---

# 📂 Project Structure

```

A1-Backend-Core/

├── core_app/
│
│   ├── domain/
│   │   └── models/
│   │
│   ├── repositories/
│   │
│   ├── services/
│   │
│   ├── routers/
│   │
│   └── main.py
│
├── docs/
│   ├── architecture.md
│   └── requirements.md
│
├── requirements.txt
└── README.md

```

* **domain** → business entities
* **repositories** → persistence logic
* **services** → business rules
* **routers** → API endpoints

---

# 📡 API Example

Example of creating a transaction.

### Request

```

POST /transactions

```
```

{
"amount": 200,
"transaction_type": "EXPENSE"
}

```

### Response

```

{
"id": 1,
"amount": -200,
"transaction_type": "EXPENSE"
}

```

This example demonstrates how the API automatically normalizes financial values while keeping the input simple for users.

---

# ▶️ Running the Project

Clone the repository:

```

git clone [https://github.com/angellnx/A1-Backend-Core](https://github.com/angellnx/A1-Backend-Core)

```

Navigate to the project directory:

```

cd A1-Backend-Core

```

Install dependencies:

```

pip install -r requirements.txt

```

Run the application:

```

uvicorn core_app.main:app --reload

```

Once the server is running, open the API documentation in your browser:

```

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

---

# 🗺 Roadmap

The project is being developed incrementally.

### Sprint 1 — Core Domain Architecture

* Define domain models
* Implement service layer
* Implement in-memory repositories
* Implement API routers
* Document architecture

### Sprint 2 — Persistence Layer

* Integrate SQLite
* Introduce SQLAlchemy ORM
* Replace in-memory repositories

### Sprint 3 — API Improvements

* Improve API schemas
* Pagination and filtering
* Better error handling

### Sprint 4 — Authentication & Security

* JWT authentication
* Login and registration
* Protected routes
* Password hashing improvements

### Sprint 5 — Testing

* Unit tests for services
* Repository tests
* API integration tests

### Sprint 6 — Privacy & Data Protection

* User data deletion mechanisms
* Privacy policy structure
* Data minimization review
* Security and data protection improvements

### Sprint 7 — Production Readiness

* Environment configuration
* Logging improvements
* Performance optimization

---

# 🔮 Future Improvements

Potential future features:

* PostgreSQL support
* Redis caching
* Docker containerization
* CI/CD pipeline
* Background processing
* Financial analytics features
* Investment tracking and portfolio management

---

# 🌍 Long-Term Vision

The long-term goal of this project is to support a complete personal finance platform that helps individuals better understand and manage their financial lives.

A key objective is to make financial management tools **more accessible and understandable**, particularly for people who traditionally have limited access to structured financial planning resources.

While this repository focuses on the backend API, the broader vision includes expanding the ecosystem around it.

Possible future components include:

* A **web application** that allows users to visualize and manage their financial activity.
* A **mobile application** designed for quick and practical expense tracking in everyday situations.
* **Investment monitoring tools**, allowing users to follow their portfolio evolution over time.
* **Data-driven financial insights**, helping users understand spending patterns and financial habits.
* Intelligent features powered by **data analysis and AI** to help identify risky financial behaviors and support better decision-making.

The long-term objective is to gradually evolve the system into a platform capable of supporting tools that promote **financial organization, transparency, and improved quality of life**.

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve the project, feel free to:

* open an issue
* suggest improvements
* submit a pull request

---

# 👨‍💻 Author

Developer focused on **Python, Backend Engineering and Data Systems**, currently building the technical foundation for financial management platforms and data-driven financial tools.

🔗 GitHub  
https://github.com/angellnx

🔗 LinkedIn  
https://www.linkedin.com/in/angellnx/

---

# 📜 License

This project is licensed under the MIT License.