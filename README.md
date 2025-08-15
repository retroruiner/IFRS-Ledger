# Учёт баланса по МСФО 9

Небольшое приложение на Django. Показывает принцип двойной записи.
Есть иерархия счетов: Статья -> Балансовая группа -> Счёт.

Транзакция: Дебет одного счёта = Кредит другого, сумма одинаковая.

## Что умеет
- Хранит статьи, группы, счета.
- Создаёт транзакции (дебет, кредит, сумма, описание) и меняет балансы.
- Показывает список счетов и историю транзакций.
- Есть админка.

## Требования
- Python 3.11+
- Django 4.2.x
- pip
- SQLite (по умолчанию) или PostgreSQL 15+ для Docker/Prod
- Docker + Docker Compose (только если запускаете в контейнерах)

---

## Запуск локально (без Docker)

```bash
# 1. Виртуальное окружение
python -m venv .venv

# 2. Активировать
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Зависимости
pip install -r requirements.txt

# 4. Миграции БД
python manage.py migrate

# 5. Стартовые данные (необязательно)
python manage.py loaddata initial_data

# 6. Админ-пользователь
python manage.py createsuperuser

# 7. Запуск сервера
python manage.py runserver
````

---

## Запуск в Docker

В репозитории должны быть: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.env.dev`, `.env.prod`.

### Файлы `.env`

`.env.dev` (пример):

```env
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=dev-secret
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://ifrs9:ifrs9@db:5432/ifrs9
```

`.env.prod` (пример, замените ключ):

```env
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=change-this-to-secure
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://ifrs9:ifrs9@db:5432/ifrs9
```

### Dev (runserver)

```bash
# сборка и запуск
docker compose up --build

# открыть приложение
# http://localhost:8000/

# первый раз (инициализация)
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py loaddata initial_data
```

### Prod (Gunicorn)

```bash
# сборка и запуск в фоне
docker compose -f docker-compose.prod.yml up --build -d

# проверить
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f db
docker compose -f docker-compose.prod.yml logs -f web

# первичная настройка
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker compose -f docker-compose.prod.yml exec web python manage.py loaddata initial_data

# открыть
# http://localhost:8000/

# остановить
docker compose -f docker-compose.prod.yml down
# удалить с томом БД
docker compose -f docker-compose.prod.yml down -v
```

## Маршруты

| URL                  | Описание            |
| -------------------- | ------------------- |
| `/`                  | Список счетов       |
| `/transactions/`     | История транзакций  |
| `/transactions/new/` | Создание транзакции |
| `/admin/`            | Админка Django      |

---

## Тесты

```bash
python manage.py test
# или в Docker:
docker compose exec web python manage.py test
```
