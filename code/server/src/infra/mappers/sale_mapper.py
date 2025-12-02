from typing import List

from src.core.entities.sale import Sale, SaleItem
from src.infra.db.models.sale_model import SaleModel, SaleItemModel

def sale_item_to_domain(item_model: SaleItemModel) -> SaleItem:
    """Convert SaleItemModel to SaleItem domain entity."""
    return SaleItem(
        product_id=item_model.product_id,
        product_name=item_model.product_name,
        quantity=item_model.quantity,
        unit_price=item_model.unit_price,
        total_price=item_model.total_price
    )

def to_domain(model: SaleModel) -> Sale:
    """Convert SaleModel to Sale domain entity."""
    return Sale(
        id=model.id,
        items=[sale_item_to_domain(item) for item in model.items],
        total_amount=model.total_amount,
        data_venda=model.data_venda,
    )

def to_domain_list(models: List[SaleModel]) -> List[Sale]:
    """Convert list of SaleModel to list of Sale domain entities."""
    return [to_domain(model) for model in models]

def sale_item_to_model(item: SaleItem, sale_id: int) -> SaleItemModel:
    """Convert SaleItem domain entity to SaleItemModel."""
    return SaleItemModel(
        sale_id=sale_id,
        product_id=item.product_id,
        product_name=item.product_name,
        quantity=item.quantity,
        unit_price=item.unit_price,
        total_price=item.total_price
    )

def from_domain(sale: Sale) -> SaleModel:
    """Convert Sale domain entity to SaleModel."""
    sale_model = SaleModel(
        id=sale.id,
        total_amount=sale.total_amount,
        data_venda=sale.data_venda
    )
    
    return sale_model