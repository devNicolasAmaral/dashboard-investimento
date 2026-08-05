# Dashboard de Investimentos

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?style=flat-square&logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)

Sistema web para gerenciamento de ativos financeiros, desenvolvido para controlar investimentos, acompanhar patrimônio e servir como base para análises financeiras.

---

## Funcionalidades

- Cadastro e gerenciamento de ativos financeiros
- API REST para operações da aplicação
- Persistência relacional utilizando PostgreSQL
- Backend assíncrono com FastAPI
- Interface web desenvolvida com NiceGUI
- Ambiente containerizado com Docker

---

## Stack

| Camada | Tecnologia |
| :--- | :--- |
| Backend | FastAPI |
| Interface | NiceGUI |
| Banco de Dados | PostgreSQL |
| Infraestrutura | Docker Compose |

---

## Executando o projeto

### Opção 1 — Docker (recomendado)

Clone o repositório:

```bash
git clone https://github.com/devNicolasAmaral/dashboard-investimento.git

cd dashboard-investimento
```

Crie o arquivo `.env` utilizando o `.env.example` como base.

Inicie os containers:

```bash
docker compose up --build
```

A aplicação estará disponível em:

Aplicação

```
http://localhost:8080
```

Documentação da API

```
http://localhost:8000/docs
```

---

### Opção 2 — Ambiente local

Clone o repositório:

```bash
git clone https://github.com/devNicolasAmaral/dashboard-investimento.git

cd dashboard-investimento
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` utilizando o `.env.example` como base.

Certifique-se de possuir uma instância do PostgreSQL em execução e atualize a variável `DATABASE_URL` conforme sua configuração.

Inicie a aplicação:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em:

Aplicação

```
http://localhost:8080
```

Documentação da API

```
http://localhost:8000/docs
```

---

## Variáveis de ambiente

Exemplo do arquivo `.env`:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=investments_db

DATABASE_URL=postgresql+asyncpg://admin:secret@db:5432/investments_db
```

---

## Próximas funcionalidades

- Implementação de cache com Redis
- Testes automatizados
- Dashboard analítico
