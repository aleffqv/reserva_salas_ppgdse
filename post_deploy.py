import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reserva_salas_ppgdse.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("INICIANDO CRIACAO DE SUPERUSER")


ADMIN_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ppgdse')
ADMIN_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ppgdse@gmail.com')
ADMIN_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'PPGDSE2026')

print("Variaveis carregadas:")
print("Username:", ADMIN_USERNAME)
print("Email:", ADMIN_EMAIL)
print("Password:", "*" * len(ADMIN_PASSWORD) if ADMIN_PASSWORD else "NAO DEFINIDA")

if not ADMIN_USERNAME or not ADMIN_EMAIL or not ADMIN_PASSWORD:
    print("ERRO: Variaveis de admin nao configuradas no Render!")
    print("Configure no Render:")
    print("DJANGO_SUPERUSER_USERNAME")
    print("DJANGO_SUPERUSER_EMAIL")
    print("DJANGO_SUPERUSER_PASSWORD")
    sys.exit(1)

try:
    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        # Tenta criar usando create_superuser
        try:
            user = User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            print("SUPERUSER CRIADO COM SUCESSO!")
        except:
            # Se nao funcionar, cria manualmente
            user = User.objects.create_user(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print("SUPERUSER CRIADO MANUALMENTE!")
    else:
        # Atualiza usuario existente
        user = User.objects.get(username=ADMIN_USERNAME)
        user.set_password(ADMIN_PASSWORD)
        user.email = ADMIN_EMAIL
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print("SUPERUSER ATUALIZADO!")

    print("PRONTO!")
    print("Usuario:", ADMIN_USERNAME)
    print("Senha:", ADMIN_PASSWORD)
    
except Exception as e:
    print("ERRO:", str(e))
    sys.exit(1)