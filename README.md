# MADDR API - Documentação Completa

API RESTful para gerenciamento de livros, autores e contas de usuário, construída com FastAPI, SQLAlchemy (async), Alembic e autenticação JWT.

## 📋 Índice

- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Execução](#️-execução)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Modelos de Dados](#️-modelos-de-dados)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação e Segurança](#-autenticação-e-segurança)
- [Testes](#-testes)
- [Comandos Úteis](#️-comandos-úteis)

---

## 📋 Requisitos

- **Python:** 3.13+
- **Poetry:** Para gerenciamento de dependências
- **Banco de Dados:** SQLite (padrão) ou outro compatível com SQLAlchemy

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <repo-url>
cd maddr-api
```

### 2. Instale as dependências

```bash
poetry install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./maddr_db.db
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Execute as migrações do banco de dados

```bash
poetry run alembic upgrade head
```

---

## ▶️ Execução

### Servidor de Desenvolvimento

```bash
poetry run fastapi dev src/maddr_api/app.py
```

O servidor estará disponível em: **`http://localhost:8000`**

### Documentação Interativa

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📁 Estrutura do Projeto

```
maddr-api/
├── src/
│   └── maddr_api/
│       ├── __init__.py
│       ├── app.py                    # Aplicação principal FastAPI
│       ├── config/
│       │   ├── database.py           # Configuração do banco de dados
│       │   └── settings.py           # Configurações da aplicação
│       ├── models/                   # Modelos SQLAlchemy
│       │   ├── __init__.py
│       │   ├── account.py            # Modelo de conta de usuário
│       │   ├── author.py             # Modelo de autor
│       │   └── book.py               # Modelo de livro
│       ├── schemas/                  # Schemas Pydantic
│       │   ├── __init__.py
│       │   ├── account.py            # Schemas de conta
│       │   ├── author.py             # Schemas de autor
│       │   ├── book.py               # Schemas de livro
│       │   └── token.py              # Schemas de token
│       ├── routers/                  # Rotas da API
│       │   ├── __init__.py
│       │   ├── account.py            # Endpoints de conta
│       │   ├── author.py             # Endpoints de autor
│       │   ├── book.py               # Endpoints de livro
│       │   └── token.py              # Endpoints de autenticação
│       ├── services/                 # Lógica de negócio
│       │   ├── __init__.py
│       │   ├── main.py               # BaseCRUD genérico
│       │   ├── account.py            # Serviços de conta
│       │   ├── author.py             # Serviços de autor
│       │   ├── book.py               # Serviços de livro
│       │   └── token.py              # Serviços de token
│       ├── security/                 # Segurança e autenticação
│       │   ├── access_token.py       # Criação de tokens JWT
│       │   ├── get_current_user.py   # Middleware de autenticação
│       │   └── hash_password.py      # Hash de senhas (Argon2)
│       └── utils/                    # Utilitários
│           └── sanitization.py       # Sanitização de strings
├── migrations/                       # Migrações Alembic
│   ├── versions/
│   └── env.py
├── tests/                            # Testes automatizados
│   ├── conftest.py
│   ├── test_account.py
│   ├── test_author.py
│   ├── test_book.py
│   ├── test_security.py
│   └── test_token.py
├── pyproject.toml                    # Configuração do projeto
├── alembic.ini                       # Configuração do Alembic
└── README.md
```

---

## 🗄️ Modelos de Dados

### Account (Conta de Usuário)

```python
{
  "id": int,                  # ID único (gerado automaticamente)
  "username": str,            # Nome de usuário (único)
  "email": str,               # Email (único)
  "password": str,            # Senha (hash Argon2)
  "created_at": datetime,     # Data de criação
  "updated_at": datetime      # Data de atualização
}
```

### Author (Autor)

```python
{
  "id": int,                  # ID único (gerado automaticamente)
  "name": str,                # Nome do autor
  "created_at": datetime,     # Data de criação
  "updated_at": datetime,     # Data de atualização
  "books": list[Book]         # Lista de livros (relacionamento)
}
```

### Book (Livro)

```python
{
  "id": int,                  # ID único (gerado automaticamente)
  "title": str,               # Título do livro
  "author_id": int,           # ID do autor (FK)
  "publish_year": int,        # Ano de publicação
  "created_at": datetime,     # Data de criação
  "updated_at": datetime,     # Data de atualização
  "author": Author            # Relação com autor
}
```

---

## 📚 Endpoints da API

### 🏠 Root

#### **GET /**
- **Descrição:** Endpoint de boas-vindas
- **Autenticação:** Não requerida
- **Resposta:** `200 OK`
```json
{
  "message": "Welcome to the MADDR API!"
}
```

---

### 🔐 Autenticação (Token)

#### **POST /token/**
Gera um token de acesso JWT para autenticação.

- **Autenticação:** Não requerida
- **Content-Type:** `application/x-www-form-urlencoded`
- **Corpo da Requisição:**
  - `username` (string): Nome de usuário
  - `password` (string): Senha

- **Resposta:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

- **Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu_usuario&password=sua_senha"
```

#### **POST /token/refresh-token**
Renova o token de acesso existente.

- **Autenticação:** Não requerida
- **Content-Type:** `application/x-www-form-urlencoded`
- **Corpo da Requisição:**
  - `username` (string): Nome de usuário
  - `password` (string): Senha

- **Resposta:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 👤 Contas (Account)

#### **POST /account/**
Cria uma nova conta de usuário.

- **Autenticação:** Não requerida
- **Corpo da Requisição:**
```json
{
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com",
  "password": "senha_segura123"
}
```

- **Resposta:** `201 CREATED`
```json
{
  "id": 1,
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com"
}
```

- **Validações:**
  - Username e email devem ser únicos
  - Senha será armazenada com hash Argon2
  
- **Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/account/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_exemplo",
    "email": "usuario@exemplo.com",
    "password": "senha_segura123"
  }'
```

#### **GET /account/{account_id}**
Recupera os dados de uma conta pelo ID.

- **Autenticação:** Não requerida
- **Parâmetros:**
  - `account_id` (path, int): ID da conta

- **Resposta:** `200 OK`
```json
{
  "id": 1,
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com"
}
```

- **Erros:**
  - `404 NOT FOUND`: Conta não encontrada

#### **PUT /account/{account_id}**
Atualiza os dados de uma conta.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `account_id` (path, int): ID da conta
  
- **Corpo da Requisição:**
```json
{
  "username": "novo_usuario",
  "email": "novo@exemplo.com",
  "password": "nova_senha123"
}
```

- **Resposta:** `200 OK`
```json
{
  "id": 1,
  "username": "novo_usuario",
  "email": "novo@exemplo.com"
}
```

- **Validações:**
  - Apenas o próprio usuário pode atualizar sua conta
  - Username e email devem permanecer únicos

- **Exemplo cURL:**
```bash
curl -X PUT "http://localhost:8000/account/1" \
  -H "Authorization: Bearer seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novo_usuario",
    "email": "novo@exemplo.com",
    "password": "nova_senha123"
  }'
```

#### **DELETE /account/{account_id}**
Remove uma conta do sistema.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `account_id` (path, int): ID da conta

- **Resposta:** `200 OK`
```json
{
  "message": "Account deleted successfully."
}
```

- **Validações:**
  - Apenas o próprio usuário pode deletar sua conta

---

### ✍️ Autores (Author)

#### **POST /author/**
Cria um novo autor.

- **Autenticação:** Requerida (Bearer Token)
- **Corpo da Requisição:**
```json
{
  "name": "J.K. Rowling"
}
```

- **Resposta:** `201 CREATED`
```json
{
  "id": 1,
  "name": "J.K. Rowling"
}
```

- **Validações:**
  - Nome do autor deve ser único
  - Nome é sanitizado automaticamente

- **Erros:**
  - `409 CONFLICT`: Autor com esse nome já existe

- **Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/author/" \
  -H "Authorization: Bearer seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{"name": "J.K. Rowling"}'
```

#### **GET /author/{author_id}**
Recupera os dados de um autor pelo ID.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `author_id` (path, int): ID do autor

- **Resposta:** `200 OK`
```json
{
  "id": 1,
  "name": "J.K. Rowling"
}
```

- **Erros:**
  - `404 NOT FOUND`: Autor não encontrado

#### **PATCH /author/{author_id}**
Atualiza os dados de um autor.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `author_id` (path, int): ID do autor
  
- **Corpo da Requisição:**
```json
{
  "name": "Novo Nome do Autor"
}
```

- **Resposta:** `200 OK`
```json
{
  "id": 1,
  "name": "Novo Nome do Autor"
}
```

- **Validações:**
  - Nome deve permanecer único

#### **DELETE /author/{author_id}**
Remove um autor do sistema.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `author_id` (path, int): ID do autor

- **Resposta:** `200 OK`
```json
{
  "message": "Author deleted successfully."
}
```

- **Nota:** Livros relacionados ao autor também serão afetados pelo relacionamento configurado

---

### 📖 Livros (Book)

#### **POST /book/**
Cria um novo livro.

- **Autenticação:** Requerida (Bearer Token)
- **Corpo da Requisição:**
```json
{
  "title": "Harry Potter e a Pedra Filosofal",
  "author_id": 1,
  "publish_year": 1997
}
```

- **Resposta:** `201 CREATED`
```json
{
  "id": 1,
  "title": "Harry Potter e a Pedra Filosofal",
  "author_id": 1,
  "publish_year": 1997
}
```

- **Validações:**
  - Título deve ser único
  - Author_id deve existir no banco de dados
  - Título é sanitizado automaticamente

- **Erros:**
  - `409 CONFLICT`: Livro com esse título já existe

- **Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/book/" \
  -H "Authorization: Bearer seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter e a Pedra Filosofal",
    "author_id": 1,
    "publish_year": 1997
  }'
```

#### **GET /book/{book_id}**
Recupera os dados de um livro pelo ID.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros:**
  - `book_id` (path, int): ID do livro

- **Resposta:** `200 OK`
```json
{
  "id": 1,
  "title": "Harry Potter e a Pedra Filosofal",
  "author_id": 1,
  "publish_year": 1997
}
```

- **Erros:**
  - `404 NOT FOUND`: Livro não encontrado

#### **GET /book/**
Lista todos os livros com filtros opcionais e paginação.

- **Autenticação:** Requerida (Bearer Token)
- **Parâmetros de Query:**
  - `title` (opcional, string): Filtrar por título (busca parcial)
  - `publish_year` (opcional, int): Filtrar por ano de publicação
  - `limit` (opcional, int, padrão: 20): Número máximo de resultados
  - `skip` (opcional, int, padrão: 0): Número de registros a pular

- **Resposta:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Harry Potter e a Pedra Filosofal",
    "author_id": 1,
    "publish_year": 1997
  },
  {
    "id": 2,
    "title": "Harry Potter e a Câmara Secreta",
    "author_id": 1,
    "publish_year": 1998
  }
]
```

- **Exemplos cURL:**

Listar todos os livros (primeiros 20):
```bash
curl -X GET "http://localhost:8000/book/" \
  -H "Authorization: Bearer seu_token_aqui"
```

Filtrar por título:
```bash
curl -X GET "http://localhost:8000/book/?title=Harry%20Potter" \
  -H "Authorization: Bearer seu_token_aqui"
```

Filtrar por ano de publicação:
```bash
curl -X GET "http://localhost:8000/book/?publish_year=1997" \
  -H "Authorization: Bearer seu_token_aqui"
```

Paginação (pular 10, retornar 5):
```bash
curl -X GET "http://localhost:8000/book/?skip=10&limit=5" \
  -H "Authorization: Bearer seu_token_aqui"
```

Filtros combinados:
```bash
curl -X GET "http://localhost:8000/book/?title=Harry&publish_year=1997&limit=10&skip=0" \
  -H "Authorization: Bearer seu_token_aqui"
```

---

## 🔒 Autenticação e Segurança

### Sistema de Autenticação

A API utiliza **JSON Web Tokens (JWT)** para autenticação:

1. **Obtenha um token:** Faça login via `POST /token/` com suas credenciais
2. **Use o token:** Inclua o header `Authorization: Bearer {token}` nas requisições
3. **Renove o token:** Use `POST /token/refresh-token` quando necessário

### Segurança de Senhas

- Senhas são armazenadas usando **Argon2** (via `pwdlib`)
- Hash seguro com salt automático
- Verificação de senha protegida contra timing attacks

### Sanitização de Dados

- Todos os campos de texto (títulos, nomes) são sanitizados antes de serem salvos
- Proteção contra caracteres especiais e espaços em branco desnecessários

### Endpoints Protegidos

Os seguintes endpoints **requerem autenticação**:
- Todos os endpoints de `/author/` (exceto root)
- Todos os endpoints de `/book/` (exceto root)
- `PUT /account/{account_id}`
- `DELETE /account/{account_id}`

Os seguintes endpoints **não requerem autenticação**:
- `POST /account/` (criar conta)
- `GET /account/{account_id}` (ler conta pública)
- `POST /token/` (obter token)
- `POST /token/refresh-token` (renovar token)

---

## 🧪 Testes

### Executar Todos os Testes

```bash
poetry run task test
```

Este comando irá:
1. Executar o lint (ruff check)
2. Rodar todos os testes com pytest
3. Gerar relatório de cobertura
4. Criar relatório HTML em `htmlcov/`

### Executar Testes Específicos

```bash
# Apenas testes de account
poetry run pytest tests/test_account.py -v

# Apenas testes de author
poetry run pytest tests/test_author.py -v

# Apenas testes de book
poetry run pytest tests/test_book.py -v

# Apenas testes de segurança
poetry run pytest tests/test_security.py -v
```

### Ver Cobertura de Testes

```bash
# Abrir relatório HTML
open htmlcov/index.html
```

---

## 🛠️ Comandos Úteis

### Desenvolvimento

```bash
# Rodar servidor de desenvolvimento
poetry run task run

# Ou diretamente
poetry run fastapi dev src/maddr_api/app.py
```

### Linting e Formatação

```bash
# Verificar problemas de código
poetry run task lint

# Corrigir problemas automaticamente
poetry run ruff check --fix

# Formatar código
poetry run task format
```

### Migrações de Banco de Dados

```bash
# Criar nova migração
poetry run alembic revision --autogenerate -m "descrição da migração"

# Aplicar migrações
poetry run alembic upgrade head

# Reverter última migração
poetry run alembic downgrade -1

# Ver histórico de migrações
poetry run alembic history
```

### Gerenciamento de Dependências

```bash
# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show
```

---

## 📝 Fluxo de Uso Recomendado

### 1. Criar uma Conta

```bash
curl -X POST "http://localhost:8000/account/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "meu_usuario",
    "email": "meu@email.com",
    "password": "senha_segura123"
  }'
