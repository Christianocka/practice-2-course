# Tudushka

Tudushka — это асинхронный ToDo REST API на FastAPI с хранением задач в PostgreSQL.

## Структура проекта

- `back/Api/` — основной API FastAPI (эндпоинты, модели)
- `database/` — подключение к базе данных и метаданные
- `docker-compose.yml` — запуск PostgreSQL и приложения через Docker
- `Dockerfile` — сборка образа приложения
- `requirements.txt` — зависимости Python

## Быстрый старт

### 1. Клонируйте репозиторий

```sh
git clone <repo-url>
cd Tudushka
```

### 2. Запуск через Docker Compose

```sh
docker-compose up --build
```

- FastAPI будет доступен на [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Переменные окружения

- `DATABASE_URL` — строка подключения к PostgreSQL (уже задана в docker-compose.yml)

## Основные эндпоинты

- `GET /tasks` — получить список задач
- `POST /tasks` — добавить задачу
- `PUT /tasks/{id}` — обновить задачу
- `PATCH /tasks/{id}/toggle_done` — изменить статус задачи (выполнена/не выполнена)
- `DELETE /tasks/{id}` — удалить задачу
- `POST /register` — регистрация пользователя
- `POST /login` — получение токена

## Примеры запросов к API

### Регистрация пользователя

```sh
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### Авторизация (получение токена)

```sh
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=user@example.com&password=yourpassword'
```
**Ответ:**  
```json
{"access_token": "<ваш токен>", "token_type": "bearer"}
```

### Создание задачи

```sh
curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <ваш токен>" \
  -H "Content-Type: application/json" \
  -d '{"task": "Купить хлеб"}'
```

### Получение всех задач

```sh
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <ваш токен>"
```

### Получение задачи по id

```sh
curl -X GET "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer <ваш токен>"
```

### Обновление задачи

```sh
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer <ваш токен>" \
  -H "Content-Type: application/json" \
  -d '{"task": "Купить молоко"}'
```

### Удаление задачи

```sh
curl -X DELETE "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer <ваш токен>"
```

### Переключение статуса задачи

```sh
curl -X PATCH "http://localhost:8000/tasks/1/toggle_done" \
  -H "Authorization: Bearer <ваш токен>"
```

## Зависимости

- FastAPI
- Uvicorn
- SQLAlchemy
- Databases
- asyncpg
- psycopg2-binary
- pydantic
- python-jose
- passlib[bcrypt]
- alembic

## Лицензия

MIT
