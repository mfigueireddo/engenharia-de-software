import pytest
from unittest.mock import Mock

from src.core.use_cases.delete_product import DeleteProductUseCase
from src.core.interfaces.product_repository import ProductRepository
from src.core.exceptions import ProductNotFound


def test_execute_deletes_existing_product_by_name():
    repo = Mock(spec=ProductRepository)
    repo.delete_by_name.return_value = True

    use_case = DeleteProductUseCase(repository=repo)

    result = use_case.execute(nome="Sabonete")

    assert result is None
    repo.delete_by_name.assert_called_once_with("Sabonete")


def test_execute_raises_ProductNotFound_when_repository_returns_false():
    repo = Mock(spec=ProductRepository)
    repo.delete_by_name.return_value = False

    use_case = DeleteProductUseCase(repository=repo)

    with pytest.raises(ProductNotFound):
        use_case.execute(nome="ProdutoInexistente")

    repo.delete_by_name.assert_called_once_with("ProdutoInexistente")
    repo.update.assert_not_called() if hasattr(repo, "update") else None  # defensivo


def test_execute_propagates_unexpected_exceptions_from_repository():
    repo = Mock(spec=ProductRepository)
    repo.delete_by_name.side_effect = Exception("db error")

    use_case = DeleteProductUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(nome="QualquerNome")

    repo.delete_by_name.assert_called_once_with("QualquerNome")
