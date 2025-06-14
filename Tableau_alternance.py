import sqlite3
import csv
from curl_url import sauvegarder_page_web_curl
import parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "BDD_alternance.db"
csv_file_path = BASE_DIR / "données_de_base.csv"
curl_folder = BASE_DIR / "curl_url"
curl_folder.mkdir(exist_ok=True)



def creer_table_si_absente(db_path):
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alternance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise TEXT,
            url TEXT,
            sauvegarde_locale TEXT,
            date_candidature TEXT,
            retour_oui_ou_non TEXT,
            date_de_retour TEXT,
            commentaire TEXT
        )
    """)
    con.commit()
    con.close()

def importer_csv_si_table_vide(csv_file_path, db_path):
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM alternance")
    nb = cur.fetchone()[0]
    if nb == 0:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute('''INSERT INTO alternance
                    (entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (row['entreprise'], row['url'], row['sauvegarde_locale'], row['date_candidature'],
                     row['retour_oui_ou_non'], row['date_de_retour'], row['commentaire']))
        con.commit()
        print("Base de donnée initialisée avec le CSV.")
    con.close()

def recuperer_url():
    url = input("Indiquez l'url de la page à sauvegarder : ")
    nom_fichier = input("Indiquez le nom du fichier de sauvegarde : ")
    dossier = str(curl_folder)
    chemin_local = sauvegarder_page_web_curl(url, dossier, nom_fichier)
    print("Page sauvegardée localement à :", chemin_local)
    return url, chemin_local

def demander_date_candidature():
    while True:
        date = input("Entrez la date de candidature (JJ/MM/AAAA) : ")
        result = parse.parse("{:d}/{:d}/{:d}", date)
        if result and len(date) == 10:
            jour, mois, annee = result
            if 1 <= jour <= 31 and 1 <= mois <= 12 and 1900 <= annee <= 2100:
                return date
        print("Format invalide. Veuillez entrer la date au format JJ/MM/AAAA.")

def demander_oui_non():
    while True:
        reponse = input("Le retour est-il positif ? (oui/non/attente) : ").strip().lower()
        if reponse in ["oui", "non", "attente"]:
            return reponse
        else:
            print("Réponse invalide. Veuillez taper 'oui' ou 'non' ou 'attente'.")

def demander_date_retour(retour_oui_non):
    if retour_oui_non in ["oui","non"]:
        while True:
            date = input("Entrez la date de retour (JJ/MM/AAAA) : ")
            result = parse.parse("{:d}/{:d}/{:d}", date)
            if result and len(date) == 10:
                jour, mois, annee = result
                if 1 <= jour <= 31 and 1 <= mois <= 12 and 1900 <= annee <= 2100:
                    return date
            print("Format invalide. Veuillez entrer la date au format JJ/MM/AAAA.")
    else:
        return "Néant"

def nouvelle_entree_tableau():
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    # La table existe déjà, pas besoin de la créer ici
    entreprise = input("Entrez le nom de l'entreprise : ")
    url, sauvegarde_locale = recuperer_url()
    date_candidature = demander_date_candidature()
    retour_oui_ou_non = demander_oui_non()
    date_de_retour = demander_date_retour(retour_oui_ou_non)
    commentaire = input("Ajoutez un commentaire : ")
    cur.execute('''INSERT INTO alternance (
        entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire)
    VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire))
    con.commit()
    print("Nouvelle entrée ajoutée avec succès.")
    con.close()
    Home()

def afficher_table():
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("SELECT * FROM alternance")
    tableau = cur.fetchall()
    print("Entreprise | URL | Sauvegarde locale | Date de candidature | Retour | Date de retour | Commentaire")
    print("-" * 110)
    for table in tableau:
        entreprise, url, sauvegarde_locale, date_candidature, retour_oui_ou_non, date_de_retour, commentaire = table
        print(f"{entreprise} | {url} | {sauvegarde_locale} | {date_candidature} | {retour_oui_ou_non} | {date_de_retour} | {commentaire}")
    con.close()
    Home()

def Home():
    print("Bienvenue dans le tableau de suivi de recherche d'alternance !")
    print("1. Ajouter une nouvelle entrée")
    print("2. Afficher le tableau")
    print("3. Quitter")
    choix = input("Veuillez choisir une option (1, 2 ou 3) : ")
    if choix == "1":
        nouvelle_entree_tableau()
    elif choix == "2":
        afficher_table()
    elif choix == "3":
        print("Merci d'avoir utilisé le tableau de suivi. Au revoir !")
        raise SystemExit
    else:
        print("Choix invalide, veuillez réessayer.")
        Home()


if __name__ == "__main__":
    creer_table_si_absente(str(db_path))
    importer_csv_si_table_vide(str(csv_file_path), str(db_path))
    Home()


