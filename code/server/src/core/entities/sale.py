from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class SaleItem:
    """Represents an item in a sale with product and quantity."""
    
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

@dataclass
class Sale:
    """Domain representation of a sale."""

    items: List[SaleItem]
    total_amount: float
    
    id: Optional[int] = None
    #data_venda: datetime = field(default_factory=datetime.utcnow)
    data_venda: datetime = field(default_factory=datetime.now)