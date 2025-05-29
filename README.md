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
- `POST /tasks` — добавить задачу (требует JSON: `{ "id": int, "task": str, "done": bool }`)
- `PUT /toggle/{id}` — изменить статус задачи (выполнена/не выполнена)
- `DELETE /delete/{id}` — удалить задачу

## Пример запроса

```sh
curl -X POST "http://localhost:8000/tasks" -H "Content-Type: application/json" -d '{"id": 1, "task": "Купить хлеб", "done": false}'
```

## Зависимости

- FastAPI
- Uvicorn
- SQLAlchemy
- Databases
- asyncpg
- psycopg2-binary
- pydantic

## Лицензия

MIT
