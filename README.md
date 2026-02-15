# EPI-ALS-Biblio

**Projet Master 2 – Gestion de Bibliothèque**
Établissement : EPI Niger
Application développée avec **Python (Flask)**, **HTML/CSS** et **SQLite**.

Lien GitHub : [https://github.com/izeint/EPI-ALS-Biblio](https://github.com/izeint/EPI-ALS-Biblio)

---

## 1. Description du projet

EPI-ALS-Biblio est une application web permettant :

* La gestion des utilisateurs (inscription, connexion).
* La gestion des livres (CRUD : création, lecture, modification, suppression).
* L’interface intuitive pour administrateurs et membres.
* Une base de données SQLite pour stocker les informations.

Architecture :

* Front-end : HTML/CSS
* Back-end : Python + Flask
* Base de données : SQLite

---

## 2. Prérequis

* Python 3.10 ou supérieur
* Git installé
* Terminal ou invite de commande
* (Optionnel) Virtualenv

---

## 3. Installation

1. **Cloner le dépôt Git :**

```bash
git clone https://github.com/izeint/EPI-ALS-Biblio.git
cd EPI-ALS-Biblio
```

2. **Créer un environnement virtuel (recommandé) :**

```bash
python -m venv venv
```

3. **Activer l’environnement :**

* Windows :

```bash
venv\Scripts\activate
```

* Linux/Mac :

```bash
source venv/bin/activate
```

4. **Installer les dépendances :**

```bash
pip install -r requirements.txt
```

---

## 4. Lancer l’application

1. Exécuter :

```bash
python app.py
```

2. Ouvrir le navigateur et accéder à :

```
http://127.0.0.1:5000
```

3. Créer un compte ou se connecter.
4. Gérer les livres (CRUD).

---

## 5. Structure du projet

```
EPI-ALS_BIBLIO/
├─ epi-als/
│   ├─ auth.py
│   ├─ routes.py
│   ├─ models.py
│   └─ extensions.py
├─ static/
├─ templates/
├─ app.py
├─ bibliotheque.db
├─ requirements.txt
└─ README.md
```

---

## 6. Fonctionnalités

* **Utilisateur :** Inscription, connexion, consultation des livres.
* **Administrateur :** CRUD complet sur les livres et gestion des utilisateurs.
* **Base de données :** SQLite, toutes les opérations CRUD implémentées.
* **Robustesse :** Gestion des erreurs et validation des formulaires.

---

## 7. Auteur

* Étudiant :  Assoumane Ada Izeinatou

* Établissement : EPI Niger

