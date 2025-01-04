from flask import Flask
from app.extensions import db, ma
from app.routes import register_routes
from flask_migrate import Migrate

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)

    Migrate(app, db)

    register_routes(app)

    return app
