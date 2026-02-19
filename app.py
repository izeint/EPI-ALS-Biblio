from flask import Flask
from config import Config
from extensions import db
from routes import main
from auth import auth

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)

    # Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Créer les tables
    with app.app_context():
        db.create_all()

    return app

# 🔴 Obligatoire pour gunicorn
app = create_app()

if __name__ == "__main__":
    app.run()
