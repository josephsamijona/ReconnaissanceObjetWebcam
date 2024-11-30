# Utiliser une image Python officielle comme image parent
FROM python:3.11-slim

# Définir les variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Installer les dépendances
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le code de l'application dans le conteneur
COPY . /code/

# Collecter les fichiers statiques


# Exposer le port que l'application va utiliser
EXPOSE 8000

# Commande pour lancer l'application avec Gunicorn
CMD ["gunicorn", "ReconnaissanceObjetWebcam.wsgi:application", "--bind", "0.0.0.0:8000"]
