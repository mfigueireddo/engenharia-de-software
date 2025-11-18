from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI
from src.app.dependencies import (
    get_add_product_use_case,
    get_delete_product_use_case,
    get_env_config_service,
    get_get_product_use_case,
    get_health_check_use_case,
    get_list_products_use_case,
    get_edit_product_use_case
)
from src.app.routes import (
    register_docs_routes,
    register_health_routes,
    register_product_routes,
    register_pages_routes # Temporário
)
from src.infra.logging import configure_logging

config_service = get_env_config_service()

info = Info(
    title=config_service.get_service_name(),
    version=config_service.get_service_version(),
)
import os
tempBASE_DIR = os.path.dirname(os.path.abspath(__file__))
tempTEMPLATES_DIR = os.path.join(tempBASE_DIR, "../../../client/templates")
tempSTATIC_DIR = os.path.join(tempBASE_DIR, "../../../client/static")

def create_app() -> OpenAPI:
    configure_logging()
    application = OpenAPI(
        __name__, 
        info=info,
        template_folder=tempTEMPLATES_DIR,
        static_folder=tempSTATIC_DIR, 
        )
    CORS(application)

    register_docs_routes(application)
    register_product_routes(
        application,
        add_use_case=get_add_product_use_case(),
        list_use_case=get_list_products_use_case(),
        get_use_case=get_get_product_use_case(),
        delete_use_case=get_delete_product_use_case(),
        edit_use_case= get_edit_product_use_case()
    )
    register_pages_routes(application) # Temporário
    register_health_routes(application, get_health_check_use_case())

    return application

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)