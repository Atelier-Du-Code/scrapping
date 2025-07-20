# Dockerfile

FROM python:3.11-slim

# Installer les dépendances système nécessaires à Tesseract et au build
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    libtesseract-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier requirements et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . /app/

# Collecter les fichiers statiques
# Collecter les fichiers statiques et appliquer les migrations
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput


# Exposer le port 8000 (celui par défaut de gunicorn)
EXPOSE 8000

# Commande pour démarrer gunicorn
CMD ["gunicorn", "webapp.wsgi:application", "--bind", "0.0.0.0:8000"]
