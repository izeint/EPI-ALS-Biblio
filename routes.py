# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Livre, Utilisateur, Emprunt
from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)

# -------------------------------
# Page d'accueil
# -------------------------------
@main.route("/")
def index():
    return render_template("index.html")


# -------------------------------
# Login / Register
# -------------------------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        user = Utilisateur.query.filter_by(email=email).first()
        if user and user.check_mot_de_passe(mot_de_passe):
            session["user_id"] = user.id
            session["user_role"] = user.role
            flash("Connexion réussie !", "success")
            return redirect(url_for("main.index"))
        flash("Email ou mot de passe incorrect.", "danger")
    return render_template("login.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        role = request.form.get("role", "etudiant")  # par défaut étudiant

        if Utilisateur.query.filter_by(email=email).first():
            flash("Email déjà utilisé.", "danger")
            return redirect(url_for("main.register"))

        user = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            role=role
        )
        user.set_mot_de_passe(mot_de_passe)
        db.session.add(user)
        db.session.commit()
        flash("Inscription réussie !", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")


@main.route("/logout")
def logout():
    session.clear()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("main.login"))


# -------------------------------
# Gestion des livres
# -------------------------------
@main.route("/livres")
def liste_livres():
    livres = Livre.query.all()
    return render_template("livres/list.html", livres=livres)


@main.route("/livres/ajouter", methods=["GET", "POST"])
def ajouter_livre():
    if request.method == "POST":
        livre = Livre(
            titre=request.form["titre"],
            auteur=request.form["auteur"],
            categorie=request.form.get("categorie"),
            annee=request.form.get("annee"),
            isbn=request.form.get("isbn")
        )
        db.session.add(livre)
        db.session.commit()
        return redirect(url_for("main.liste_livres"))
    return render_template("livres/ajouter.html")


@main.route("/livres/modifier/<int:id>", methods=["GET", "POST"])
def modifier_livre(id):
    livre = Livre.query.get_or_404(id)
    if request.method == "POST":
        livre.titre = request.form["titre"]
        livre.auteur = request.form["auteur"]
        livre.categorie = request.form.get("categorie")
        livre.annee = request.form.get("annee")
        livre.isbn = request.form.get("isbn")
        db.session.commit()
        return redirect(url_for("main.liste_livres"))
    return render_template("livres/modifier.html", livre=livre)


@main.route("/livres/supprimer/<int:id>", methods=["POST"])
def supprimer_livre(id):
    livre = Livre.query.get_or_404(id)
    db.session.delete(livre)
    db.session.commit()
    return redirect(url_for("main.liste_livres"))


# -------------------------------
# Gestion des étudiants
# -------------------------------
@main.route("/etudiants")
def liste_etudiants():
    etudiants = Utilisateur.query.filter_by(role="etudiant").all()
    return render_template("utilisateurs/etudiants/liste.html", etudiants=etudiants)


@main.route("/etudiant/ajouter", methods=["GET", "POST"])
def ajouter_etudiant():
    if request.method == "POST":
        etudiant = Utilisateur(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            email=request.form["email"],
            role="etudiant",
            matricule=request.form.get("matricule"),
            filiere=request.form.get("filiere"),
            niveau=request.form.get("niveau")
        )
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe:
            etudiant.set_mot_de_passe(mot_de_passe)
        db.session.add(etudiant)
        db.session.commit()
        return redirect(url_for("main.liste_etudiants"))
    return render_template("utilisateurs/etudiants/ajouter.html")


@main.route("/etudiant/modifier/<int:id>", methods=["GET", "POST"])
def modifier_etudiant(id):
    etudiant = Utilisateur.query.get_or_404(id)
    if request.method == "POST":
        etudiant.nom = request.form["nom"]
        etudiant.prenom = request.form["prenom"]
        etudiant.email = request.form["email"]
        etudiant.matricule = request.form.get("matricule")
        etudiant.filiere = request.form.get("filiere")
        etudiant.niveau = request.form.get("niveau")
        db.session.commit()
        return redirect(url_for("main.liste_etudiants"))
    return render_template("utilisateurs/etudiants/modifier.html", etudiant=etudiant)


@main.route("/etudiant/supprimer/<int:id>", methods=["POST"])
def supprimer_etudiant(id):
    etudiant = Utilisateur.query.get_or_404(id)
    db.session.delete(etudiant)
    db.session.commit()
    return redirect(url_for("main.liste_etudiants"))


# -------------------------------
# Gestion des enseignants
# -------------------------------
@main.route("/enseignants")
def liste_enseignants():
    enseignants = Utilisateur.query.filter_by(role="enseignant").all()
    return render_template("utilisateurs/enseignants/liste.html", enseignants=enseignants)


