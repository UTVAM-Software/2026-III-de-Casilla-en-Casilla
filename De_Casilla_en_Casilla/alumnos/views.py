from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Avg, Count, F
from django.db import models  
from .models import Equipo, AlumnoTemporal, ProgresoJuego
from .forms import EquipoForm, AlumnoTemporalForm

@login_required
def panel_alumnos(request):
    """Panel principal: muestra equipos, alumnos y estadísticas del profesor actual."""
    equipos = Equipo.objects.filter(creador=request.user)
    alumnos = AlumnoTemporal.objects.filter(creador=request.user)
    
    estadisticas = ProgresoJuego.objects.filter(alumno__creador=request.user).aggregate(
        total_partidas=Count('id'),
        promedio_puntaje=Avg('puntaje'),
        total_completadas=Count('id', filter=models.Q(completada=True))
    )

    context = {
        'equipos': equipos,
        'alumnos': alumnos,
        'estadisticas': estadisticas,
    }
    return render(request, 'alumnos/panel.html', context)

@login_required
@permission_required('alumnos.add_equipo', raise_exception=True)
def crear_equipo(request):
    """Vista para que el profesor registre un nuevo equipo."""
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.creador = request.user
            equipo.save()
            messages.success(request, "Equipo creado exitosamente.")
            return redirect('alumnos:panel')
    else:
        form = EquipoForm()
    
    return render(request, 'alumnos/crear_equipo.html', {'form': form})

@login_required
@permission_required('alumnos.add_alumnotemporal', raise_exception=True)
def crear_alumno(request):
    """Vista para registrar un alumno temporal (sin correo ni contraseña)."""
    if request.method == 'POST':
        form = AlumnoTemporalForm(request.POST, usuario=request.user)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.creador = request.user
            alumno.save()
            messages.success(request, f"Alumno '{alumno.nombre}' registrado con código de acceso: {alumno.codigo_acceso}")
            return redirect('alumnos:panel')
    else:
        form = AlumnoTemporalForm(usuario=request.user)

    return render(request, 'alumnos/crear_alumno.html', {'form': form})