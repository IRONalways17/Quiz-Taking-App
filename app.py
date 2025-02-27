from flask import Flask
from config import Config
from models import db
from routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprint for routes
    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)