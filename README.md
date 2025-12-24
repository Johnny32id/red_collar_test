# Geo Points API

![Tests & Lint](https://img.shields.io/github/actions/workflow/status/Johnny32id/red_collar_test/tests.yml?label=Tests%20%26%20Lint)

Backend-приложение на Django для работы с географическими точками на карте. Приложение предоставляет REST API для создания точек, обмена сообщениями и поиска контента в заданном радиусе от указанных координат.

## Технический стек

- Python 3.10+
- Django 5.0+
- Django REST Framework (DRF)
- SQLite с расширением SpatiaLite
- GeoDjango
- Poetry (управление зависимостями)
- pytest (тестирование)

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd red_collar_test
```

### 2. Установка зависимостей

```bash
poetry install
```

### 3. Установка SpatiaLite

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y spatialite-bin libspatialite-dev libsqlite3-mod-spatialite
```

**macOS:**
```bash
brew install spatialite-tools
```

**Windows:**
```bash
conda install -c conda-forge spatialite
```

### 4. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и добавьте необходимые переменные:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл, указав свои значения (особенно `SECRET_KEY` для production).

### 5. Применение миграций

```bash
poetry run python manage.py migrate
```

### 6. Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
poetry run python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

## Получение токена авторизации

После создания пользователя получите токен:

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Сохраните полученный токен в `.env` как `API_TOKEN` для удобства использования.

## API Документация

Все эндпоинты требуют авторизации через Token Authentication в заголовке:
```
Authorization: Token <your_token>
```

### Эндпоинты

#### 1. Создание точки

**POST** `/api/points/`

```bash
curl -X POST http://localhost:8000/api/points/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Москва",
    "description": "Столица России",
    "latitude": 55.7558,
    "longitude": 37.6173
  }'
```

#### 2. Создание сообщения

**POST** `/api/points/messages/`

```bash
curl -X POST http://localhost:8000/api/points/messages/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "point_id": 1,
    "text": "Привет из Москвы!"
  }'
```

#### 3. Поиск точек в радиусе

**GET** `/api/points/search/?latitude=55.7558&longitude=37.6173&radius=10`

Параметры:
- `latitude` (float) - широта центра поиска
- `longitude` (float) - долгота центра поиска
- `radius` (float) - радиус поиска в километрах (от 0.1 до 1000)

```bash
curl -X GET "http://localhost:8000/api/points/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token <your_token>"
```

#### 4. Поиск сообщений в радиусе

**GET** `/api/messages/search/?latitude=55.7558&longitude=37.6173&radius=10`

Параметры аналогичны поиску точек.

```bash
curl -X GET "http://localhost:8000/api/messages/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token <your_token>"
```

#### 5. Список точек

**GET** `/api/points/`

Возвращает список всех точек с пагинацией.

#### 6. Список сообщений

**GET** `/api/messages/`

Возвращает список всех сообщений с пагинацией.

## Тестирование

```bash
poetry run pytest
```

С покрытием кода:

```bash
poetry run pytest --cov=points --cov-report=html
```

## Разработка

### Форматирование кода

```bash
poetry run black .
poetry run isort .
poetry run ruff check .
```

### Миграции

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Технические детали

- Все координаты хранятся в формате WGS84 (SRID 4326)
- Поиск в радиусе выполняется с помощью GeoDjango `distance_lte`
- Используется пространственная индексация для оптимизации запросов
- Все эндпоинты требуют авторизации через Token Authentication
- База данных SQLite создается автоматически при первом запуске миграций

## Лицензия

MIT
