from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Definimos los roles disponibles
    ROLES = (
        ('admin', 'Administrador'),
        ('maestro', 'Maestro'),
        ('usuario', 'Usuario'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"