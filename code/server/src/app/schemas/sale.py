from typing import List, Optional

from pydantic import BaseModel
from src.core.entities.sale import Sale, SaleItem

class SaleItemSchema(BaseModel):
    """Schema for a sale item."""
    
    product_id: int
    quantity: int

class VendaSchema(BaseModel):
    """Payload esperado para criação de vendas."""

    items: List[SaleItemSchema]

class VendaBuscaSchema(BaseModel):
    """Estrutura de busca por venda usando o identificador."""

    id: int

class ListagemVendasSchema(BaseModel):
    """Listagem de vendas."""

    vendas: List["VendaViewSchema"]

class VendaViewSchema(BaseModel):
    """Representação de uma venda completa."""

    id: int
    items: List[dict]
    total_amount: float
    data_venda: str

class VendaDelSchema(BaseModel):
    """Retorno após remoção de uma venda."""

    message: str
    id: int

# ======= Devolução ao JS =======

def apresenta_venda(venda: Sale) -> dict:
    """Converte a entidade de domínio para resposta JSON."""
    return {
        "id": venda.id,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price
            }
            for item in venda.items
        ],
        "total_amount": venda.total_amount,
        "data_venda": venda.data_venda.isoformat() if venda.data_venda else None
    }

def apresenta_vendas(vendas: List[Sale]) -> dict:
    """Converte a lista de vendas para resposta JSON."""
    return {
        "vendas": [apresenta_venda(venda) for venda in vendas]
    }