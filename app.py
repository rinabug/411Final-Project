import os
from flask import Flask
from dotenv import load_dotenv
from routes.health_routes import health_bp
from routes.auth_routes import auth_bp
from routes.recommendation_routes import recommendation_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recommendation_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
