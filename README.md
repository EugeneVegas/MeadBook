# MeadBook

Домашний журнал медовара. Учебный пет-проект.

## Запуск

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python manage.py migrate

python manage.py runserver
