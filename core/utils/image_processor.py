# # core/utils/image_processor.py
# import os
# from PIL import Image, ImageEnhance
# import pytesseract
# from django.conf import settings

# def traiter_image(image_file, output_folder):
#     """
#     Traite une image et retourne le texte extrait par OCR.
#     """
#     os.makedirs(output_folder, exist_ok=True)

#     # Convertir en niveaux de gris
#     image = Image.open(image_file).convert("L")

#     # Remplacement des gris cibles par blanc
#     target_grays = [206, 217]
#     tolerance = 2
#     pixels = image.load()
#     width, height = image.size

#     for x in range(width):
#         for y in range(height):
#             val = pixels[x, y]
#             if any(abs(val - tg) <= tolerance for tg in target_grays):
#                 pixels[x, y] = 250  # Remplace par du blanc

#     # Augmenter le contraste
#     enhancer = ImageEnhance.Contrast(image)
#     image_contrastee = enhancer.enhance(4.0)

#     # OCR avec Tesseract (langue française)
#     texte = pytesseract.image_to_string(image_contrastee, lang='fra')

#     # Sauvegarder le texte dans un fichier
#     base_name = os.path.splitext(image_file.name)[0]
#     texte_file_path = os.path.join(output_folder, f"{base_name}.txt")
#     with open(texte_file_path, 'w', encoding='utf-8') as f:
#         f.write(texte.strip())

#     return texte_file_path, texte.strip()
import logging
from PIL import Image, ImageEnhance
import pytesseract
import os

logger = logging.getLogger(__name__)

def traiter_image(image_file, output_folder):
    """
    Traite une image et retourne le texte extrait par OCR.
    """
    try:
        logger.info("📥 Début du traitement de l'image : %s", image_file.name)

        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(output_folder, exist_ok=True)
        logger.info("📂 Répertoire de sortie : %s", output_folder)

        # Charger l'image et convertir en niveaux de gris
        image = Image.open(image_file).convert("L")
        logger.info("🎨 Image convertie en niveaux de gris.")

        # Remplacement des gris cibles par blanc
        target_grays = [206, 217]
        tolerance = 2
        pixels = image.load()
        width, height = image.size
        logger.info("🖌️ Taille de l'image : %dx%d", width, height)
        logger.info("🔍 Remplacement des gris cibles (%s) avec une tolérance de %d.", target_grays, tolerance)

        count_replacements = 0
        for x in range(width):
            for y in range(height):
                val = pixels[x, y]
                if any(abs(val - tg) <= tolerance for tg in target_grays):
                    pixels[x, y] = 250  # Remplace par du blanc
                    count_replacements += 1
        logger.info("✅ Nombre de pixels remplacés : %d", count_replacements)

        # Augmenter le contraste
        enhancer = ImageEnhance.Contrast(image)
        image_contrastee = enhancer.enhance(4.0)
        logger.info("✨ Contraste augmenté (facteur 4.0).")

        # OCR avec Tesseract (langue française)
        logger.info("📝 Début de l'OCR avec Tesseract (langue: fra).")
        texte = pytesseract.image_to_string(image_contrastee, lang='fra')
        logger.info("✅ OCR terminé. Longueur du texte extrait : %d caractères.", len(texte))

        # Sauvegarder le texte dans un fichier
        base_name = os.path.splitext(image_file.name)[0]
        texte_file_path = os.path.join(output_folder, f"{base_name}.txt")
        with open(texte_file_path, 'w', encoding='utf-8') as f:
            f.write(texte.strip())
        logger.info("💾 Texte sauvegardé dans : %s", texte_file_path)

        logger.info("🎉 Traitement terminé pour l'image : %s", image_file.name)
        return texte_file_path, texte.strip()

    except Exception as e:
        logger.error("❌ Erreur dans traiter_image : %s", e, exc_info=True)
        raise
