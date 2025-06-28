from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.exts import db


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from app.routes.terrain_routes import terrain_bp
    from app.routes.premium_routes import premium_bp

    app.register_blueprint(terrain_bp, url_prefix='/api')
    app.register_blueprint(premium_bp, url_prefix='/api/premium')


    return app