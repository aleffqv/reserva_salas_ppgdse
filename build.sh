#!/usr/bin/env bash
set -o errexit

echo "INSTALANDO DEPENDENCIAS..."
pip install -r requirements.txt

echo "COLETANDO STATIC FILES..."
python manage.py collectstatic --noinput

echo "APLICANDO MIGRACOES..."
python manage.py migrate --noinput

echo "CRIANDO SUPERUSER..."
python post_deploy.py

echo "DEPLOY COMPLETO"
