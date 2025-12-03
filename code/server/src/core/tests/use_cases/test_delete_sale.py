import pytest
from unittest.mock import Mock

from src.core.use_cases.delete_sale import DeleteSaleUseCase
from src.core.interfaces.sale_repository import SaleRepository
from src.core.exceptions import SaleNotFound


def test_execute_deletes_existing_sale_by_id():
    repo = Mock(spec=SaleRepository)
    repo.get_by_id.return_value = object()
    repo.delete_by_id.return_value = True

    use_case = DeleteSaleUseCase(repository=repo)

    result = use_case.execute(sale_id=1)

    assert result is True

    repo.get_by_id.assert_called_once_with(1)
    repo.delete_by_id.assert_called_once_with(1)


def test_execute_raises_SaleNotFound_when_sale_does_not_exist():
    repo = Mock(spec=SaleRepository)
    repo.get_by_id.return_value = None

    use_case = DeleteSaleUseCase(repository=repo)

    with pytest.raises(SaleNotFound):
        use_case.execute(sale_id=999)

    repo.get_by_id.assert_called_once_with(999)
    repo.delete_by_id.assert_not_called()


def test_execute_propagates_unexpected_exceptions_from_repository():
    repo = Mock(spec=SaleRepository)
    repo.get_by_id.return_value = object()
    repo.delete_by_id.side_effect = Exception("db error")

    use_case = DeleteSaleUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(sale_id=5)

    repo.get_by_id.assert_called_once_with(5)
    repo.delete_by_id.assert_called_once_with(5)