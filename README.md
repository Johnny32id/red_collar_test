# Geo Points API

![Tests & Lint](https://github.com/Johnny32id/red_collar_test/actions/workflows/tests.yml/badge.svg)

Backend-приложение на Django для работы с географическими точками на карте. Приложение предоставляет REST API для создания точек, обмена сообщениями и поиска контента в заданном радиусе от указанных координат.

## Технический стек

- Python 3.10+
- Django 5.0+
- Django REST Framework (DRF)
- SQLite с расширением SpatiaLite
- GeoDjango
- Poetry (управление зависимостями)
- pytest (тестирование)

## Требования

- Python 3.10 или выше
- Poetry для управления зависимостями
- SpatiaLite (для работы с геоданными в SQLite)

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

Для работы с геоданными в SQLite необходимо установить SpatiaLite:

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
Скачайте и установите SpatiaLite с официального сайта или используйте conda:
```bash
conda install -c conda-forge spatialite
```

**Примечание:** Пакет `libsqlite3-mod-spatialite` необходим для загрузки модуля SpatiaLite в SQLite.

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе примера:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл, указав свои значения для секретного ключа. Пример содержимого `.env.example`:

```env
# Django настройки
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API токен для авторизации в API
API_TOKEN=your_api_token_here
```

**Важно:** Измените `SECRET_KEY` на уникальное значение для production окружения!

**Примечание:** База данных SQLite создается автоматически при первом запуске миграций. Файл базы данных `db.sqlite3` будет создан в корне проекта. SpatiaLite инициализируется автоматически при первом подключении к базе данных.

### 5. Применение миграций

```bash
poetry run python manage.py migrate
```

### 6. Создание суперпользователя (опционально)

```bash
poetry run python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
poetry run python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

## Быстрая проверка работы проекта

После установки и настройки можно быстро проверить, что все работает:

### 1. Убедитесь, что SpatiaLite установлен

```bash
spatialite --version
```

### 2. Получите токен авторизации

После создания пользователя получите токен:

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

Скопируйте полученный токен и добавьте его в файл `.env`:

```env
API_TOKEN=your_api_token_here
```

### 3. Протестируйте основные эндпоинты

**Создайте точку:**

Используя токен из переменной окружения:
```bash
export API_TOKEN=$(grep API_TOKEN .env | cut -d '=' -f2)
curl -X POST http://localhost:8000/api/points/ \
  -H "Authorization: Token $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Москва",
    "latitude": 55.7558,
    "longitude": 37.6173
  }'
```

Или укажите токен напрямую:
```bash
curl -X POST http://localhost:8000/api/points/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Москва",
    "latitude": 55.7558,
    "longitude": 37.6173
  }'
```

**Создайте сообщение:**

Используя токен из переменной окружения:
```bash
export API_TOKEN=$(grep API_TOKEN .env | cut -d '=' -f2)
curl -X POST http://localhost:8000/api/points/messages/ \
  -H "Authorization: Token $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "point_id": 1,
    "text": "Привет из Москвы!"
  }'
```

**Поиск точек:**

Используя токен из переменной окружения:
```bash
export API_TOKEN=$(grep API_TOKEN .env | cut -d '=' -f2)
curl -X GET "http://localhost:8000/api/points/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token $API_TOKEN"
```

### 4. Запустите тесты

```bash
poetry run pytest
```

## API Документация

Все эндпоинты требуют авторизации через Token Authentication.

### Получение токена авторизации

Сначала создайте пользователя через Django admin или используйте команду:

```bash
poetry run python manage.py createsuperuser
```

Затем получите токен через API:

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Ответ:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Рекомендуется:** Сохраните токен в файл `.env` для удобства использования:

```env
API_TOKEN=9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Затем используйте токен из переменной окружения в запросах:

```bash
export API_TOKEN=$(grep API_TOKEN .env | cut -d '=' -f2)
curl -X GET http://localhost:8000/api/points/ \
  -H "Authorization: Token $API_TOKEN"
```

Или укажите токен напрямую в заголовке `Authorization: Token <your_token>` для всех последующих запросов.

### Эндпоинты API

#### 1. Создание точки на карте

**POST** `/api/points/`

Создает новую географическую точку.

**Заголовки:**
```
Authorization: Token <your_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "name": "Москва",
  "description": "Столица России",
  "latitude": 55.7558,
  "longitude": 37.6173
}
```

**Пример запроса (curl):**
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

**Ответ (201 Created):**
```json
{
  "id": 1,
  "name": "Москва",
  "description": "Столица России",
  "latitude": 55.7558,
  "longitude": 37.6173,
  "location": "POINT (37.6173 55.7558)",
  "created_by": {
    "id": 1,
    "username": "admin"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "messages_count": 0
}
```

#### 2. Создание сообщения к точке

**POST** `/api/points/messages/`

Создает сообщение к заданной точке.

**Заголовки:**
```
Authorization: Token <your_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "point_id": 1,
  "text": "Привет из Москвы!"
}
```

