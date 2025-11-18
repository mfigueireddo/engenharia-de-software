from typing import List, Optional

from pydantic import BaseModel
from src.core.entities.product import Product

class ProdutoSchema(BaseModel):
    """Payload esperado para criação de produtos."""

    nome: str
    marca: str
    categoria: str
    preco: float
    preco_promocional: Optional[float] = None


class ProdutoBuscaSchema(BaseModel):
    """Estrutura de busca por produto usando o identificador."""

    id: int


class ProdutoBuscaPorNomeSchema(BaseModel):
    """Estrutura para operações que utilizam o nome do produto."""

    nome: str


class ListagemProdutosSchema(BaseModel):
    """Listagem de produtos."""

    produtos: List[ProdutoSchema]


class ProdutoViewSchema(BaseModel):
    """Representação de um produto com seus comentários."""

    id: int
    nome: str
    marca: str
    categoria: str
    preco: float
    preco_promocional: Optional[float]

class ProdutoEditSchema(BaseModel):

    id: int
    nome: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = None
    preco_promocional: Optional[float] = None

class ProdutoDelSchema(BaseModel):
    """Retorno após remoção de um produto."""

    message: str
    nome: str

# ======= Devolução ao JS =======

def apresenta_produto(produto: Product) -> dict:
    """Converte a entidade de domínio para resposta JSON."""
    return {
        "id": produto.id,
        "nome": produto.nome,
        "marca": produto.marca,
        "categoria": produto.categoria,
        "preco": produto.preco,
        "preco_promocional": produto.preco_promocional
    }


def apresenta_produtos(produtos: List[Product]) -> dict:
    """Converte a lista de produtos para resposta JSON."""
    return {
        "produtos": [
            {
                "id": produto.id,
                "nome": produto.nome,
                "marca": produto.marca,
                "categoria": produto.categoria,
                "preco": produto.preco,
                "preco_promocional": produto.preco_promocional,
            }
            for produto in produtos
        ]
    }
