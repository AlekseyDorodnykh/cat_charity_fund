# Проект QRKot

## Описание
Приложение для Фонда, который собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Основные используемые технологии
1. Python 3.10 
2. FastAPI 0.78.0
3. SQLAlchemy
4. SQLite


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AlekseyDorodnykh/cat_charity_fund.git
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Создать файл .env в корне проекта:
```
APP_TITLE=Кошачий благотворительный фонд
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
description=Сервис для поддержки котиков!
SECRET=GhI67!asyk  (укажите свой)
FIRST_SUPERUSER_EMAIL=admin@admin.com  (укажите свой)
FIRST_SUPERUSER_PASSWORD=1234567  (укажите свой)

# Данные из настройки Google Cloud:
EMAIL = none (укажите свой)
TYPE = none
PROJECT_ID = none
PRIVATE_KEY_ID = none
PRIVATE_KEY = none
CLIENT_EMAIL = none
CLIENT_ID = none
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL = none

```

Выполнить миграции:
```
alembic upgrade head
```

Запустить проект:
```
uvicorn app.main:app
```

После запуска будет доступна документация:
```
http://127.0.0.1:8000/swagger
http://127.0.0.1:8000/redoc
```

### Автор проекта:
- [Дородных Алексей](https://github.com/AlekseyDorodnykh/)