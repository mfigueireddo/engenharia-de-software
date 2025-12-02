# src/core/tests/use_cases/test_list_products.py

import pytest
from unittest.mock import Mock

from src.core.entities.product import Product
from src.core.use_cases.list_products import ListProductsUseCase
from src.core.interfaces.product_repository import ProductRepository


def test_execute_returns_list_of_products():
    repo = Mock(spec=ProductRepository)
    products = [
        Product(
            nome="Sabonete",
            marca="MarcaX",
            categoria="Higiene",
            preco=5.0,
            preco_promocional=4.0,
        ),
        Product(
            nome="Arroz",
            marca="MarcaY",
            categoria="Alimentos",
            preco=10.0,
            preco_promocional=None,
        ),
    ]
    repo.list_all.return_value = products

    use_case = ListProductsUseCase(repository=repo)

    result = use_case.execute()

    assert result is products
    repo.list_all.assert_called_once()


def test_execute_returns_empty_list_when_no_products():
    repo = Mock(spec=ProductRepository)
    repo.list_all.return_value = []

    use_case = ListProductsUseCase(repository=repo)

    result = use_case.execute()

    assert result == []
    repo.list_all.assert_called_once()


def test_execute_propagates_repository_exceptions():
    repo = Mock(spec=ProductRepository)
    repo.list_all.side_effect = Exception("db error")

    use_case = ListProductsUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute()

    repo.list_all.assert_called_once()
