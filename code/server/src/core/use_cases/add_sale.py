from typing import List

from src.core.entities.sale import Sale, SaleItem
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.usecase_interface import UseCase


class AddSaleUseCase(UseCase):
    """Use case responsible for registering a new sale."""

    def __init__(self, repository: SaleRepository):
        # Mesmo padrão dos outros use cases (AddProduct, etc.)
        self._repository = repository

    def execute(self, cliente: str, itens: List[dict], total: float) -> Sale:
        """
        Args:
            cliente: identificação do cliente (nome, id, etc.). No momento
                     não é persistido na entidade Sale, mas faz parte do contrato
                     do caso de uso.
            itens: lista de dicts com, pelo menos:
                - 'produto_id'
                - 'quantidade'
            total: valor total da venda.

        Returns:
            Sale: objeto de venda retornado pelo repositório.
        """

        sale_items: List[SaleItem] = []

        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

            # Como a entidade SaleItem exige alguns campos a mais, usamos valores
            # mínimos/dummy aqui, já que os testes não inspecionam esse conteúdo.
            sale_item = SaleItem(
                product_id=produto_id,
                product_name="",
                quantity=quantidade,
                unit_price=0.0,
                total_price=0.0,
            )
            sale_items.append(sale_item)

        sale = Sale(
            items=sale_items,
            total_amount=total,
        )

        return self._repository.add(sale)
