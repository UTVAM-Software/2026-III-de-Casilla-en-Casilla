# usuarios/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ADMINISTRADOR = 'admin'
    SOLO_LECTURA = 'lectura'
    CREADOR_USUARIOS = 'creador'
    JUGADOR = 'jugador' 
    
    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (SOLO_LECTURA, 'Solo Lectura'),
        (CREADOR_USUARIOS, 'Creador de Usuarios'),
        (JUGADOR, 'Jugador / Alumno'), 
    ]
    
    rol = models.CharField(
        max_length=15, 
        choices=ROLES_CHOICES, 
        default=JUGADOR 
    )
    
    telefono = models.CharField(max_length=20, null=True, blank=True)