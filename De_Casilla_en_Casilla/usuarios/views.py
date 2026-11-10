from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Usuario
from .forms import RegistroPublicoForm, UsuarioAdminCreationForm


class VerPanelMixin(UserPassesTestMixin):
    """ Permite ver la lista a Administrador, Solo Lectura y Creador """
    def test_func(self):
        user = self.request.user
        roles_permitidos = [Usuario.ADMINISTRADOR, Usuario.SOLO_LECTURA, Usuario.CREADOR_USUARIOS]
        return user.is_authenticated and (user.rol in roles_permitidos or user.is_superuser)

    def handle_no_permission(self):
        return render(self.request, 'usuarios/403.html', status=403)


class CrearUsuarioMixin(UserPassesTestMixin):
    """ Permite acceder a crear usuarios a Administrador y Creador """
    def test_func(self):
        user = self.request.user
        roles_permitidos = [Usuario.ADMINISTRADOR, Usuario.CREADOR_USUARIOS]
        return user.is_authenticated and (user.rol in roles_permitidos or user.is_superuser)

    def handle_no_permission(self):
        return render(self.request, 'usuarios/403.html', status=403)


class SoloAdminMixin(UserPassesTestMixin):
    """ Exclusivo para el Administrador Mayor (Editar y Borrar) """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.rol == Usuario.ADMINISTRADOR or user.is_superuser)

    def handle_no_permission(self):
        return render(self.request, 'usuarios/403.html', status=403)

class IniciarSesionView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True 

class RegistroUsuarioView(CreateView):
    template_name = 'usuarios/registro.html'
    form_class = RegistroPublicoForm 
    success_url = reverse_lazy('login')

class PanelUsuariosListView(VerPanelMixin, ListView):
    model = Usuario
    template_name = 'usuarios/panel/lista_usuarios.html'
    context_object_name = 'usuarios'

class PanelUsuarioCreateView(CrearUsuarioMixin, CreateView):
    model = Usuario
    template_name = 'usuarios/panel/formulario_usuario.html'
    success_url = reverse_lazy('panel_usuarios_lista')
    def get_form_class(self):
        user = self.request.user
        if user.rol == Usuario.ADMINISTRADOR or user.is_superuser:

            return UsuarioAdminCreationForm
        return RegistroPublicoForm

class PanelUsuarioUpdateView(SoloAdminMixin, UpdateView):
    model = Usuario
    fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
    template_name = 'usuarios/panel/formulario_usuario.html'
    success_url = reverse_lazy('panel_usuarios_lista')

class PanelUsuarioDeleteView(SoloAdminMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/panel/confirmar_borrado.html'
    success_url = reverse_lazy('panel_usuarios_lista')


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'