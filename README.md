# OC_Projet9
Openclassrooms - Projet 9 : Développez une application Web en utilisant Django

## Prérequis

- Python 3.10+
- pip

## Installation

Installer pipenv et les requirements  
Documentation pipenv si problème lors de l'installation : [Documentation pipenv](https://pipenv.pypa.io/en/latest/installation.html)
```bash
# install pipenv if needed
pip install pipenv
# clone repo
git clone https://github.com/Masuchotabe/OC_Projet9.git
# go to repo
cd OC_Projet9 
# create env + install requirements 
pipenv install
```
Il faut ensuite créer un fichier .env sur le modèle du fichier .env.template et remplir la secret_Key et la variable de Debug avec True ou False

Activer l'environnement virtuel
```bash
pipenv shell
```
Lancer le serveur

```bash
cd src/
python manage.py runserver
```
Le projet est accessible sur http://127.0.0.1:8000/

## création de données factices
```bash
# Install dev packages
pipenv install --dev 
# create data with images. 
python manage.py fake_data --users 20 --tickets 50 --reviews 80 --with-images
```

## Développement
Utilisation de ruff pour formater et vérifier le suivi de la PEP8
```bash
# format code with ruff. Need to be in /src directory and dev packages installed 
pipenv install --dev
ruff check  
ruff format 
```

## Utilisation
Ce projet est un projet de démonstration. Les fichiers images, stockées dans le dossier /media, est versionné uniquement à titre de démonstration. 
Les utilisateurs sont accessibles dans la base de données. 
Les mots de passes sont ceux configurés dans la commande `fake_data`.




