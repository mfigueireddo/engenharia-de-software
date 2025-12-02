from typing import List

from src.core.entities.sale import Sale
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.usecase_interface import UseCase

class ListSalesUseCase(UseCase):
    """Use case responsible for listing all sales."""

    def __init__(self, repository: SaleRepository):
        self._repository = repository

    def execute(self) -> List[Sale]:
        """Execute the list sales use case."""
        return self._repository.list_all()