from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    @app.after_request
    def add_cors_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    swagger = Swagger(app)

    from app.models.user_model import User
    from app.models.session_model import Session

    from .routes import bp
    app.register_blueprint(bp)

    # Optional: create tables if not using migrations (not recommended with migrations)
    # with app.app_context():
    #     db.create_all()

    return app
