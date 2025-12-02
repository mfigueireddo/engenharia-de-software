from typing import Optional

from src.core.entities.sale import Sale
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.usecase_interface import UseCase
from src.core.exceptions import SaleNotFound

class GetSaleUseCase(UseCase):
    """Use case responsible for retrieving a sale by ID."""

    def __init__(self, repository: SaleRepository):
        self._repository = repository

    def execute(self, sale_id: int) -> Sale:
        """Execute the get sale use case."""
        sale = self._repository.get_by_id(sale_id)
        if not sale:
            raise SaleNotFound(f"Venda com ID {sale_id} não encontrada.")
        return sale