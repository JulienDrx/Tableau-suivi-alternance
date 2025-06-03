from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_PATH = r"C:\Users\Julie\Desktop\fichier_db\BDD_alternance.db"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupération des données du formulaire
        entreprise = request.form['entreprise']
        url = request.form['url']
        sauvegarde_locale = request.form['sauvegarde_locale']
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']
        # Insertion dans la base
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO alternance (
            entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire))
        con.commit()
        con.close()
        return redirect('/')
    # Affichage du tableau
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM alternance")
    tableau = cur.fetchall()
    con.close()
    return render_template('tableau.html', tableau=tableau)

if __name__ == '__main__':
    app.run(debug=True)