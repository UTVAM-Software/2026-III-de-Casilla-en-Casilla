from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include('game.urls')),
    path('auth/', include('usuarios.urls')),
    path('gestion/', include('alumnos.urls')),
    path('preguntas/', include('preguntas.urls')),
]