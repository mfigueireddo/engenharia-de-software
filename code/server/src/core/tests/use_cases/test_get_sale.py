import pytest
from unittest.mock import Mock

from src.core.use_cases.get_sale import GetSaleUseCase
from src.core.interfaces.sale_repository import SaleRepository
from src.core.entities.sale import Sale
from src.core.exceptions import SaleNotFound


def test_execute_returns_sale_when_found_by_id():
    repo = Mock(spec=SaleRepository)
    returned = Mock(spec=Sale)
    repo.get_by_id.return_value = returned

    use_case = GetSaleUseCase(repository=repo)

    result = use_case.execute(sale_id=1)

    assert result is returned
    repo.get_by_id.assert_called_once_with(1)


def test_execute_raises_SaleNotFound_when_sale_missing():
    repo = Mock(spec=SaleRepository)
    repo.get_by_id.return_value = None

    use_case = GetSaleUseCase(repository=repo)

    with pytest.raises(SaleNotFound):
        use_case.execute(sale_id=42)

    repo.get_by_id.assert_called_once_with(42)


def test_execute_propagates_repository_exceptions():
    repo = Mock(spec=SaleRepository)
    repo.get_by_id.side_effect = Exception("db error")

    use_case = GetSaleUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(sale_id=99)

    repo.get_by_id.assert_called_once_with(99)