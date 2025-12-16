from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Sala, Reserva


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Administração de usuários customizados"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'telefone', 'setor', 'is_staff', 'pode_reservar']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'setor', 'pode_reservar']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'setor']

    list_editable = ('pode_reservar',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'setor')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'setor')}),
    )


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """Administração de salas"""
    list_display = ['numero', 'cor', 'descricao']
    search_fields = ['numero', 'descricao']
    list_filter = ['cor']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """Administração de reservas"""
    list_display = ['sala', 'usuario', 'dia_semana', 'horario', 'data_criacao']
    list_filter = ['sala', 'dia_semana', 'horario', 'data_criacao']
    search_fields = ['sala__numero', 'usuario__username', 'usuario__first_name', 'usuario__last_name']
    date_hierarchy = 'data_criacao'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando objeto existente
            return ['data_criacao']
        return []
