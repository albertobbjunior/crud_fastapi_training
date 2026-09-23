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
