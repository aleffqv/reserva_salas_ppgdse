from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from .models import Sala, Reserva, Usuario
from .forms import ReservaForm, UsuarioRegistroForm


def calendario_view(request):
    """View principal que exibe o calendário de reservas"""
    salas = Sala.objects.all()
    reservas = Reserva.objects.select_related('sala', 'usuario').all()
    
    # Organizar reservas por dia e horário
    calendario = {}
    for dia, dia_nome in Reserva.DIAS_SEMANA:
        calendario[dia] = {}
        for horario, horario_nome in Reserva.HORARIOS:
            calendario[dia][horario] = []
    
    for reserva in reservas:
        calendario[reserva.dia_semana][reserva.horario].append(reserva)
    
    context = {
        'salas': salas,
        'calendario': calendario,
        'dias_semana': Reserva.DIAS_SEMANA,
        'horarios': Reserva.HORARIOS,
    }
    return render(request, 'salas/calendario.html', context)


def sala_detalhes_view(request, sala_id):
    """View para exibir detalhes de uma sala específica (para o pop-up)"""
    sala = get_object_or_404(Sala, id=sala_id)
    reservas = Reserva.objects.filter(sala=sala).select_related('usuario')
    
    # Organizar reservas por dia
    reservas_por_dia = {}
    for dia, dia_nome in Reserva.DIAS_SEMANA:
        reservas_por_dia[dia] = {
            'nome': dia_nome,
            'horarios': {}
        }
        for horario, horario_nome in Reserva.HORARIOS:
            reservas_por_dia[dia]['horarios'][horario] = {
                'nome': horario_nome,
                'reserva': None
            }
    
    for reserva in reservas:
        reservas_por_dia[reserva.dia_semana]['horarios'][reserva.horario]['reserva'] = reserva
    
    context = {
        'sala': sala,
        'reservas_por_dia': reservas_por_dia,
    }
    return render(request, 'salas/sala_detalhes.html', context)


@login_required
def criar_reserva_view(request):
    """View para criar uma nova reserva"""
    
    if request.method == 'POST':
        
        form = ReservaForm(request.POST, usuario=request.user)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            if not request.user.pode_reservar:
                messages.error(
                    request,
                    "Sua conta ainda não foi aprovada por um administrador."
                )
                return redirect('calendario')
            try:
                reserva.save()
                messages.success(request, 'Reserva criada com sucesso!')
                return redirect('calendario')
            except Exception as e:
                messages.error(request, f'Erro ao criar reserva: {str(e)}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ReservaForm(usuario=request.user)
    
    context = {
        'form': form,
        'titulo': 'Nova Reserva',
        'botao': 'Criar Reserva'
    }
    return render(request, 'salas/reserva_form.html', context)


@login_required
def editar_reserva_view(request, reserva_id):
    """View para editar uma reserva existente"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    # Verificar se o usuário é o dono da reserva
    if reserva.usuario != request.user:
        messages.error(request, 'Você não tem permissão para editar esta reserva.')
        return redirect('calendario')
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva, usuario=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reserva atualizada com sucesso!')
                return redirect('calendario')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar reserva: {str(e)}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ReservaForm(instance=reserva, usuario=request.user)
    
    context = {
        'form': form,
        'reserva': reserva,
        'titulo': 'Editar Reserva',
        'botao': 'Salvar Alterações'
    }
    return render(request, 'salas/reserva_form.html', context)


@login_required
def excluir_reserva_view(request, reserva_id):
    """View para excluir uma reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    # Verificar se o usuário é o dono da reserva
    if reserva.usuario != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta reserva.')
        return redirect('calendario')
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso!')
        return redirect('calendario')
    
    context = {
        'reserva': reserva
    }
    return render(request, 'salas/reserva_confirmar_exclusao.html', context)


@login_required
def minhas_reservas_view(request):
    """View para listar as reservas do usuário logado"""
    reservas = Reserva.objects.filter(usuario=request.user).select_related('sala').order_by('dia_semana', 'horario')
    
    context = {
        'reservas': reservas
    }
    return render(request, 'salas/minhas_reservas.html', context)


def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('calendario')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'calendario')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'salas/login.html')


def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('calendario')


def registro_view(request):
    """View para registro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('calendario')
    
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Aguarde a aprovação de um administrador para fazer reservas.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UsuarioRegistroForm()
    
    context = {
        'form': form
    }
    return render(request, 'salas/registro.html', context)