**Пример запроса (curl):**
```bash
curl -X POST http://localhost:8000/api/points/messages/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "point_id": 1,
    "text": "Привет из Москвы!"
  }'
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "point": {
    "id": 1,
    "name": "Москва",
    "description": "Столица России",
    "latitude": 55.7558,
    "longitude": 37.6173,
    "location": "POINT (37.6173 55.7558)",
    "created_by": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "messages_count": 1
  },
  "text": "Привет из Москвы!",
  "author": {
    "id": 1,
    "username": "admin"
  },
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### 3. Поиск точек в радиусе

**GET** `/api/points/search/`

Ищет точки в заданном радиусе от указанных координат.

**Параметры запроса:**
- `latitude` (float) - широта центра поиска
- `longitude` (float) - долгота центра поиска
- `radius` (float) - радиус поиска в километрах (от 0.1 до 1000)

**Заголовки:**
```
Authorization: Token <your_token>
```

**Пример запроса (curl):**
```bash
curl -X GET "http://localhost:8000/api/points/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token <your_token>"
```

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Москва",
    "description": "Столица России",
    "latitude": 55.7558,
    "longitude": 37.6173,
    "location": "POINT (37.6173 55.7558)",
    "created_by": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "messages_count": 1
  }
]
```

#### 4. Поиск сообщений в радиусе

**GET** `/api/messages/search/`

Ищет сообщения, чьи точки находятся в заданном радиусе от указанных координат.

**Параметры запроса:**
- `latitude` (float) - широта центра поиска
- `longitude` (float) - долгота центра поиска
- `radius` (float) - радиус поиска в километрах (от 0.1 до 1000)

**Заголовки:**
```
Authorization: Token <your_token>
```

**Пример запроса (curl):**
```bash
curl -X GET "http://localhost:8000/api/messages/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token <your_token>"
```

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "point": {
      "id": 1,
      "name": "Москва",
      "description": "Столица России",
      "latitude": 55.7558,
      "longitude": 37.6173,
      "location": "POINT (37.6173 55.7558)",
      "created_by": {
        "id": 1,
        "username": "admin"
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "messages_count": 1
    },
    "text": "Привет из Москвы!",
    "author": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
]
```

#### 5. Получение списка точек

**GET** `/api/points/`

Возвращает список всех точек с пагинацией.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Пример запроса (curl):**
```bash
curl -X GET http://localhost:8000/api/points/ \
  -H "Authorization: Token <your_token>"
```

#### 6. Получение списка сообщений

**GET** `/api/messages/`

Возвращает список всех сообщений с пагинацией.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Пример запроса (curl):**
```bash
curl -X GET http://localhost:8000/api/messages/ \
  -H "Authorization: Token <your_token>"
```

## Примеры запросов (Postman)

### Коллекция Postman

Импортируйте следующие запросы в Postman:

1. **Создание точки**
   - Method: POST
   - URL: `http://localhost:8000/api/points/`
   - Headers: `Authorization: Token <your_token>`
   - Body (JSON):
     ```json
     {
       "name": "Санкт-Петербург",
       "description": "Северная столица",
       "latitude": 59.9343,
       "longitude": 30.3351
     }
     ```

2. **Создание сообщения**
   - Method: POST
   - URL: `http://localhost:8000/api/points/messages/`
   - Headers: `Authorization: Token <your_token>`
   - Body (JSON):
     ```json
     {
       "point_id": 1,
       "text": "Красивый город!"
     }
     ```

3. **Поиск точек**
   - Method: GET
   - URL: `http://localhost:8000/api/points/search/?latitude=55.7558&longitude=37.6173&radius=50`
   - Headers: `Authorization: Token <your_token>`

4. **Поиск сообщений**
   - Method: GET
   - URL: `http://localhost:8000/api/messages/search/?latitude=55.7558&longitude=37.6173&radius=50`
   - Headers: `Authorization: Token <your_token>`

## Тестирование

Запуск тестов:

```bash
poetry run pytest
```

Запуск тестов с покрытием:

```bash
poetry run pytest --cov=points --cov-report=html
```

## Техническое описание

### Архитектура проекта

Проект использует стандартную архитектуру Django с разделением на приложения:

- `config/` - конфигурация проекта (settings, urls, wsgi)
- `points/` - приложение для работы с точками и сообщениями
  - `models.py` - модели Point и Message с геополями
  - `serializers.py` - сериализаторы для API
  - `views.py` - ViewSet'ы для REST API
  - `urls.py` - маршрутизация API
  - `admin.py` - настройка админ-панели

### Модели данных

#### Point (Точка)
- `location` - PointField (GeoDjango) для хранения координат
- `name` - название точки
- `description` - описание точки
- `created_by` - пользователь, создавший точку
- `created_at`, `updated_at` - временные метки

#### Message (Сообщение)
- `point` - связь с точкой
- `text` - текст сообщения
- `author` - автор сообщения
- `created_at`, `updated_at` - временные метки

### Географические операции

Проект использует GeoDjango и SpatiaLite для работы с геоданными:

- Все координаты хранятся в формате WGS84 (SRID 4326)
- Поиск в радиусе выполняется с помощью `distance_lte` и `D(km=...)`
- Используется пространственная индексация для оптимизации запросов

### Безопасность

- Все эндпоинты требуют авторизации через Token Authentication
- Использование `IsAuthenticated` permission для всех ViewSet'ов
- CORS настроен для разрешенных источников

### Оптимизация

- Использование `select_related` и `prefetch_related` для уменьшения количества запросов к БД
- Пространственные индексы на геополя
- Пагинация для списковых эндпоинтов

## Разработка

### Форматирование кода

```bash
poetry run black .
poetry run isort .
poetry run ruff check .
```

### Создание миграций

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Лицензия

MIT
