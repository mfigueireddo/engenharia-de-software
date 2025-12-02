import pytest
from unittest.mock import Mock

from src.core.use_cases.add_sale import AddSaleUseCase
from src.core.interfaces.sale_repository import SaleRepository
from src.core.entities.sale import Sale  # usado apenas para especificação de mocks, se existir


def test_execute_adds_sale_and_returns_repository_result():
    repo = Mock(spec=SaleRepository)
    returned_sale = Mock(spec=Sale)
    repo.add.return_value = returned_sale

    use_case = AddSaleUseCase(repository=repo)

    result = use_case.execute(
        cliente="ClienteX",
        itens=[{"produto_id": 1, "quantidade": 2}],
        total=100.0,
    )

    assert result is returned_sale
    repo.add.assert_called_once()

    added_sale_arg = repo.add.call_args.args[0]
    assert added_sale_arg is not None


def test_execute_propagates_repository_exceptions():
    repo = Mock(spec=SaleRepository)
    repo.add.side_effect = Exception("db error")

    use_case = AddSaleUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(
            cliente="ClienteY",
            itens=[],
            total=0.0,
        )

    repo.add.assert_called_once()