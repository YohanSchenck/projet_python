# Projet Python

```bash
Request URL:
https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.202403.csv.gz
Request Method:
GET
Status Code:
200 OK (from disk cache)
Remote Address:
137.129.43.49:443
Referrer Policy:
strict-origin-when-cross-origin
```

Démarche :

- Passer une requête GET à l'url donné
- Stocker en mémoire le fichier d'archive (format .gz)
- Dézipper le fichier et extraire le .csv à l'intérieur (le nom du fichier dans l'archive sera synop.202401.csv)
- Enregistrer le fichier dans un dossier csv qu'on créera si inexistant
