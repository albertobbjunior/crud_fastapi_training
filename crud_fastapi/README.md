# CRUD FastAPI + PostgreSQL

Projeto acadêmico simples utilizando:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Uvicorn2

---

# 1. Criar ambiente virtual

Windows:

    python -m venv venv

Ativar:

    venv\Scripts\activate

Linux/Mac:

    python3 -m venv venv

    source venv/bin/activate

---

# 2. Instalar dependências

    pip install -r requirements.txt

---

# 3. Subir PostgreSQL

É necessário ter Docker instalado.

Execute:

    docker compose up -d

---

# 4. Iniciar a API

Execute:

    uvicorn app.main:app --reload

---

# 5. Abrir a API

    http://127.0.0.1:8000

---

# 6. Abrir o Swagger

    http://127.0.0.1:8000/docs

---

# ENDPOINTS

Criar:

    POST /pessoas

Listar:

    GET /pessoas

Buscar:

    GET /pessoas/{id}

Atualizar:

    PUT /pessoas/{id}

Excluir:

    DELETE /pessoas/{id}

---

# EXEMPLO

POST /pessoas

JSON:

{
    "nome": "João Silva",
    "cidade": "Porto",
    "estado_civil": "Solteiro",
    "data_nascimento": "1995-05-20"
}

---

# BANCO

Banco:

    crud_db

Usuário:

    postgres

Senha:

    postgres

Porta:

    5432

Tabela:

    pessoas
