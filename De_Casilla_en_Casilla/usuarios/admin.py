from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registramos nuestro modelo personalizado para que aparezca en el panel
admin.site.register(Usuario, UserAdmin)