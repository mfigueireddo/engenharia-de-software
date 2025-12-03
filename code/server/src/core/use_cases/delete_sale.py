from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.usecase_interface import UseCase
from src.core.exceptions import SaleNotFound

class DeleteSaleUseCase(UseCase):
    """Use case responsible for deleting a sale."""

    def __init__(self, repository: SaleRepository):
        self._repository = repository

    def execute(self, sale_id: int) -> bool:
        """Execute the delete sale use case."""
        sale = self._repository.get_by_id(sale_id)
        if not sale:
            raise SaleNotFound(f"Venda com ID {sale_id} não encontrada.")
        
        return self._repository.delete_by_id(sale_id)