from functools import lru_cache

from src.infra.db import SessionLocal
from src.core.config import EnvConfigService

from src.core.use_cases.health_check import HealthCheckUseCase

# ======= Produtos =======
from src.infra.repositories import SqlAlchemyProductRepository
from src.core.use_cases.add_product import AddProductUseCase
from src.core.use_cases.get_product import GetProductUseCase
from src.core.use_cases.edit_product import EditProductUseCase
from src.core.use_cases.list_products import ListProductsUseCase
from src.core.use_cases.delete_product import DeleteProductUseCase

# ======= Vendas =======
from src.infra.repositories.sqlalchemy_sale_repository import SqlAlchemySaleRepository
from src.core.use_cases.add_sale import AddSaleUseCase
from src.core.use_cases.get_sale import GetSaleUseCase
from src.core.use_cases.list_sales import ListSalesUseCase
from src.core.use_cases.delete_sale import DeleteSaleUseCase

@lru_cache
def get_env_config_service() -> EnvConfigService:
    return EnvConfigService()

@lru_cache
def get_health_check_use_case() -> HealthCheckUseCase:
    config_service = get_env_config_service()
    return HealthCheckUseCase(
        service_name_provider=config_service.get_service_name,
        service_version_provider=config_service.get_service_version,
    )

# ======= Produtos =======

@lru_cache
def get_product_repository() -> SqlAlchemyProductRepository:
    return SqlAlchemyProductRepository(SessionLocal)

@lru_cache
def get_add_product_use_case() -> AddProductUseCase:
    return AddProductUseCase(get_product_repository())

@lru_cache
def get_get_product_use_case() -> GetProductUseCase:
    return GetProductUseCase(get_product_repository())

@lru_cache
def get_list_products_use_case() -> ListProductsUseCase:
    return ListProductsUseCase(get_product_repository())

@lru_cache
def get_edit_product_use_case() -> EditProductUseCase:
    return EditProductUseCase(get_product_repository())

@lru_cache
def get_delete_product_use_case() -> DeleteProductUseCase:
    return DeleteProductUseCase(get_product_repository())

# ======= Vendas =======

@lru_cache
def get_sale_repository() -> SqlAlchemySaleRepository:
    return SqlAlchemySaleRepository(SessionLocal)

@lru_cache
def get_add_sale_use_case() -> AddSaleUseCase:
    return AddSaleUseCase(get_sale_repository(), get_product_repository())

@lru_cache
def get_get_sale_use_case() -> GetSaleUseCase:
    return GetSaleUseCase(get_sale_repository())

@lru_cache
def get_list_sales_use_case() -> ListSalesUseCase:
    return ListSalesUseCase(get_sale_repository())

@lru_cache
def get_delete_sale_use_case() -> DeleteSaleUseCase:
    return DeleteSaleUseCase(get_sale_repository())