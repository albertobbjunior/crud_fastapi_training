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
