import subprocess
import os

def sauvegarder_page_web_curl(url, dossier_sauvegarde, nom_fichier):
    chemin_fichier = os.path.join(dossier_sauvegarde, nom_fichier)
    try:
        # Commande curl pour télécharger la page
        subprocess.run(["curl", "-L", url, "-o", chemin_fichier], check=True)
        print(f"Page sauvegardée : {chemin_fichier}")
        return chemin_fichier
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None

# Exemple d'utilisation :
# url = "https://exemple.com"
# dossier = r"C:\Users\Julie\Desktop\pages_sauvegardees"
# nom_fichier = "exemple.html"
# chemin = sauvegarder_page_web_curl(url, dossier, nom_fichier)