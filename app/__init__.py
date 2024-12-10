from flask import Flask
from app.database import Base, engine
from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.recommendations import recommendations_bp

def create_app():
    app = Flask(__name__)

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recommendations_bp)

    return app
