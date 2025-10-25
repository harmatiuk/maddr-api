# maddr-api

API para gerenciamento de contas de usuário, construída com FastAPI, SQLAlchemy, Alembic e autenticação JWT.

## Estrutura do Projeto

```
maddr-api/
├── src/
│   └── maddr_api/
│       ├── app.py                # Ponto de entrada FastAPI
│       ├── config/
│       │   ├── database.py       # Configuração do banco de dados (SQLAlchemy)
│       │   └── settings.py       # Configurações do projeto (env)
│       ├── models/
│       │   └── account.py        # Modelo Account (ORM)
│       ├── routers/
│       │   ├── account.py        # Rotas de conta (CRUD)
│       │   └── token.py          # Rotas de autenticação/token
│       ├── schemas/
│       │   ├── account.py        # Schemas Pydantic para Account
│       │   └── token.py          # Schemas Pydantic para Token
│       └── services/
│           ├── account.py        # Lógica de negócio para contas
│           ├── token.py          # Lógica de negócio para tokens
│           └── main.py           # Utilitários e enums
├── migrations/                   # Migrações Alembic
├── tests/                        # Testes automatizados (pytest)
│   ├── conftest.py               # Fixtures de teste
│   ├── test_account.py           # Testes de conta
│   ├── test_app.py               # Testes da aplicação
│   ├── test_database.py          # Testes de integração com o banco
│   └── test_security.py          # Testes de segurança/autenticação
├── pyproject.toml                # Configuração de dependências e ferramentas
└── README.md                     # (Você está aqui)
```

## Requisitos

- Python 3.13+
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone <repo-url>
   cd maddr-api
   ```

2. **Instale as dependências:**
   ```sh
   poetry install
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./test.db
   SECRET_KEY=uma_chave_secreta
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Execute as migrações do banco de dados:**
   ```sh
   poetry run alembic upgrade head
   ```

## Execução

Para rodar o servidor de desenvolvimento:

```sh
poetry run fastapi dev src/maddr_api/app.py
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Testes

Execute todos os testes com cobertura:

```sh
poetry run task test
```

## Principais Endpoints

- `POST /account/` — Criação de conta
- `GET /account/{id}` — Consulta de conta por ID
- `PUT /account/{id}` — Atualização de conta
- `DELETE /account/{id}` — Remoção de conta
- `POST /token/` — Geração de token JWT

## Convenções e Ferramentas

- **Lint:** `ruff`
- **Testes:** `pytest`, `pytest-asyncio`
- **Cobertura:** `coverage`
- **Migrações:** `alembic`
- **Hash de senha:** `pwdlib[argon2]`
- **Autenticação:** JWT (`pyjwt`)

---

> Para dúvidas ou sugestões, abra uma issue ou envie um pull request!