import random
import string
from django.conf import settings
from django.db import models

def generar_codigo_acceso():
    """Genera un código corto de 6 caracteres para entrada rápida sin contraseña."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=6))

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equipos_creados",
        verbose_name="Profesor / Creador",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.nombre

class AlumnoTemporal(models.Model):
    nombre = models.CharField(max_length=120, verbose_name="Nombre o Alias del Alumno")
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Alumnos",
        verbose_name="Equipo asignado",
    )
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alumnos_temporales_creados",
        verbose_name="Profesor / Creador",
    )
    codigo_acceso = models.CharField(
        max_length=10,
        unique=True,
        default=generar_codigo_acceso,
        verbose_name="Código de acceso rápido",
    )
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alumno Temporal"
        verbose_name_plural = "Alumnos Temporales"
        ordering = ["nombre"]
        permissions = [
            ("view_reporte_progreso", "Puede ver el reporte de progreso de los alumnos"),
        ]

    def __str__(self):
        return f"{self.nombre} [{self.codigo_acceso}]"

class ProgresoJuego(models.Model):
    NIVEL_ALFA = "alfa"
    NIVEL_BETA = "beta"
    NIVELES_CHOICES = [(NIVEL_ALFA, "Alfa"), (NIVEL_BETA, "Beta")]

    alumno = models.ForeignKey(
        AlumnoTemporal,
        on_delete=models.CASCADE,
        related_name="partidas",
        verbose_name="Alumno",
    )
    nivel = models.CharField(
        max_length=10,
        choices=NIVELES_CHOICES,
        default=NIVEL_ALFA,
        verbose_name="Nivel jugado",
    )
    casilla_alcanzada = models.PositiveIntegerField(default=1)
    puntaje = models.PositiveIntegerField(default=0)
    intentos = models.PositiveIntegerField(default=0)
    aciertos = models.PositiveIntegerField(default=0)
    tiempo_segundos = models.PositiveIntegerField(default=0)
    completada = models.BooleanField(default=False)
    fecha_partida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Progreso del Juego"
        verbose_name_plural = "Progresos del Juego"

    @property
    def porcentaje_aciertos(self):
        if self.intentos == 0:
            return 0.0
        return round((self.aciertos / self.intentos) * 100, 1)

    def __str__(self):
        return f"{self.alumno.nombre} - {self.puntaje} pts"