from typing import Callable, List, Optional

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from src.core.entities.sale import Sale
from src.core.interfaces.sale_repository import SaleRepository
from src.infra.db.models.sale_model import SaleModel, SaleItemModel
from src.infra.mappers import sale_mapper


class SqlAlchemySaleRepository(SaleRepository):
    """SQLAlchemy implementation of the sale repository port."""

    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def add(self, sale: Sale) -> Sale:
        session = self._session_factory()
        try:
            # Cria o modelo principal da venda
            sale_model = SaleModel(
                total_amount=sale.total_amount,
                data_venda=sale.data_venda,
            )
            session.add(sale_model)
            session.flush()  # Pega o ID gerado para a venda
            
            # Cria os itens da venda
            for item in sale.items:
                item_model = SaleItemModel(
                    sale_id=sale_model.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price
                )
                session.add(item_model)
            
            session.commit()
            session.refresh(sale_model)
            return sale_mapper.to_domain(sale_model)
        except IntegrityError:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_all(self) -> List[Sale]:
        session = self._session_factory()
        try:
            models = session.query(SaleModel).all()
            return sale_mapper.to_domain_list(models)
        finally:
            session.close()

    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        session = self._session_factory()
        try:
            model = (
                session.query(SaleModel)
                .filter(SaleModel.id == sale_id)
                .first()
            )
            return sale_mapper.to_domain(model) if model else None
        finally:
            session.close()

    def delete_by_id(self, sale_id: int) -> bool:
        session = self._session_factory()
        try:
            from src.infra.db.models.sale_model import SaleItemModel
            
            # Primeiro deleta todos os itens da venda
            session.query(SaleItemModel).filter(SaleItemModel.sale_id == sale_id).delete()
            
            # Depois deleta a venda principal
            count = (
                session.query(SaleModel)
                .filter(SaleModel.id == sale_id)
                .delete()
            )
            session.commit()
            return bool(count)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()