from app import create_app
import config

app = create_app()

if __name__ == "__main__":
    app.run(debug=True , port=config.Config.FLASK_RUN_PORT)
