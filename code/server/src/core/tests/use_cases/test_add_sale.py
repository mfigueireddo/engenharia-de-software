import pytest
from unittest.mock import Mock

from src.core.entities.product import Product
from src.core.entities.sale import Sale, SaleItem
from src.core.interfaces.sale_repository import SaleRepository
from src.core.interfaces.product_repository import ProductRepository
from src.core.use_cases.add_sale import AddSaleUseCase
from src.core.exceptions import ProductNotFound


def test_execute_adds_sale_and_returns_repository_result():
    sale_repo = Mock(spec=SaleRepository)
    product_repo = Mock(spec=ProductRepository)

    product = Product(
        id=1,
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=10.0,
        preco_promocional=8.0,
    )
    product_repo.get_by_id.return_value = product

    returned_sale = Mock(spec=Sale)
    sale_repo.add.return_value = returned_sale

    use_case = AddSaleUseCase(
        sale_repository=sale_repo,
        product_repository=product_repo,
    )

    result = use_case.execute(
        items_data=[{"product_id": 1, "quantity": 2}],
    )

    assert result is returned_sale

    product_repo.get_by_id.assert_called_once_with(1)
    sale_repo.add.assert_called_once()

    added_sale_arg = sale_repo.add.call_args.args[0]
    assert isinstance(added_sale_arg, Sale)
    assert added_sale_arg.total_amount == pytest.approx(2 * 8.0)

    assert len(added_sale_arg.items) == 1
    item: SaleItem = added_sale_arg.items[0]
    assert isinstance(item, SaleItem)
    assert item.product_id == product.id
    assert item.product_name == product.nome
    assert item.quantity == 2
    assert item.unit_price == 8.0 
    assert item.total_price == pytest.approx(16.0)


def test_execute_uses_regular_price_when_no_promotional_price():
    sale_repo = Mock(spec=SaleRepository)
    product_repo = Mock(spec=ProductRepository)

    product = Product(
        id=2,
        nome="Arroz",
        marca="MarcaY",
        categoria="Alimentos",
        preco=5.0,
        preco_promocional=None,
    )
    product_repo.get_by_id.return_value = product
    sale_repo.add.return_value = Mock(spec=Sale)

    use_case = AddSaleUseCase(
        sale_repository=sale_repo,
        product_repository=product_repo,
    )

    use_case.execute(items_data=[{"product_id": 2, "quantity": 3}])

    sale_repo.add.assert_called_once()
    added_sale_arg = sale_repo.add.call_args.args[0]

    assert added_sale_arg.total_amount == pytest.approx(3 * 5.0)
    assert len(added_sale_arg.items) == 1
    item: SaleItem = added_sale_arg.items[0]
    assert item.unit_price == 5.0
    assert item.total_price == pytest.approx(15.0)


def test_execute_raises_ProductNotFound_when_product_not_found():
    sale_repo = Mock(spec=SaleRepository)
    product_repo = Mock(spec=ProductRepository)

    product_repo.get_by_id.return_value = None

    use_case = AddSaleUseCase(
        sale_repository=sale_repo,
        product_repository=product_repo,
    )

    with pytest.raises(ProductNotFound):
        use_case.execute(items_data=[{"product_id": 999, "quantity": 1}])

    product_repo.get_by_id.assert_called_once_with(999)
    sale_repo.add.assert_not_called()


def test_execute_propagates_exceptions_from_sale_repository():
    sale_repo = Mock(spec=SaleRepository)
    product_repo = Mock(spec=ProductRepository)

    product = Product(
        id=3,
        nome="Feijão",
        marca="MarcaZ",
        categoria="Alimentos",
        preco=7.0,
        preco_promocional=None,
    )
    product_repo.get_by_id.return_value = product

    sale_repo.add.side_effect = Exception("db error")

    use_case = AddSaleUseCase(
        sale_repository=sale_repo,
        product_repository=product_repo,
    )

    with pytest.raises(Exception):
        use_case.execute(items_data=[{"product_id": 3, "quantity": 2}])

    product_repo.get_by_id.assert_called_once_with(3)
    sale_repo.add.assert_called_once()
