import requests
import gzip
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

def generate_monthly_dates(start: str, end: str) -> list:
    start_date = datetime.strptime(start, "%Y%m")
    end_date = datetime.strptime(end, "%Y%m")
    
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y%m"))
        if start_date.month == 12:
            start_date = datetime(start_date.year + 1, 1, 1)
        else:
            start_date = datetime(start_date.year, start_date.month + 1, 1)
    
    return dates

json_folder = "./json"
base_url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{date}.csv.gz"
monthly_dates = generate_monthly_dates("199601", datetime.now().strftime("%Y%m"))

for date in monthly_dates:
    url = base_url.format(date=date)
    json_filename = f"synop.{date}.json"
    
    response = requests.get(url)
    print(f"GET {url}")
    
    if response.status_code == 200:
        content = response.content
        try:
            with gzip.open(BytesIO(content), 'rt', encoding='utf-8') as f_mem:
                df = pd.read_csv(f_mem, sep=';')
                df_clean = df[['numer_sta', 'date', 'ff', 't']]
            if not os.path.exists(json_folder):
                os.makedirs(json_folder)
            json_path = os.path.join(json_folder, json_filename)
            df_clean.to_json(json_path, orient='records', lines=True)
            print(f"Fichier {json_filename} enregistré dans le dossier {json_folder}.")
        except gzip.BadGzipFile:
            print("Le contenu téléchargé n'est pas un fichier gzip valide.")
    else:
        print(f"Échec du téléchargement de {url}. Vérifiez l'URL et réessayez.")
