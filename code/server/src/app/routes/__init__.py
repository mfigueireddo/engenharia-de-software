from src.app.routes.docs_routes import register_docs_routes
from src.app.routes.health_routes import register_health_routes
from src.app.routes.product_routes import register_product_routes
from src.app.routes.pages_routes import register_pages_routes

_all__ = [
    "register_docs_routes",
    "register_health_routes",
    "register_product_routes",
    "register_pages_routes"
]
