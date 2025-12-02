from datetime import datetime
from src.core.entities.product import Product


def test_product_creation_with_all_fields():
    product = Product(
        id=1,
        nome="Sabonete",
        marca="MarcaX",
        categoria="Higiene",
        preco=5.0,
        preco_promocional=4.0,
    )

    assert product.id == 1
    assert product.nome == "Sabonete"
    assert product.marca == "MarcaX"
    assert product.categoria == "Higiene"
    assert product.preco == 5.0
    assert product.preco_promocional == 4.0
    assert isinstance(product.data_insercao, datetime)


def test_product_id_defaults_to_none_when_not_provided():
    product = Product(
        nome="Arroz",
        marca="MarcaY",
        categoria="Alimentos",
        preco=10.0,
        preco_promocional=None,
    )

    assert product.id is None


def test_product_data_insercao_is_set_automatically():
    product = Product(
        nome="Feijão",
        marca="MarcaZ",
        categoria="Alimentos",
        preco=8.0,
        preco_promocional=None,
    )

    assert isinstance(product.data_insercao, datetime)
