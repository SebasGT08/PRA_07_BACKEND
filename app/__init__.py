from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Habilita CORS para todos los dominios en todas las rutas
    CORS(app)

    # Registrar blueprints (rutas)
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app