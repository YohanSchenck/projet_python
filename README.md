# Projet Python

## Description du projet
L'idée du projet est de récupérer les données météo France afin de visualiser l'évolution de la température et de la force du vent depuis 1996 sur l'ensemble des stations météorologiques françaises

## Commande pour lancer le serveur

### Création d'un environnement python

```
python -m venv venv
```

### Utilisation de l'environnement

* Windows
```
venv/Scripts\activate
```

* MACOS/ LINUX
```
source venv/bin/activate
```

### Importation des packages nécessaires

```
pip install -r requirements.txt
```

### Lancement du serveur

```
python -m app.main
```

## Couverture des tests

![Alt text](/static/Tests/Coverage.png)
