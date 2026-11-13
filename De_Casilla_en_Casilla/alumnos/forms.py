from django import forms
from .models import Equipo, AlumnoTemporal

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Los Halcones'})
        }

class AlumnoTemporalForm(forms.ModelForm):
    class Meta:
        model = AlumnoTemporal
        fields = ['nombre', 'equipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Alias del alumno (Ej. Ruben)'}),
            'equipo': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['equipo'].queryset = Equipo.objects.filter(creador=usuario)