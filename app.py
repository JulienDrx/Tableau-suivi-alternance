from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path
from Tableau_alternance import creer_table_si_absente, importer_csv_si_table_vide
from curl_url import sauvegarder_page_web_curl
import webbrowser
import threading
import sys
import time
import os
import tempfile


if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent.resolve()

db_path = base_path / "BDD_alternance.db"
template_folder = base_path / "templates"

app = Flask(__name__, template_folder=str(template_folder))



@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        entreprise = request.form['entreprise']
        url = request.form['url']
        nom_fichier = request.form['nom_fichier']
        sauvegarde_locale = sauvegarder_page_web_curl(url, str(Path("pages_enregistrées")), nom_fichier)
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']
        # Insertion dans la base
        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        cur.execute('''INSERT INTO alternance (
            entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire))
        con.commit()
        con.close()
        return redirect('/')
    # Affichage du tableau
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

def open_browser():
    global _browser_opened
    print("attente ouverture navigateur")
    time.sleep(3)
    with _browser_lock:
            if not _browser_opened:
                print("Ouverture du navigateur")
                webbrowser.open_new("http://127.0.0.1:5000")
                _browser_opened = True
            else:
                print("Navigateur déjà ouvert, pas besoin de le rouvrir.")





def run_app():
    print("Lancement de l'application Flask")
    app.run(debug=False,use_reloader = False)
    


if __name__ == '__main__':
    creer_table_si_absente(db_path)
    importer_csv_si_table_vide("données_de_base.csv", db_path)

    threading.Thread(target=run_app).start()
    open_browser()

    while True:
        time.sleep(1)
