# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Utilisateur
from extensions import db
from flask_login import login_user, logout_user, LoginManager

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Utilisateur.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return redirect(url_for('auth.register'))

        if Utilisateur.query.filter_by(email=email).first():
            flash('Email déjà utilisé', 'danger')
            return redirect(url_for('auth.register'))

        user = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            role='etudiant',  # par défaut
            password=generate_password_hash(password, method='sha256')
        )
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès ! Connectez-vous.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
