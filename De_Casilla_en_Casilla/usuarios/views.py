from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Usuario

# READ: Muestra la tabla con todos los usuarios
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/lista.html'
    context_object_name = 'usuarios'

# CREATE: Muestra el formulario para crear un usuario nuevo
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'usuarios/formulario.html'
    # Campos que mostraremos en el HTML
    fields = ['username', 'email', 'rol', 'telefono'] 
    success_url = reverse_lazy('lista_usuarios')

# UPDATE: Formulario pre-llenado para editar
class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'usuarios/formulario.html'
    fields = ['username', 'email', 'rol', 'telefono']
    success_url = reverse_lazy('lista_usuarios')

# DELETE: Pantalla de confirmación para borrar
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/confirmar_borrado.html'
    success_url = reverse_lazy('lista_usuarios')