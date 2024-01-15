# tms-django

## Установка окружения

```
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Настройка PostgreSQL сервера

Имя БД: django
Схема: public

Команда для подключения к базе:
```shell
psql --dbname postgres
```

Команды для создания базы данных:
```sql
CREATE USER django WITH PASSWORD 'django' CREATEDB;
CREATE DATABASE django OWNER django;
GRANT ALL PRIVILEGES ON DATABASE django TO django;
```

Команда для создания структуры базы данных
```shell
python3 manage.py migrate
```
