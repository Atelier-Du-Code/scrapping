# core/utils/image_processor.py
import os
from PIL import Image, ImageEnhance
import pytesseract
from django.conf import settings

def traiter_image(image_file, output_folder):
    """
    Traite une image et retourne le texte extrait par OCR.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Convertir en niveaux de gris
    image = Image.open(image_file).convert("L")

    # Remplacement des gris cibles par blanc
    target_grays = [206, 217]
    tolerance = 2
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            val = pixels[x, y]
            if any(abs(val - tg) <= tolerance for tg in target_grays):
                pixels[x, y] = 250  # Remplace par du blanc

    # Augmenter le contraste
    enhancer = ImageEnhance.Contrast(image)
    image_contrastee = enhancer.enhance(4.0)

    # OCR avec Tesseract (langue française)
    texte = pytesseract.image_to_string(image_contrastee, lang='fra')

    # Sauvegarder le texte dans un fichier
    base_name = os.path.splitext(image_file.name)[0]
    texte_file_path = os.path.join(output_folder, f"{base_name}.txt")
    with open(texte_file_path, 'w', encoding='utf-8') as f:
        f.write(texte.strip())

    return texte_file_path, texte.strip()
