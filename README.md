# A1-BACKEND-CORE

API backend para **gestão financeira pessoal**, desenvolvida em **Python**, com foco em **boas práticas de arquitetura**, **organização de código** e **regras de negócio bem definidas**.

🚧 **Status do projeto:** Em desenvolvimento — *Sprint 1*

---

## 📌 Objetivo do Projeto

Criar uma API robusta para controle financeiro pessoal, permitindo:

- Cadastro de usuários
- Organização de itens financeiros
- Tipos de movimentações financeiras (**entrada** e **saída**)
- Registro de movimentações com regras de negócio claras
- Base sólida para futura aplicação mobile

Este projeto foi pensado desde o início como um **projeto de portfólio profissional**, priorizando:
- Clareza de código
- Separação de responsabilidades
- Escalabilidade
- Padrões utilizados no mercado

---

## 🧠 Arquitetura e Conceitos Utilizados

O projeto segue uma **arquitetura em camadas**, inspirada em práticas como:

- **Service Layer**
- **Repository Pattern**
- Princípios de **Clean Architecture**

### Camadas principais

#### 🧩 Entities
Representam o **domínio da aplicação** e suas regras centrais.  
Não dependem de frameworks ou banco de dados.

#### 🗄 Repositories
Responsáveis pelo **acesso e persistência de dados**.  
Atualmente abstraídos, com implementação de banco planejada.

#### ⚙️ Services
Contêm as **regras de negócio**, validações e fluxos da aplicação.  
São o coração da lógica do sistema.

Essa separação facilita:
- Testes unitários
- Manutenção
- Evolução do projeto
- Migração de banco de dados

---

## 🗂 Estrutura do Projeto

```text```
core_app/
 ├── entities/        # Entidades do domínio
 ├── repositories/    # Camada de acesso a dados
 ├── services/        # Regras de negócio
 ├── routers/         # Endpoints da API (FastAPI)
 ├── config/          # Configurações da aplicação
 └── main.py          # Inicialização da aplicação

## 🛠 Tecnologias Utilizadas

- Python 3.11+
- FastAPI — framework para construção da API
- Pydantic — validação e tipagem de dados
- Uvicorn — servidor ASGI
- SQLite — banco de dados inicial (ambiente local / desenvolvimento)
- SQLAlchemy (planejado) — ORM para persistência de dados
- Alembic (planejado) — versionamento de banco de dados
- PostgreSQL (planejado) — banco de dados para produção
- Git & GitHub — versionamento de código

## 🗺 Roadmap do Projeto

O desenvolvimento está organizado em sprints, seguindo uma evolução incremental e realista.

## ✅ Sprint 1 — Base do Domínio (Atual)

 Estrutura base do projeto

 Arquitetura em camadas (entities, repositories, services)

 Definição das entidades de domínio

 Implementação das regras de negócio nos services

 Tipos de movimentação (entrada e saída)

 Projeto pronto para integração com banco de dados