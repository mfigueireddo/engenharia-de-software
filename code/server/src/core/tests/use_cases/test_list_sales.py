import pytest
from unittest.mock import Mock

from src.core.use_cases.list_sales import ListSalesUseCase
from src.core.interfaces.sale_repository import SaleRepository
from src.core.entities.sale import Sale


def test_execute_returns_list_of_sales():
    repo = Mock(spec=SaleRepository)
    sales = [Mock(spec=Sale), Mock(spec=Sale)]
    repo.list_all.return_value = sales

    use_case = ListSalesUseCase(repository=repo)

    result = use_case.execute()

    assert result is sales
    repo.list_all.assert_called_once()


def test_execute_returns_empty_list_when_no_sales():
    repo = Mock(spec=SaleRepository)
    repo.list_all.return_value = []

    use_case = ListSalesUseCase(repository=repo)

    result = use_case.execute()

    assert result == []
    repo.list_all.assert_called_once()


def test_execute_propagates_repository_exceptions():
    repo = Mock(spec=SaleRepository)
    repo.list_all.side_effect = Exception("db error")

    use_case = ListSalesUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute()

    repo.list_all.assert_called_once()