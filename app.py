# app.py
from flask import Flask
from config import Config
from extensions import db
from routes import main
from auth import auth  # <-- Blueprint auth pour login/register


def create_app():
    """
    Crée et configure l'application Flask.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation des extensions
    db.init_app(app)

    # Enregistrement des Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app


# 🔴 LIGNE AJOUTÉE POUR GUNICORN (OBLIGATOIRE)
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
