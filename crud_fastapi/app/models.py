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
