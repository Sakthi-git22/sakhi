from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.routes import main_bp  # Import blueprint
    app.register_blueprint(main_bp)
    return app
