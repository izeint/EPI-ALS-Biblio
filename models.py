from extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------
# Modèle Livre
# ---------------------------
class Livre(db.Model):
    __tablename__ = "livre"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(100))
    annee = db.Column(db.Integer)
    isbn = db.Column(db.String(50))

    # Relation avec les emprunts
    emprunts = db.relationship("Emprunt", backref="livre", lazy=True)

    def __repr__(self):
        return f"<Livre {self.titre}>"


# ---------------------------
# Modèle Utilisateur
# ---------------------------
class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'etudiant', 'enseignant', 'bibliothecaire'

    # Champs spécifiques selon rôle
    # Étudiant
    matricule = db.Column(db.String(50))
    filiere = db.Column(db.String(100))
    niveau = db.Column(db.String(50))

    # Enseignant
    specialite = db.Column(db.String(100))

    # Bibliothécaire
    mot_de_passe_hash = db.Column(db.String(128))
    horaires = db.Column(db.String(100))

    # Relations
    emprunts = db.relationship("Emprunt", backref="emprunteur", lazy=True, foreign_keys='Emprunt.utilisateur_id')
    validations = db.relationship("Emprunt", backref="bibliothecaire", lazy=True, foreign_keys='Emprunt.bibliothecaire_id')

    def __repr__(self):
        return f"<Utilisateur {self.nom} {self.prenom} ({self.role})>"

    # Méthodes pour les mots de passe (bibliothécaires)
    def set_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def check_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)


# ---------------------------
# Modèle Emprunt
# ---------------------------
class Emprunt(db.Model):
    __tablename__ = "emprunt"

    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    bibliothecaire_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)

    date_emprunt = db.Column(db.DateTime, default=datetime.utcnow)
    date_retour = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))

    def __repr__(self):
        return f"<Emprunt Livre:{self.livre.titre} par {self.emprunteur.nom} {self.emprunteur.prenom}>"

