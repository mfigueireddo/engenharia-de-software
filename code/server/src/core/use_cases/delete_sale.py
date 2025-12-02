# src/core/use_cases/delete_sale.py

from src.core.exceptions import SaleNotFound
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.usecase_interface import UseCase


class DeleteSaleUseCase(UseCase):
    """Use case responsável por remover uma venda pelo id."""

    def __init__(self, repository: SaleRepository):
        self._repository = repository

    def execute(self, sale_id: int) -> None:
        removed = self._repository.delete_by_id(sale_id)
        if not removed:
            raise SaleNotFound(f"Venda '{sale_id}' não encontrada.")
        # sucesso -> não precisa retornar nada (None)
        return None