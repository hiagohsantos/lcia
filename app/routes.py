from app.controllers.publish_controller import bp as publish_bp
from app.controllers.auth_controller import bp as auth_bp
from app.controllers.organization_controller import bp as organization_bp

def register_routes(app):
    app.register_blueprint(publish_bp, url_prefix='/api')
    app.register_blueprint(organization_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
