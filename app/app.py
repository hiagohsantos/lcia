from flask import Flask
from app.extensions import db, ma
from app.routes import register_routes
from app.models.organization import Organization
from app.models.apikey import ApiKey
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)
    
    ma.init_app(app)

    register_routes(app)

    return app
