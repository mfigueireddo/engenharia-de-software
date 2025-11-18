from typing import List

from src.core.entities.product import Product
from src.infra.db.models.product_model import ProductModel

def to_domain(model: ProductModel) -> Product:
    return Product(
        id=model.id,
        nome=model.nome,
        marca=model.marca,
        categoria=model.categoria,
        preco=model.preco,
        preco_promocional=model.preco_promocional,
        data_insercao=model.data_insercao,
    )


def to_domain_list(models: List[ProductModel]) -> List[Product]:
    return [to_domain(model) for model in models]
