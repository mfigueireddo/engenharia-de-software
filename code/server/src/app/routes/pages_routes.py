from flask import render_template
from flask_openapi3 import Tag

# ======= Temporário =======

frontend_tag = Tag(name="Frontend", description="Rotas de páginas HTML")

def register_pages_routes(app):
    @app.get("/teste", tags=[frontend_tag])
    def produtos_page():
        return render_template("products.html")