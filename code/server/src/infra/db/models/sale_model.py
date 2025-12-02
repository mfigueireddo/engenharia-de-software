from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.db.base import Base
from src.infra.db.models.product_model import ProductModel


class SaleModel(Base):
    __tablename__ = "venda"

    id: Optional[int] = Column("pk_venda", Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)
    
    items = relationship("SaleItemModel", back_populates="sale", cascade="all, delete-orphan")


class SaleItemModel(Base):
    __tablename__ = "item_venda"

    id: Optional[int] = Column("pk_item_venda", Integer, primary_key=True)
    sale_id = Column("fk_venda", Integer, ForeignKey("venda.pk_venda"), nullable=False)
    product_id = Column("fk_produto", Integer, ForeignKey("produto.pk_produto"), nullable=False)
    product_name = Column(String(140), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    sale = relationship("SaleModel", back_populates="items")
    product = relationship("ProductModel")