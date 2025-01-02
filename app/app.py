from flask import Flask
from app.extensions import db, ma
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    #app.config.from_object('app.config')

    #db.init_app(app)
    #ma.init_app(app)

    register_routes(app)

    return app
