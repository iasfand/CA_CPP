from flask import Flask, render_template
from app.routes.main import main
from app.routes.auth import auth
from app.routes.airport import airport

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.secret_key = app.config["SESSION_SECRET"]

    # Register routes
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(airport)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", title="Page Not Found", message="The page you are looking for does not exist."), 404

    return app
