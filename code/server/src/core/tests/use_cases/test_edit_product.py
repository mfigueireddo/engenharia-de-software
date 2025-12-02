import pytest
from unittest.mock import Mock

from src.core.entities.product import Product
from src.core.use_cases.edit_product import EditProductUseCase
from src.core.interfaces.product_repository import ProductRepository
from src.core.exceptions import ProductNotFound


def test_execute_updates_existing_product_and_returns_updated_entity():
    repo = Mock(spec=ProductRepository)

    existing = Product(
        id=1,
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=5.0,
        preco_promocional=4.0,
    )
    repo.get_by_id.return_value = existing

    updated_product = Product(
        id=1,
        nome="Sabonete",
        marca="MarcaNova",
        categoria="Higiene",
        preco=6.0,
        preco_promocional=4.0,  # continua 4.0 porque preco_promocional=None não altera
    )
    repo.update.return_value = updated_product

    use_case = EditProductUseCase(repository=repo)

    result = use_case.execute(
        id=1,
        nome=None,
        marca="MarcaNova",
        categoria=None,
        preco=6.0,
        preco_promocional=None,
    )

    assert result is updated_product

    repo.get_by_id.assert_called_once_with(1)
    repo.update.assert_called_once()

    called_id, called_product = repo.update.call_args.args

    assert called_id == 1
    assert isinstance(called_product, Product)

    assert called_product.marca == "MarcaNova"
    assert called_product.preco == 6.0

    # campos não atualizados permanecem
    assert called_product.nome == "Sabonete"
    assert called_product.categoria == "Higiene"
    assert called_product.preco_promocional == 4.0


def test_execute_raises_ProductNotFound_when_product_does_not_exist():
    repo = Mock(spec=ProductRepository)
    repo.get_by_id.return_value = None

    use_case = EditProductUseCase(repository=repo)

    with pytest.raises(ProductNotFound):
        use_case.execute(
            id=999,
            nome="Qualquer",
            marca=None,
            categoria=None,
            preco=None,
            preco_promocional=None,
        )

    repo.get_by_id.assert_called_once_with(999)
    repo.update.assert_not_called()


def test_execute_propagates_exceptions_from_repository():
    repo = Mock(spec=ProductRepository)
    repo.get_by_id.side_effect = Exception("db error")

    use_case = EditProductUseCase(repository=repo)

    with pytest.raises(Exception):
        use_case.execute(
            id=1,
            nome=None,
            marca="X",
            categoria=None,
            preco=None,
            preco_promocional=None,
        )

    repo.get_by_id.assert_called_once_with(1)
    repo.update.assert_not_called()