@main.route("/enseignant/ajouter", methods=["GET", "POST"])
def ajouter_enseignant():
    if request.method == "POST":
        enseignant = Utilisateur(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            email=request.form["email"],
            role="enseignant",
            specialite=request.form.get("specialite")
        )
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe:
            enseignant.set_mot_de_passe(mot_de_passe)
        db.session.add(enseignant)
        db.session.commit()
        return redirect(url_for("main.liste_enseignants"))
    return render_template("utilisateurs/enseignants/ajouter.html")


@main.route("/enseignant/modifier/<int:id>", methods=["GET", "POST"])
def modifier_enseignant(id):
    enseignant = Utilisateur.query.get_or_404(id)
    if request.method == "POST":
        enseignant.nom = request.form["nom"]
        enseignant.prenom = request.form["prenom"]
        enseignant.email = request.form["email"]
        enseignant.specialite = request.form.get("specialite")
        db.session.commit()
        return redirect(url_for("main.liste_enseignants"))
    return render_template("utilisateurs/enseignants/modifier.html", enseignant=enseignant)


@main.route("/enseignant/supprimer/<int:id>", methods=["POST"])
def supprimer_enseignant(id):
    enseignant = Utilisateur.query.get_or_404(id)
    db.session.delete(enseignant)
    db.session.commit()
    return redirect(url_for("main.liste_enseignants"))


# -------------------------------
# Gestion des bibliothécaires
# -------------------------------
@main.route("/bibliothecaires")
def liste_bibliothecaires():
    bibliothecaires = Utilisateur.query.filter_by(role="bibliothecaire").all()
    return render_template("utilisateurs/bibliothecaires/liste.html", bibliothecaires=bibliothecaires)


@main.route("/bibliothecaire/ajouter", methods=["GET", "POST"])
def ajouter_bibliothecaire():
    if request.method == "POST":
        bibliothecaire = Utilisateur(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            email=request.form["email"],
            role="bibliothecaire",
            horaires=request.form.get("horaires")
        )
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe:
            bibliothecaire.set_mot_de_passe(mot_de_passe)
        db.session.add(bibliothecaire)
        db.session.commit()
        return redirect(url_for("main.liste_bibliothecaires"))
    return render_template("utilisateurs/bibliothecaires/ajouter.html")


@main.route("/bibliothecaire/modifier/<int:id>", methods=["GET", "POST"])
def modifier_bibliothecaire(id):
    bibliothecaire = Utilisateur.query.get_or_404(id)
    if request.method == "POST":
        bibliothecaire.nom = request.form["nom"]
        bibliothecaire.prenom = request.form["prenom"]
        bibliothecaire.email = request.form["email"]
        bibliothecaire.horaires = request.form.get("horaires")
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe:
            bibliothecaire.set_mot_de_passe(mot_de_passe)
        db.session.commit()
        return redirect(url_for("main.liste_bibliothecaires"))
    return render_template("utilisateurs/bibliothecaires/modifier.html", bibliothecaire=bibliothecaire)


@main.route("/bibliothecaire/supprimer/<int:id>", methods=["POST"])
def supprimer_bibliothecaire(id):
    bibliothecaire = Utilisateur.query.get_or_404(id)
    db.session.delete(bibliothecaire)
    db.session.commit()
    return redirect(url_for("main.liste_bibliothecaires"))


# -------------------------------
# Gestion des emprunts
# -------------------------------
@main.route("/emprunts")
def liste_emprunts():
    emprunts = Emprunt.query.all()
    return render_template("emprunt/liste.html", emprunts=emprunts)


@main.route("/emprunt/ajouter", methods=["GET", "POST"])
def ajouter_emprunt():
    livres = Livre.query.all()
    utilisateurs = Utilisateur.query.filter(Utilisateur.role.in_(["etudiant", "enseignant"])).all()
    bibliothecaires = Utilisateur.query.filter_by(role="bibliothecaire").all()

    if request.method == "POST":
        livre_id = request.form["livre_id"]
        utilisateur_id = request.form["utilisateur_id"]
        bibliothecaire_id = request.form["bibliothecaire_id"]

        date_emprunt_str = request.form.get("date_emprunt")
        date_retour_str = request.form.get("date_retour")
        date_emprunt = datetime.strptime(date_emprunt_str, "%Y-%m-%dT%H:%M") if date_emprunt_str else datetime.utcnow()
        date_retour = datetime.strptime(date_retour_str, "%Y-%m-%dT%H:%M") if date_retour_str else datetime.utcnow()

        emprunt = Emprunt(
            livre_id=livre_id,
            utilisateur_id=utilisateur_id,
            bibliothecaire_id=bibliothecaire_id,
            date_emprunt=date_emprunt,
            date_retour=date_retour
        )
        db.session.add(emprunt)
        db.session.commit()
        return redirect(url_for("main.liste_emprunts"))

    return render_template("emprunt/ajouter.html",
                           livres=livres,
                           utilisateurs=utilisateurs,
                           bibliothecaires=bibliothecaires)


@main.route("/emprunt/supprimer/<int:id>", methods=["POST"])
def supprimer_emprunt(id):
    e = Emprunt.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for("main.liste_emprunts"))
