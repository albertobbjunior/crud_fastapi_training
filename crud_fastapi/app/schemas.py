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
