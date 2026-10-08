from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsuarioListView.as_view(), name='lista_usuarios'),
    path('nuevo/', views.UsuarioCreateView.as_view(), name='crear_usuario'),
    path('editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('borrar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='borrar_usuario'),
]