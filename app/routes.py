from app.controllers.process_controller import process_bp
from app.controllers.auth_controller import auth_bp

def register_routes(app):
    app.register_blueprint(process_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
