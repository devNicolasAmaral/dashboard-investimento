# Dashboard de Investimentos

Sistema web para gerenciamento de ativos financeiros, desenvolvido para controlar investimentos, acompanhar patrimônio e servir como base para análises financeiras.

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?style=flat-square&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)

---

## Funcionalidades

- Cadastro e gerenciamento de ativos financeiros
- API REST para operações da aplicação
- Persistência relacional utilizando PostgreSQL
- Backend assíncrono com FastAPI
- Interface web desenvolvida com NiceGUI
- Ambiente totalmente containerizado com Docker

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

### Clonar o repositório

```bash
git clone https://github.com/devNicolasAmaral/dashboard-investimento.git
cd dashboard-investimento
```

### Executar

```bash
docker compose up --build
```

### Acessar

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

O projeto utiliza um arquivo `.env`.

Exemplo:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=investments_db

DATABASE_URL=postgresql+asyncpg://admin:secret@db:5432/investments_db
```

---

## Próximas funcionalidades

- Cache com Redis
- Testes automatizados
- Dashboard analítico
