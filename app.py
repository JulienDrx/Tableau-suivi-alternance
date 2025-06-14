from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path
from Tableau_alternance import creer_table_si_absente, importer_csv_si_table_vide
from curl_url import sauvegarder_page_web_curl

db_path = Path(__file__).resolve().parent / "BDD_alternance.db"

app = Flask(__name__)



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

if __name__ == '__main__':
    creer_table_si_absente(db_path)
    importer_csv_si_table_vide("données_de_base.csv", db_path)
    app.run(debug=True)