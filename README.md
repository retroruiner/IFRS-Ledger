# Учёт баланса по МСФО 9

Мини-приложение на **Django** для ведения бухгалтерского учёта по принципу **двойной записи**.

Структура:
- **Статья бухгалтерского баланса** -> **Балансовая группа** -> **Счёт**
- **Проводка**: Дебет одного счёта и Кредит другого с одинаковой суммой

---

## Запуск проекта

```bash
# 1. Создать виртуальное окружение
python -m venv .venv

# 2. Активировать окружение
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Выполнить миграции
python manage.py migrate

# 5. Загрузить стартовые данные
python manage.py loaddata initial_data

# 6. Создать суперпользователя
python manage.py createsuperuser

# 7. Запустить сервер
python manage.py runserver
````
---

## Запуск тестов

```bash
python manage.py test
```

---

## Основные маршруты

| URL                  | Описание            |
| -------------------- | ------------------- |
| `/`                  | Список счетов       |
| `/transactions/`     | История транзакций  |
| `/transactions/new/` | Создание транзакции |
| `/admin/`            | Админ-панель Django |

---
