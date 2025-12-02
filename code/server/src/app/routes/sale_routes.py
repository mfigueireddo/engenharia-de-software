from flask_openapi3 import Tag
from src.app.schemas.sale import (
    VendaSchema,
    VendaBuscaSchema,
    VendaViewSchema,
    ListagemVendasSchema,
    VendaDelSchema,
    apresenta_venda,
    apresenta_vendas,
)
from src.app.schemas import ErrorSchema
from src.core.exceptions import ProductNotFound
from src.core.use_cases.add_sale import AddSaleUseCase
from src.core.use_cases.list_sales import ListSalesUseCase
from src.core.use_cases.get_sale import GetSaleUseCase
from src.core.use_cases.delete_sale import DeleteSaleUseCase

venda_tag = Tag(
    name="Venda",
    description="Adição, visualização e remoção de vendas à base",
)


def register_sale_routes(
    app,
    add_use_case: AddSaleUseCase,
    list_use_case: ListSalesUseCase,
    get_use_case: GetSaleUseCase,
    delete_use_case: DeleteSaleUseCase,
) -> None:
    
    # ======= Adição =======

    @app.post(
        "/venda",
        tags=[venda_tag],
        responses={"200": VendaViewSchema, "400": ErrorSchema, "404": ErrorSchema}
    )
    def add_venda(body: VendaSchema):
        from flask import request
        try:
            if hasattr(body, 'items'):
                items_data = [{"product_id": item.product_id, "quantity": item.quantity} for item in body.items]
            else:
                json_data = request.get_json()
                if not json_data or 'items' not in json_data:
                    return {"message": "Campo 'items' é obrigatório"}, 400
                
                items_data = [{"product_id": item["product_id"], "quantity": item["quantity"]} for item in json_data["items"]]
            
            venda = add_use_case.execute(items_data)
            return apresenta_venda(venda), 200
        except ProductNotFound as error:
            return {"message": str(error)}, 404
        except Exception as error:
            return {"message": f"Não foi possível criar a venda: {str(error)}"}, 400

    # ======= Obtenção múltipla =======

    @app.get(
        "/vendas",
        tags=[venda_tag],
        responses={"200": ListagemVendasSchema, "404": ErrorSchema},
    )
    def get_vendas():
        vendas = list_use_case.execute()
        if not vendas:
            return {"vendas": []}, 200
        return apresenta_vendas(vendas), 200

    # ======= Obtenção única =======

    @app.get(
        "/venda",
        tags=[venda_tag],
        responses={"200": VendaViewSchema, "404": ErrorSchema},
    )
    def get_venda(query: VendaBuscaSchema):
        try:
            venda = get_use_case.execute(query.id)
            return apresenta_venda(venda), 200
        except Exception as error:
            # Pode ser SaleNotFound ou outro erro
            if "não encontrada" in str(error):
                return {"message": str(error)}, 404
            return {"message": str(error)}, 400

    # ======= Deleção =======

    @app.delete(
        "/venda",
        tags=[venda_tag],
        responses={"200": VendaDelSchema, "404": ErrorSchema},
    )
    def del_venda(query: VendaBuscaSchema):
        try:
            delete_use_case.execute(query.id)
            return {"message": "Venda removida", "id": query.id}, 200
        except Exception as error:
            # Pode ser SaleNotFound ou outro erro
            if "não encontrada" in str(error):
                return {"message": str(error)}, 404
            return {"message": str(error)}, 400