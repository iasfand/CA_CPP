from flask import Flask, render_template , request
from boto3 import session
import boto3
import logging
import watchtower
from app.routes.main import main
from app.routes.auth import auth
from app.routes.airport import airport
from app.utils.filters import format_date, format_date_time


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.secret_key = app.config["SESSION_SECRET"]

    # Register custom Jinja2 filters
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["format_date_time"] = format_date_time

    # Initialize the AWS session with the specified profile and region
    aws_session = session.Session(
        profile_name=app.config["AWS_PROFILE_NAME"], 
        region_name=app.config["AWS_REGION"]
    )

    # Set up a default boto3 session for libraries like Watchtower that rely on it
    boto3.setup_default_session(
        profile_name=app.config["AWS_PROFILE_NAME"], 
        region_name=app.config["AWS_REGION"]
    )

    # Initialize the DynamoDB resource using the session
    app.dynamodb = aws_session.resource("dynamodb")

    # Initialize the S3 client using the session
    app.s3_client = aws_session.client("s3")
    print(f"S3 client initialized with profile: {app.config['AWS_PROFILE_NAME']}")

    # Initialize the DynamoDB table
    app.dynamodb_table = app.dynamodb.Table(app.config["DYNAMODB_TABLE_NAME"])
    print(f"DynamoDB Table: {app.config['DYNAMODB_TABLE_NAME']} initialized.")

    # Configure CloudWatch logging
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group="SkyPortLogs",
        stream_name="FlaskAppLogs"
    )
    cloudwatch_handler.setLevel(logging.INFO)
    cloudwatch_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    # Add CloudWatch logging to the app's logger
    app.logger.addHandler(cloudwatch_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("CloudWatch logging initialized.")

    # Register routes
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(airport)

   # Error handling for 404
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"404 Error: {request.url} not found.")
        return render_template(
            "error.html", 
            title="Page Not Found", 
            message="The page you are looking for does not exist."
        ), 404

    return app
