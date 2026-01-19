# Investment Dashboard

> **Sistema de gestão e análise de portfólio financeiro focado em performance e integridade de dados.**

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?style=flat-square&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)

---

## 🎯 Objetivo Técnico
Este projeto vai além de um simples CRUD financeiro. O objetivo é implementar uma arquitetura capaz de processar dados de mercado e renderizar análises em tempo real sem bloquear a thread principal.

A escolha de **NiceGUI** (ao invés de frameworks JS tradicionais) permite manter a lógica de negócio e a interface unificadas em Python, reduzindo a complexidade da stack e facilitando a manutenção, enquanto o **FastAPI** garante que o backend suporte alta concorrência.

---

## 🛠️ Stack & Decisões Arquiteturais

| Componente | Tecnologia | Por que foi escolhido? |
| :--- | :--- | :--- |
| **Backend** | `FastAPI` | Suporte nativo a `async/await` para I/O não-bloqueante e validação automática com Pydantic. |
| **Frontend** | `NiceGUI` | Renderização server-side leve, eliminando a necessidade de uma stack Node.js separada. |
| **Database** | `PostgreSQL` | Robustez para transações financeiras e integridade referencial complexa. |
| **Infra** | `Docker Compose` | Orquestração dos serviços (App + DB) para garantir ambiente idêntico em Dev e Prod. |

---

## ⚡ Quickstart (Rodando com Docker)

Você não precisa configurar ambiente Python localmente. Se tiver o Docker instalado:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/devNicolasAmaral/dashboard-investimento.git](https://github.com/devNicolasAmaral/dashboard-investimento.git)
   cd dashboard-investimento
   ```

2. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```

3. **Acesse:**
   * **Aplicação:** `http://localhost:8080` (Ou a porta definida no seu docker-compose)
   * **API Docs:** `http://localhost:8000/docs`

---

## 🔧 Variáveis de Ambiente (.env)

O sistema espera um arquivo `.env` na raiz para configurar o banco de dados. Um exemplo (`.env.example`) está incluído:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=investments_db
DATABASE_URL=postgresql+asyncpg://admin:secret@db:5432/investments_db
```

---

## 🧩 Funcionalidades Chave (Backend)

* **Ingestão de Dados:** Endpoints assíncronos para cadastro e atualização de ativos.
* **Cálculo de Rentabilidade:** Lógica segregada em Services para processar dividendos e valorização.
* **Validação Estrita:** Uso de Pydantic V2 para garantir que nenhum dado sujo entre no banco.

---

## 🚀 Roadmap

* [ ] Implementar sistema de cache (Redis) para cotações em tempo real.
* [ ] Adicionar testes de integração (Pytest) no pipeline de CI.
* [ ] Refinar dashboard analítico com gráficos comparativos (Benchmarking).

---

<div align="center">
  <sub>Desenvolvido por <a href="https://github.com/devNicolasAmaral">Nicolas Amaral</a></sub>
</div>
