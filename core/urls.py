from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # maintenant la racine redirige vers login
    path('home/', views.home_view, name='home'),  # l’accueil devient /home/
    path('logout/', views.logout_view, name='logout'),
    path('convertir_image/', views.convertir_image, name='convertir_image'),
]
