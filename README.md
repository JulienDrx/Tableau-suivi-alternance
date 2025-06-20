# 📊 Tableau de suivi de recherche d'alternance

Ce projet est une application **web** (et **console**) permettant de suivre efficacement tes candidatures à des offres d'alternance.  
Elle s'appuie sur **Flask**, **SQLite**, et enregistre localement une copie des pages via `curl`.

---

## 🚀 Fonctionnalités

- ✅ Ajout de candidatures via formulaire web
- 📋 Affichage dans un tableau web interactif
- 💾 Base de données SQLite **persistante et personnalisée**
- 📂 Emplacement de la base mémorisé automatiquement (`db_config.txt`)
- 🌐 Sauvegarde automatique des pages d'offres (via `curl`)
- 🧱 Application compilable en `.exe` avec PyInstaller
- 🖥️ Interface console en option

---

## 🧰 Technologies utilisées

- Python 3
- Flask
- SQLite3
- HTML (Jinja2)
- `curl` via subprocess
- `tkinter` pour la sélection de fichiers

---

## 📁 Structure du projet

```
Tableau-suivi-alternance/
├── app.py                  # Application web Flask
├── Tableau_alternance.py   # Interface console & logique DB
├── curl_url.py             # Sauvegarde de pages HTML (curl)
├── templates/              # HTML (Flask)
├── static/                 # CSS
├── .gitignore              # Fichiers ignorés par Git
├── db_config.txt           # 📌 Chemin de la base (non suivi par Git)
├── build.bat               # Script pour recompiler l'application
└── README.md               # Documentation
```

---

## 🗃️ Système de base de données persistante

Lors du premier lancement, l'application vous demandera **où enregistrer la base SQLite**.  
Ce chemin est mémorisé dans un fichier `db_config.txt`, et **réutilisé automatiquement à chaque lancement**.

> Si vous supprimez ce fichier, l'application vous redemandera le chemin.

---

## ▶️ Lancer l'application Web

```bash
git clone https://github.com/JulienDrx/Tableau-suivi-alternance.git
cd Tableau-suivi-alternance

python -m venv env
env\Scripts\activate
pip install -r requirements.txt

python app.py
```

---

## 🧱 Compiler en .exe

```bash
pyinstaller --onefile --console ^
--add-data "templates;templates" ^
--add-data "static;static" ^
app.py
```

Le `.exe` sera généré dans `dist/app.exe`

---

## 🙋 Auteur

- [JulienDrx](https://github.com/JulienDrx)