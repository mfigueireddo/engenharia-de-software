from typing import List

from src.core.entities.sale import Sale, SaleItem
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.product_repository import ProductRepository
from src.core.interfaces.usecase_interface import UseCase
from src.core.exceptions import ProductNotFound

class AddSaleUseCase(UseCase):
    """Use case responsible for registering a new sale."""

    def __init__(self, repository: SaleRepository):
        self._repository = repository

    def execute(self, items_data: List[dict]) -> Sale:
        """
        Execute the add sale use case.
        
        Args:
            items_data: List of dict with 'product_id' and 'quantity'
        
        Returns:
            Sale: The created sale
        """
        
        sale_items = []
        total_amount = 0.0
        
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            
            product = self._product_repository.get_by_id(product_id)
            if not product:
                raise ProductNotFound(f"Produto com ID {product_id} não encontrado.")
            
            # Use preço promocional se existir, caso contrário preço regular
            unit_price = product.preco_promocional if product.preco_promocional else product.preco
            total_price = unit_price * quantity
            
            sale_item = SaleItem(
                product_id=product.id,
                product_name=product.nome,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            
            sale_items.append(sale_item)
            total_amount += total_price
        
        sale = Sale(
            items=sale_items,
            total_amount=total_amount
        )
        
        return self._sale_repository.add(sale)