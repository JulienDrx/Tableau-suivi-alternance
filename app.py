from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path
from Tableau_alternance import creer_table_si_absente
from curl_url import sauvegarder_page_web_curl
import webbrowser
import threading
import sys
import time
import os
import tempfile
import tkinter as tk
from tkinter import filedialog

# === Demander le chemin de la base uniquement au premier lancement ===

CONFIG_FILE =Path("db_config.txt")

def demande_chemin_bdd():
    root = tk.Tk()
    root.withdraw()
    fichier = filedialog.asksaveasfilename(
        title="Où souhaitez-vous enregistrer la base de données ?",
        defaultextension=".db",
        filetypes=[("Base SQL", "*.db")],
        initialfile="BDD_alternance.db"
    )
    return Path(fichier) if fichier else None

if CONFIG_FILE.exists():
    chemin_str = CONFIG_FILE.read_text(encoding ="utf-8").strip()
    db_path = Path(chemin_str)
    if not db_path.exists():
        print(f"Le fichier de base de données {db_path} n'existe pas. Veuillez le recréer.")
        db_path = None
else : 
    db_path = None

if not db_path:
    chemin = demande_chemin_bdd()
    if not chemin:
        print("Aucun fichier sélectionné. Fermeture")
        exit() 

    chemin.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(str(chemin), encoding="utf-8")
    db_path = chemin






# === Lancer l'app Flask ===
template_folder = Path(__file__).parent / "templates"
app = Flask(__name__, template_folder=str(template_folder))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entreprise = request.form['entreprise']
        url = request.form['url']
        nom_fichier = request.form['nom_fichier']
        sauvegarde_locale = sauvegarder_page_web_curl(url, str(Path("pages_enregistrées")), nom_fichier)
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']

        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        cur.execute('''INSERT INTO alternance (
            entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire))
        con.commit()
        con.close()
        return redirect('/')

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("SELECT * FROM alternance")
    tableau = cur.fetchall()
    con.close()
    return render_template('tableau.html', tableau=tableau)

@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    if request.method == 'POST':
        entreprise = request.form['entreprise']
        url = request.form['url']
        nom_fichier = request.form['nom_fichier']
        sauvegarde_locale = sauvegarder_page_web_curl(url, str(Path("pages_enregistrées")), nom_fichier)
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']

        cur.execute('''UPDATE alternance SET 
            entreprise=?, url=?, sauvegarde_locale=?, date_candidature=?, 
            retour_oui_ou_non=?, date_de_retour=?, commentaire=?
            WHERE id=?''',
            (entreprise, url, sauvegarde_locale, date_candidature, 
             retour_oui_ou_non, date_de_retour, commentaire, id))
        con.commit()
        con.close()
        return redirect('/')
    else:
        cur.execute("SELECT * FROM alternance WHERE id=?", (id,))
        ligne = cur.fetchone()
        con.close()
        return render_template('modifier.html', ligne=ligne)

_browser_opened = False
_browser_lock = threading.Lock()

# === Lancement automatique ===
def open_browser():
    global _browser_opened
    print("attente ouverture navigateur")
    time.sleep(1)
    with _browser_lock:
        if not _browser_opened:
            print("Ouverture du navigateur")
            webbrowser.open_new("http://127.0.0.1:5000")
            _browser_opened = True
        else:
            print("Navigateur déjà ouvert, pas besoin de le rouvrir.")

def run_app():
    print("Lancement de l'application Flask")
    app.run(debug=False, use_reloader=False)

if __name__ == '__main__':
    creer_table_si_absente(db_path)
    threading.Thread(target=run_app).start()
    open_browser()
    while True:
        time.sleep(1)
