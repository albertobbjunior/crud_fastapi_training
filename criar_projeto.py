from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ROOT = Path("crud_fastapi")
APP = ROOT / "app"

APP.mkdir(parents=True, exist_ok=True)


# ============================================================
# ARQUIVOS DO PROJETO
# ============================================================

files = {

    "requirements.txt": """
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
""",

    ".env": """
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crud_db
""",

    "docker-compose.yml": """
services:
  postgres:
    image: postgres:16
    container_name: postgres_crud
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: crud_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
""",

    "app/__init__.py": "",

    "app/database.py": """
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
""",

    "app/models.py": """
from sqlalchemy import Column, Date, Integer, String

from .database import Base


class Pessoa(Base):

    __tablename__ = "pessoas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    cidade = Column(
        String(100),
        nullable=False
    )

    estado_civil = Column(
        String(50),
        nullable=False
    )

    data_nascimento = Column(
        Date,
        nullable=False
    )
""",

    "app/schemas.py": """
from datetime import date

from pydantic import BaseModel


class PessoaBase(BaseModel):

    nome: str
    cidade: str
    estado_civil: str
    data_nascimento: date


class PessoaCreate(PessoaBase):
    pass


class PessoaResponse(PessoaBase):

    id: int

    class Config:
        from_attributes = True
""",

    "app/crud.py": """
from sqlalchemy.orm import Session

from .models import Pessoa
from .schemas import PessoaCreate


def criar_pessoa(
    db: Session,
    pessoa: PessoaCreate
):

    nova_pessoa = Pessoa(

        nome=pessoa.nome,

        cidade=pessoa.cidade,

        estado_civil=pessoa.estado_civil,

        data_nascimento=pessoa.data_nascimento
    )

    db.add(nova_pessoa)

    db.commit()

    db.refresh(nova_pessoa)

    return nova_pessoa


def listar_pessoas(db: Session):

    return db.query(Pessoa).all()


def buscar_pessoa(
    db: Session,
    pessoa_id: int
):

    return (
        db
        .query(Pessoa)
        .filter(Pessoa.id == pessoa_id)
        .first()
    )


def atualizar_pessoa(
    db: Session,
    pessoa_id: int,
    pessoa: PessoaCreate
):

    pessoa_db = buscar_pessoa(
        db,
        pessoa_id
    )

    if pessoa_db is None:
        return None


    pessoa_db.nome = pessoa.nome

    pessoa_db.cidade = pessoa.cidade

    pessoa_db.estado_civil = pessoa.estado_civil

    pessoa_db.data_nascimento = (
        pessoa.data_nascimento
    )


    db.commit()

    db.refresh(pessoa_db)

    return pessoa_db


def excluir_pessoa(
    db: Session,
    pessoa_id: int
):

    pessoa_db = buscar_pessoa(
        db,
        pessoa_id
    )

    if pessoa_db is None:
        return None


    db.delete(pessoa_db)

    db.commit()

    return pessoa_db
""",

    "app/main.py": """
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud

from .database import (
    Base,
    engine,
    get_db
)

from .schemas import (
    PessoaCreate,
    PessoaResponse
)


# ============================================================
# CRIA AS TABELAS
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(

    title="API CRUD de Pessoas",

    description=(
        "Projeto acadêmico simples "
        "utilizando FastAPI e PostgreSQL."
    ),

    version="1.0.0"
)


# ============================================================
# ROTA INICIAL
# ============================================================

@app.get("/")
def inicio():

    return {
        "mensagem": "API CRUD funcionando!"
    }


# ============================================================
# CREATE
# ============================================================

@app.post(
    "/pessoas",

    response_model=PessoaResponse,

    status_code=201
)
def criar_pessoa(

    pessoa: PessoaCreate,

    db: Session = Depends(get_db)

):

    return crud.criar_pessoa(
        db,
        pessoa
    )


# ============================================================
# READ - LISTAR
# ============================================================

@app.get(
    "/pessoas",

    response_model=list[PessoaResponse]
)
def listar_pessoas(

    db: Session = Depends(get_db)

):

    return crud.listar_pessoas(db)


# ============================================================
# READ - BUSCAR POR ID
# ============================================================

@app.get(
    "/pessoas/{pessoa_id}",

    response_model=PessoaResponse
)
def buscar_pessoa(

    pessoa_id: int,

    db: Session = Depends(get_db)

):

    pessoa = crud.buscar_pessoa(
        db,
        pessoa_id
    )


    if pessoa is None:

        raise HTTPException(

            status_code=404,

            detail="Pessoa não encontrada"
        )


    return pessoa


# ============================================================
# UPDATE
# ============================================================

@app.put(
    "/pessoas/{pessoa_id}",

    response_model=PessoaResponse
)
def atualizar_pessoa(

    pessoa_id: int,

    pessoa: PessoaCreate,

    db: Session = Depends(get_db)

):

    pessoa_atualizada = (
        crud.atualizar_pessoa(

            db,

            pessoa_id,

            pessoa
        )
    )


    if pessoa_atualizada is None:

        raise HTTPException(

            status_code=404,

            detail="Pessoa não encontrada"
        )


    return pessoa_atualizada


# ============================================================
# DELETE
# ============================================================

@app.delete(
    "/pessoas/{pessoa_id}"
)
def excluir_pessoa(

    pessoa_id: int,

    db: Session = Depends(get_db)

):

    pessoa_excluida = (
        crud.excluir_pessoa(

            db,

            pessoa_id
        )
    )


    if pessoa_excluida is None:

        raise HTTPException(

            status_code=404,

            detail="Pessoa não encontrada"
        )


    return {

        "mensagem":
        "Pessoa excluída com sucesso"
    }
""",

    "README.md": """
# CRUD FastAPI + PostgreSQL

Projeto acadêmico simples utilizando:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Uvicorn

---

# 1. Criar ambiente virtual

Windows:

    python -m venv venv

Ativar:

    venv\\Scripts\\activate

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
"""
}


# ============================================================
# CRIAR OS ARQUIVOS
# ============================================================

for filename, content in files.items():

    file_path = ROOT / filename

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print(" PROJETO CRIADO COM SUCESSO!")
print("=" * 60)
print()
print(f"Pasta: {ROOT.absolute()}")
print()
print("Próximos passos:")
print()
print("1. Entre na pasta:")
print("   cd crud_fastapi")
print()
print("2. Crie o ambiente virtual:")
print("   python -m venv venv")
print()
print("3. Ative o ambiente virtual:")
print("   Windows: venv\\Scripts\\activate")
print()
print("4. Instale as dependências:")
print("   pip install -r requirements.txt")
print()
print("5. Suba o PostgreSQL:")
print("   docker compose up -d")
print()
print("6. Inicie a API:")
print("   uvicorn app.main:app --reload")
print()
print("7. Abra:")
print("   http://127.0.0.1:8000/docs")
print()
print("=" * 60)
