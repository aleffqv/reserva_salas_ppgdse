from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Reserva, Usuario, Sala


class ReservaForm(forms.ModelForm):
    """Formulário para criar e editar reservas"""
    
    class Meta:
        model = Reserva
        fields = ['sala', 'dia_semana', 'horario', 'observacoes']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-control'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        dia_semana = cleaned_data.get('dia_semana')
        horario = cleaned_data.get('horario')
        
        if sala and dia_semana and horario:
            # Verificar se já existe reserva para esta sala, dia e horário
            reserva_existente = Reserva.objects.filter(
                sala=sala,
                dia_semana=dia_semana,
                horario=horario
            )
            
            # Se estamos editando, excluir a reserva atual da verificação
            if self.instance.pk:
                reserva_existente = reserva_existente.exclude(pk=self.instance.pk)
            
            if reserva_existente.exists():
                raise forms.ValidationError(
                    f'A {sala} já está reservada para {dict(Reserva.DIAS_SEMANA)[dia_semana]} '
                    f'no horário {dict(Reserva.HORARIOS)[horario]}. '
                    f'Por favor, escolha outro horário ou outra sala.'
                )
        
        return cleaned_data


class UsuarioRegistroForm(UserCreationForm):
    """Formulário para registro de novos usuários"""
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'setor', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
