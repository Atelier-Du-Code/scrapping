

# Mettre à jour les paquets système
apt-get update

# Installer Tesseract OCR et le pack de langue français
sudo apt-get install -y tesseract-ocr tesseract-ocr-fra

# Installer les dépendances Python
pip install -r requirements.txt

# Appliquer les migrations Django
python3 manage.py migrate

# Collecter les fichiers statiques
python3 manage.py collectstatic --noinput





# python3 manage.py migrate
# python3 manage.py collectstatic --noinput
