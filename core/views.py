from django.shortcuts import render, redirect
from django.conf import settings
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from core.utils.image_processor import traiter_image
import pytesseract
from pathlib import Path
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

base_prompt = "Coucou chat, j'aimerai que tu me corriges ce texte sans reformulation, ni aucun ajout. Ne prends aucune liberté:\n\n"


# Décorateur pour vérifier l'authentification
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# 🏠 Page d'accueil protégée
@login_required
def home_view(request):
    user = request.session.get('user')
    return render(request, "core/home.html", {"user": user})


# 🔑 Page de connexion
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        users = settings.USERS  # Les credentials viennent de settings (via env)

        if username in users and users[username] == password:
            request.session['user'] = username  # Stocke l'utilisateur en session
            return redirect('home')  # Redirige vers la page d'accueil
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect"

    return render(request, "core/login.html", {"error": error})


# 🚪 Déconnexion
def logout_view(request):
    request.session.flush()  # Efface la session
    return redirect('login')


# 📷 OCR : Convertir une image en texte (protégé)
@login_required
@csrf_exempt
def convertir_image(request):
    if request.method == "POST":
        if "image" not in request.FILES:
            return JsonResponse({"success": False, "message": "Aucune image reçue."})

        try:
            image_file = request.FILES["image"]
            output_folder = Path(settings.MEDIA_ROOT) / "ocr_texts"

            # Étape 1 : OCR
            texte_file_path, texte_ocr = traiter_image(image_file, output_folder)

            # Étape 2 : Correction via OpenAI
            prompt = base_prompt + texte_ocr

            # Appel OpenAI
            response = client.responses.create(
                model="gpt-3.5-turbo",
                input=prompt
            )

            texte_corrige = response.output_text

            return JsonResponse({
                "success": True,
                "texte": texte_corrige,
                "logs": [
                    "✅ OCR terminé",
                    "✅ Correction OpenAI terminée"
                ]
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Requête invalide."})
