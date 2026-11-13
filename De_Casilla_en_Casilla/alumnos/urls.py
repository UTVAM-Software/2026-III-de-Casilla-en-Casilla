from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('panel/', views.panel_alumnos, name='panel'),
    path('equipo/nuevo/', views.crear_equipo, name='crear_equipo'),
    path('alumno/nuevo/', views.crear_alumno, name='crear_alumno'),
]