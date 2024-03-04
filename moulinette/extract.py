import requests
import gzip
import os

# URL du fichier à télécharger
url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.202403.csv.gz"

# Emplacement du dossier pour enregistrer le fichier CSV
csv_folder = "csv"

# Nom du fichier CSV à l'intérieur de l'archive
csv_filename = "synop.202403.csv"

# Passer une requête GET à l'URL et télécharger le fichier .gz
response = requests.get(url)

print("Type de contenu:", response.headers.get('Content-Type'))  # Vérifier le type de contenu

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Sauvegarder temporairement le contenu pour inspection
    temp_gz_path = "temp_download.gz"
    with open(temp_gz_path, "wb") as temp_gz:
        temp_gz.write(response.content)
    print(f"Fichier temporaire {temp_gz_path} enregistré.")
    
    # Essayer de décompresser le fichier sauvegardé
    try:
        with gzip.open(temp_gz_path, 'rb') as f_in:
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
