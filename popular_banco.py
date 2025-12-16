#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reserva_salas_ppgdse.settings')
django.setup()

from salas.models import Usuario, Sala, Reserva

def popular_banco():
    print("Iniciando população do banco de dados...")
    
    # Criar superusuário
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_superuser(
            username='admin',
            email='admin@ppgdse.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            telefone='(00) 0000-0000',
            setor='Administração'
        )
        print(f"✓ Superusuário criado: {admin.username}")
    else:
        print("✓ Superusuário já existe")
    
    # Criar usuários de teste (professores)
    professores_data = [
        {
            'username': 'prof.silva',
            'email': 'silva@ppgdse.com',
            'password': 'senha123',
            'first_name': 'João',
            'last_name': 'Silva',
            'telefone': '(11) 98765-4321',
            'setor': 'Engenharia de Software'
        },
        {
            'username': 'prof.santos',
            'email': 'santos@ppgdse.com',
            'password': 'senha123',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'telefone': '(11) 98765-4322',
            'setor': 'Ciência de Dados'
        },
        {
            'username': 'prof.aleff',
            'email': 'aleff@ppgdse.com',
            'password': 'senha123',
            'first_name': 'Aleff',
            'last_name': 'Oliveira',
            'telefone': '(11) 98765-4323',
            'setor': 'Sistemas Distribuídos'
        }
    ]
    
    for prof_data in professores_data:
        if not Usuario.objects.filter(username=prof_data['username']).exists():
            usuario = Usuario.objects.create_user(
                username=prof_data['username'],
                email=prof_data['email'],
                password=prof_data['password'],
                first_name=prof_data['first_name'],
                last_name=prof_data['last_name'],
                telefone=prof_data['telefone'],
                setor=prof_data['setor']
            )
            print(f"✓ Professor criado: {usuario.first_name} {usuario.last_name}")
        else:
            print(f"✓ Professor já existe: {prof_data['username']}")
    
    # Criar salas
    salas_data = [
        {'numero': '204', 'cor': '#FF8C00', 'descricao': 'Sala com capacidade para 30 pessoas'},
        {'numero': '205', 'cor': '#28A745', 'descricao': 'Sala com capacidade para 25 pessoas'},
        {'numero': '206', 'cor': '#007BFF', 'descricao': 'Sala com capacidade para 35 pessoas'}
    ]
    
    for sala_data in salas_data:
        sala, created = Sala.objects.get_or_create(
            numero=sala_data['numero'],
            defaults={
                'cor': sala_data['cor'],
                'descricao': sala_data['descricao']
            }
        )
        if created:
            print(f"✓ Sala criada: {sala.numero}")
        else:
            print(f"✓ Sala já existe: {sala.numero}")
    
    # Criar algumas reservas de exemplo
    print("\nCriando reservas de exemplo...")
    
    prof_silva = Usuario.objects.get(username='prof.silva')
    prof_aleff = Usuario.objects.get(username='prof.aleff')
    sala_204 = Sala.objects.get(numero='204')
    sala_205 = Sala.objects.get(numero='205')
    
    reservas_exemplo = [
        {
            'sala': sala_204,
            'usuario': prof_silva,
            'dia_semana': 1,  # Segunda
            'horario': '08:00-12:00',
            'observacoes': 'Aula de Engenharia de Software'
        },
        {
            'sala': sala_204,
            'usuario': prof_silva,
            'dia_semana': 2,  # Terça
            'horario': '08:00-12:00',
            'observacoes': 'Aula de Engenharia de Software'
        },
        {
            'sala': sala_205,
            'usuario': prof_aleff,
            'dia_semana': 2,  # Terça
            'horario': '14:00-18:00',
            'observacoes': 'Aula de Sistemas Distribuídos'
        },
        {
            'sala': sala_205,
            'usuario': prof_aleff,
            'dia_semana': 5,  # Sexta
            'horario': '14:00-18:00',
            'observacoes': 'Aula de Sistemas Distribuídos'
        }
    ]
    
    for reserva_data in reservas_exemplo:
        reserva, created = Reserva.objects.get_or_create(
            sala=reserva_data['sala'],
            dia_semana=reserva_data['dia_semana'],
            horario=reserva_data['horario'],
            defaults={
                'usuario': reserva_data['usuario'],
                'observacoes': reserva_data['observacoes']
            }
        )
        if created:
            print(f"✓ Reserva criada: {reserva}")
        else:
            print(f"✓ Reserva já existe: {reserva}")
    
    print("\n" + "="*60)
    print("Banco de dados populado com sucesso!")
    print("="*60)
    print("\nCredenciais de acesso:")
    print("\nAdministrador:")
    print("  Usuário: admin")
    print("  Senha: admin123")
    print("\nProfessores:")
    print("  Usuário: prof.silva | Senha: senha123")
    print("  Usuário: prof.santos | Senha: senha123")
    print("  Usuário: prof.aleff | Senha: senha123")
    print("="*60)

if __name__ == '__main__':
    popular_banco()
