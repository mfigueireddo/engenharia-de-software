from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    """Domain representation of a product."""

    nome: str
    marca: str
    categoria: str
    preco: float
    preco_promocional: Optional[float]

    id: Optional[int] = None # Tem que ficar por último!
    data_insercao: datetime = field(default_factory=datetime.utcnow)