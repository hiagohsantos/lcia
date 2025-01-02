from app.controllers.process_controller import process_bp

def register_routes(app):
    app.register_blueprint(process_bp, url_prefix='/api/v1')
