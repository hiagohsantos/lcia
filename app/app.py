from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma
from app.repositories.connection_pool import DatabaseConnectionPool
from app.repositories.seed import seed_data
from app.routes import register_routes
from flask_migrate import Migrate

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)

    Migrate(app, db)

    register_routes(app)

    with app.app_context():
        seed_data() 
        
    return app
