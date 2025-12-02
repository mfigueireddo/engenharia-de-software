from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.sale import Sale

class SaleRepository(ABC):
    """Port defining the contract for sale persistence."""

    @abstractmethod
    def add(self, sale: Sale) -> Sale:
        """Persist a sale and return the stored instance."""

    @abstractmethod
    def list_all(self) -> List[Sale]:
        """Return all stored sales."""

    @abstractmethod
    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """Return a sale by identifier, if present."""

    @abstractmethod
    def delete_by_id(self, sale_id: int) -> bool:
        """Delete a sale by id. Returns True if a row was removed."""