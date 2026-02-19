# app.py
from flask import Flask
from config import Config
from extensions import db
from routes import main
from auth import auth

def create_app():
    """
    Crée et configure l'application Flask.
    """
    # Flask sait où chercher les templates et static files
    app = Flask(
        __name__,
        template_folder="templates",   # dossier des fichiers HTML
        static_folder="static"         # dossier pour CSS, JS, images si tu en as
    )

    # Config
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)

    # Blueprints
    app.register_blueprint(main)  # routes principales
    app.register_blueprint(auth)  # login/register

    # Créer les tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app

# Obligatoire pour gunicorn
app = create_app()

if __name__ == "__main__":
    # Test local
    app.run(host="0.0.0.0", port=5000, debug=True)