```

### 2. Obter Token de Autenticação

```bash
curl -X POST "http://localhost:8000/token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=meu_usuario&password=senha_segura123"
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Usar o Token nas Requisições

Salve o token em uma variável:
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Criar um Autor

```bash
curl -X POST "http://localhost:8000/author/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "J.K. Rowling"}'
```

### 5. Criar um Livro

```bash
curl -X POST "http://localhost:8000/book/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter e a Pedra Filosofal",
    "author_id": 1,
    "publish_year": 1997
  }'
```

### 6. Listar Livros

```bash
curl -X GET "http://localhost:8000/book/" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Buscar Livros por Filtro

```bash
curl -X GET "http://localhost:8000/book/?title=Harry&publish_year=1997" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔧 Tecnologias Utilizadas

| Categoria | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework | FastAPI | 0.119.0+ |
| ORM | SQLAlchemy | 2.0.44+ |
| Migrações | Alembic | 1.17.0+ |
| Validação | Pydantic | (via FastAPI) |
| Autenticação | PyJWT | 2.10.1+ |
| Hash de Senha | pwdlib[argon2] | 0.2.1+ |
| Testes | pytest | 8.4.2+ |
| Cobertura | pytest-cov | 7.0.0+ |
| Lint/Format | ruff | 0.14.1+ |
| Task Runner | taskipy | 1.14.1+ |

---

## 📄 Licença

Este projeto está sob licença [escolha sua licença].

---

## 👨‍💻 Autor

**lucas.harmatiuk**

---