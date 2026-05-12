#!/bin/bash
set -e

echo "=== Auditoria PFIS — Inicializando ==="

echo "Gerando migrações..."
python manage.py makemigrations --noinput

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Executando seed do checklist..."
python manage.py seed_checklist

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear 2>/dev/null || python manage.py collectstatic --noinput

echo "=== Pronto. Iniciando servidor ==="
exec "$@"
