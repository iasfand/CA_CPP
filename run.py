from app import create_app
import config

# Define the application object for Gunicorn
application = create_app()  # Gunicorn looks for "application" by default

if __name__ == "__main__":
    # Only used for local development
    application.run(debug=True, port=config.Config.FLASK_RUN_PORT)
