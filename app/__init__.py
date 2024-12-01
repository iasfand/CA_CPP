from flask import Flask, render_template
from boto3 import session
from app.routes.main import main
from app.routes.auth import auth
from app.routes.airport import airport
from app.utils.filters import format_date

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.secret_key = app.config["SESSION_SECRET"]
    
    app.jinja_env.filters["format_date"] = format_date

    # Initialize the AWS session with the specified profile
    aws_session = session.Session(profile_name=app.config["AWS_PROFILE_NAME"])

    # Initialize the DynamoDB resource using the session
    app.dynamodb = aws_session.resource(
        "dynamodb",
        region_name=app.config["AWS_REGION"]
    )

    # Initialize the DynamoDB table
    app.dynamodb_table = app.dynamodb.Table(app.config["DYNAMODB_TABLE_NAME"])

    # Example usage: Print table name on startup
    print(f"DynamoDB Table: {app.config['DYNAMODB_TABLE_NAME']} initialized.")


    # Register routes
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(airport)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", title="Page Not Found", message="The page you are looking for does not exist."), 404

    return app
