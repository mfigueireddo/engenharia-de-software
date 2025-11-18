from typing import Callable, List, Optional

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from src.core.entities.product import Product
from src.core.interfaces.product_repository import ProductRepository
from src.infra.db.models.product_model import ProductModel
from src.infra.mappers import product_mapper


class SqlAlchemyProductRepository(ProductRepository):
    """SQLAlchemy implementation of the product repository port."""

    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def add(self, product: Product) -> Product:
        session = self._session_factory()
        try:
            model = ProductModel(
                nome=product.nome,
                marca=product.marca,
                categoria=product.categoria,
                preco=product.preco,
                preco_promocional=product.preco_promocional,
                data_insercao=product.data_insercao,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return product_mapper.to_domain(model)
        except IntegrityError:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_all(self) -> List[Product]:
        session = self._session_factory()
        try:
            models = session.query(ProductModel).all()
            return product_mapper.to_domain_list(models)
        finally:
            session.close()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        session = self._session_factory()
        try:
            model = (
                session.query(ProductModel)
                .filter(ProductModel.id == product_id)
                .first()
            )
            return product_mapper.to_domain(model) if model else None
        finally:
            session.close()

    def get_by_name(self, name: str) -> Optional[Product]:
        session = self._session_factory()
        try:
            model = (
                session.query(ProductModel)
                .filter(ProductModel.nome == name)
                .first()
            )
            return product_mapper.to_domain(model) if model else None
        finally:
            session.close()

    def delete_by_name(self, name: str) -> bool:
        session = self._session_factory()
        try:
            count = (
                session.query(ProductModel)
                .filter(ProductModel.nome == name)
                .delete()
            )
            session.commit()
            return bool(count)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            
    def update(self, product_id: int, product: Product) -> Product:
        """Atualiza os dados de um produto existente pelo ID."""
        session = self._session_factory()
        try:
            # Busca o produto existente pelo ID
            model = (
                session.query(ProductModel)
                .filter_by(id=product_id)
                .first()
            )

            if not model:
                raise NoResultFound(f"Produto com ID {product_id} não encontrado.")

            # Atualiza apenas os campos informados
            if product.nome is not None:
                model.nome = product.nome
            if product.marca is not None:
                model.marca = product.marca
            if product.categoria is not None:
                model.categoria = product.categoria
            if product.preco is not None:
                model.preco = product.preco
            if product.valor is not None:
                model.preco_promocional = product.preco_promocional

            session.commit()
            session.refresh(model)

            # Retorna o domínio atualizado
            return product_mapper.to_domain(model)

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


