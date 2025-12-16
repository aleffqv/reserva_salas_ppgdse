from django.urls import path
from . import views

urlpatterns = [
    # Calendário e visualização
    path('', views.calendario_view, name='calendario'),
    path('sala/<int:sala_id>/', views.sala_detalhes_view, name='sala_detalhes'),
    
    # Reservas
    path('reserva/nova/', views.criar_reserva_view, name='criar_reserva'),
    path('reserva/<int:reserva_id>/editar/', views.editar_reserva_view, name='editar_reserva'),
    path('reserva/<int:reserva_id>/excluir/', views.excluir_reserva_view, name='excluir_reserva'),
    path('minhas-reservas/', views.minhas_reservas_view, name='minhas_reservas'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
]
