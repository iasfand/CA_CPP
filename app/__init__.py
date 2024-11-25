from flask import Flask
from app.routes.main import main

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Register routes
    app.register_blueprint(main)

    return app
