# 📊 Tableau de suivi de recherche d'alternance

Ce projet est une application web (et console) qui permet de suivre facilement ses candidatures à des offres d'alternance. Il utilise **Flask**, une base de données **SQLite** et un fichier CSV de démarrage.

---

## 🚀 Fonctionnalités

- Ajout d'une candidature via formulaire web 📝
- Affichage de toutes les candidatures dans un tableau 📋
- Stockage des données dans une base SQLite locale 💾
- Pré-remplissage initial depuis un fichier CSV
- Sauvegarde d'une copie locale de l'offre (via `curl_url.py`)
- Interface console disponible également

---

## 🧰 Technologies utilisées

- Python 3
- Flask
- SQLite3
- HTML (Jinja2 Template)
- CSV

---

## 📁 Structure du projet

```
Tableau-suivi-alternance/
├── app.py                      # Application web Flask
├── Tableau_alternance.py       # Interface console + logique DB/CSV
├── curl_url.py                 # Téléchargement de pages web
├── données_de_base.csv         # Données de base à importer
├── requirements.txt            # Dépendances
├── templates/
│   └── tableau.html            # Template HTML principal
└── BDD_alternance.db           # Base de données générée
```

---

## ▶️ Lancer l'application

### 1. Cloner le projet

```bash
git clone https://github.com/JulienDrx/Tableau-suivi-alternance.git
cd Tableau-suivi-alternance
```

### 2. Installer l'environnement

```bash
python -m venv env
env\Scripts\activate      # Sous Windows
# ou
source env/bin/activate   # Sous macOS/Linux

pip install -r requirements.txt
```

### 3. Lancer le serveur Flask

```bash
python app.py
```

👉 Puis ouvrir : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 💻 Interface console (optionnelle)

```bash
python Tableau_alternance.py
```

---

## 📜 Licence

Ce projet est distribué sous licence **MIT** — libre d’utilisation, de modification et de distribution.

---

## ✨ Contributeur

- [JulienDrx](https://github.com/JulienDrx)

---

# 🇬🇧 English — Internship Application Tracker

This is a bilingual web/console app for tracking internship/job applications. Built with Flask and SQLite, it helps manage your search efficiently.

### ✅ Features

- Add new applications via a form
- Display them in a clean HTML table
- Save locally in SQLite
- Auto-import data from CSV
- Console version also available

### 📦 Tech Stack

- Python 3
- Flask + Jinja2
- SQLite3
- CSV

### 🏁 Getting Started

```bash
git clone https://github.com/JulienDrx/Tableau-suivi-alternance.git
cd Tableau-suivi-alternance
python -m venv env
source env/bin/activate      # or env\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

Enjoy using this tool, and good luck with your internship search!
