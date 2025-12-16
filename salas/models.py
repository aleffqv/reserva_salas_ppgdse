from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class Usuario(AbstractUser):
    """Modelo customizado de usuário para professores"""
    telefone = models.CharField(max_length=20, blank=True)
    setor = models.CharField(max_length=100, blank=True, verbose_name='Setor/Departamento')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    pode_reservar = models.BooleanField(
        default=False,
        verbose_name="Pode fazer reservas"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Sala(models.Model):
    """Modelo para as salas disponíveis"""
    CORES = [
        ('#FF8C00', 'Laranja'),
        ('#28A745', 'Verde'),
        ('#007BFF', 'Azul'),
    ]
    
    numero = models.CharField(max_length=10, unique=True, verbose_name='Número da Sala')
    cor = models.CharField(max_length=7, choices=CORES, verbose_name='Cor')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['numero']
    
    def __str__(self):
        return f"Sala {self.numero}"


class Reserva(models.Model):
    """Modelo para as reservas de salas"""
    DIAS_SEMANA = [
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
    ]
    
    HORARIOS = [
        ('08:00-12:00', '8h - 12h'),
        ('14:00-18:00', '14h - 18h'),
        ('18:00-22:00', '18h - 22h'),
    ]
    
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA, verbose_name='Dia da Semana')
    horario = models.CharField(max_length=20, choices=HORARIOS, verbose_name='Horário')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['dia_semana', 'horario']
        unique_together = ['sala', 'dia_semana', 'horario']
    
    def __str__(self):
        return f"{self.sala} - {self.get_dia_semana_display()} ({self.get_horario_display()})"
    
    def clean(self):
        """Validação para evitar reservas duplicadas"""
        if self.pk is None:  # Apenas para novas reservas
            if Reserva.objects.filter(
                sala=self.sala,
                dia_semana=self.dia_semana,
                horario=self.horario
            ).exists():
                raise ValidationError(
                    f'A {self.sala} já está reservada para {self.get_dia_semana_display()} '
                    f'no horário {self.get_horario_display()}.'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
