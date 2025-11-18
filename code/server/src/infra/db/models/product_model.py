from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from src.infra.db.base import Base


class ProductModel(Base):
    __tablename__ = "produto"

    id: Optional[int] = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)
    marca = Column(String(140), unique=False, nullable=False)
    categoria = Column(String(140), unique=False, nullable=False)
    preco = Column(Float, nullable=False)
    preco_promocional = Column(Float)
    data_insercao = Column(DateTime, default=datetime.utcnow)