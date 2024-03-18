# Projet Python

Commande pour lancer le serveur

```
uvicorn app.main:app --reload
```

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

- **(WEBSITE)** Essayer de joindre le site web
- Générer toutes les dates (format : AAAAMM) entre janvier 1996 et la date du jour
- Boucler sur les étapes suivantes pour chaque date :
  - Passer une requête GET à l'url donné
  - Enregistrer en mémoire le fichier d'archive (format .gz)
  - Accéder en mémoire à l'archive pour en faire un csv
  - Accéder en mémoire au csv pour le transformer en json
  - **(temporaire)** Stocker dans une dir json tous les fichiers
  - **(WEBSITE)** Passer une requête POST au site web pour chaque json à envoyer

Activer env :

```bash
.\venv\Scripts\activate
```
