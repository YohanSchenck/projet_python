import requests
import gzip
import os
import pandas as pd
from io import BytesIO

url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.202403.csv.gz"
csv_folder = "./csv"
csv_filename = "synop.202403.csv"
response = requests.get(url)

print("Type de contenu:", response.headers.get('Content-Type'))  # Vérifier le type de contenu

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Obtenir le contenu de la réponse
    content = response.content
    
    # Essayer de décompresser le contenu
    try:
        with gzip.GzipFile(fileobj=BytesIO(content), mode='rb') as f_in:
            content = f_in.read()
            
            # Vérifier si le dossier csv existe, sinon le créer
            if not os.path.exists(csv_folder):
                os.makedirs(csv_folder)
            
            # Chemin complet pour enregistrer le fichier CSV
            csv_path = os.path.join(csv_folder, csv_filename)
            
            # Enregistrer le contenu décompressé dans un fichier CSV
            with open(csv_path, "wb") as csv_file:
                csv_file.write(content)
            print(f"Fichier {csv_filename} enregistré dans le dossier {csv_folder}.")
    except gzip.BadGzipFile:
        print("Le fichier téléchargé n'est pas un fichier gzip valide.")
else:
    print("Échec du téléchargement. Vérifiez l'URL et réessayez.")
