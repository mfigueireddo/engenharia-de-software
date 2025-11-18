from typing import Optional

from src.core.entities.product import Product
from src.core.exceptions import ProductNotFound
from src.core.interfaces.product_repository import ProductRepository
from src.core.interfaces.usecase_interface import UseCase


class EditProductUseCase(UseCase):
    """Use case responsible for registering a new product."""

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def execute(
        self, id: int, nome: Optional[str], marca: Optional[str], categoria: Optional[str], preco: Optional[float], preco_promocional: Optional[float]
    ) -> Product:
        
        produto = self._repository.get_by_id(id)
        if not produto:
            raise ProductNotFound(f"Produto '{id}' não encontrado.")

        if nome is not None:
            produto.nome = nome
        if marca is not None:
            produto.marca = marca
        if categoria is not None:
            produto.categoria = categoria
        if preco is not None:
            produto.preco = preco
        if preco_promocional is not None:
            produto.preco_promocional = preco_promocional

        return self._repository.update(id, produto)
