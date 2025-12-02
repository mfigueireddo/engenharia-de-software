from unittest.mock import Mock

from src.core.entities.product import Product
from src.core.use_cases.add_product import AddProductUseCase
from src.core.interfaces.product_repository import ProductRepository


def test_execute_adds_product_with_promotional_price_and_returns_repository_result():
    repo = Mock(spec=ProductRepository)
    returned_product = Product(
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=5.0,
        preco_promocional=4.0,
    )
    repo.add.return_value = returned_product

    use_case = AddProductUseCase(repository=repo)

    result = use_case.execute(
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=5.0,
        preco_promocional=4.0,
    )

    assert result is returned_product
    repo.add.assert_called_once()

    added_product_arg = repo.add.call_args.args[0]
    assert isinstance(added_product_arg, Product)
    assert added_product_arg.nome == "Sabonete"
    assert added_product_arg.marca == "MarcaX"
    assert added_product_arg.categoria == "Higiene"
    assert added_product_arg.preco == 5.0
    assert added_product_arg.preco_promocional == 4.0


def test_execute_adds_product_without_promotional_price():
    repo = Mock(spec=ProductRepository)
    returned_product = Product(
        nome="Arroz",
        marca="MarcaY",
        categoria="Alimentos",
        preco=10.0,
        preco_promocional=None,
    )
    repo.add.return_value = returned_product

    use_case = AddProductUseCase(repository=repo)

    result = use_case.execute(
        nome="Arroz",
        marca="MarcaY",
        categoria="Alimentos",
        preco=10.0,
        preco_promocional=None,
    )

    assert result is returned_product
    repo.add.assert_called_once()

    added_product_arg = repo.add.call_args.args[0]
    assert isinstance(added_product_arg, Product)
    assert added_product_arg.nome == "Arroz"
    assert added_product_arg.preco_promocional is None
def test_execute_propagates_exceptions_from_repository():
    repo = Mock(spec=ProductRepository)
    repo.add.side_effect = Exception("db error")

    use_case = AddProductUseCase(repository=repo)

    try:
        use_case.execute(
            nome="Feijão",
            marca="MarcaZ",
            categoria="Alimentos",
            preco=8.0,
            preco_promocional=None,
        )
    except Exception as e:
        assert str(e) == "db error"

    repo.add.assert_called_once()

    added_product_arg = repo.add.call_args.args[0]
    assert isinstance(added_product_arg, Product)   
    assert added_product_arg.nome == "Feijão"
    assert added_product_arg.marca == "MarcaZ"  

def test_execute_adds_product_with_zero_promotional_price():
    repo = Mock(spec=ProductRepository)
    returned_product = Product(
        nome="Pasta de Dente",
        marca="MarcaA",
        categoria="Higiene",
        preco=7.0,
        preco_promocional=0.0,
    )
    repo.add.return_value = returned_product

    use_case = AddProductUseCase(repository=repo)

    result = use_case.execute(
        nome="Pasta de Dente",
        marca="MarcaA",
        categoria="Higiene",
        preco=7.0,
        preco_promocional=0.0,
    )

    assert result is returned_product
    repo.add.assert_called_once()

    added_product_arg = repo.add.call_args.args[0]
    assert isinstance(added_product_arg, Product)
    assert added_product_arg.nome == "Pasta de Dente"
    assert added_product_arg.preco_promocional == 0.0
