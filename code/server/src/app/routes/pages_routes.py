from flask import render_template
from flask_openapi3 import Tag

frontend_tag = Tag(name="Frontend", description="Rotas de páginas HTML")

def register_pages_routes(app):
    @app.get("/", tags=[frontend_tag])
    def produtos_homepage():
        return render_template("products.html")
    
    @app.get("/page/produtos", tags=[frontend_tag])
    def produtos_page():
        return render_template("products.html")

    @app.get("/page/vendas", tags=[frontend_tag])
    def vendas_page():
        return render_template("sales.html")