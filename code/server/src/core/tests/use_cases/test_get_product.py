import pytest
from unittest.mock import Mock

from src.core.entities.product import Product
from src.core.use_cases.get_product import GetProductUseCase
from src.core.interfaces.product_repository import ProductRepository
from src.core.exceptions import ProductNotFound


def test_execute_returns_product_when_found_by_id():
    repo = Mock(spec=ProductRepository)
    returned = Product(
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=5.0,
        preco_promocional=4.0,
    )
    repo.get_by_id.return_value = returned

    use_case = GetProductUseCase(repository=repo)

    result = use_case.execute(product_id=1)

    assert result is returned
    repo.get_by_id.assert_called_once_with(1)


def test_execute_raises_ProductNotFound_when_product_missing():
    repo = Mock(spec=ProductRepository)
    repo.get_by_id.return_value = None

    use_case = GetProductUseCase(repository=repo)

    with pytest.raises(ProductNotFound):
        use_case.execute(product_id=42)

    repo.get_by_id.assert_called_once_with(42)


def test_execute_propagates_repository_exceptions():
    repo = Mock(spec=ProductRepository)
    repo.get_by_id.side_effect = Exception("db error")

    use_case = GetProductUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(product_id=99)

    repo.get_by_id.assert_called_once_with(99)
