A New Beginning - репозиторий для презентации моих навыков написания REST-API.

Django REST API блог-платформа с системой подписок, комментариями и Token аутентификацией.

# Технологии

- Backend: Python 3.12, Django 5.2, Django REST Framework
- База данных: MySQL 8.0
- Контейнеризация: Docker, Docker Compose
- Web server: Nginx + uWSGI
- Аутентификация: TokenAuthentification
- Тестирование: pytest + coverage
- Документация: Swagger, ReDoc.

# Быстрый старт

Запуск с Docker Compose (рекомендуется)
В терминале нужно выполнить следующее (инструкция для linux/Ubuntu):
```
# Создаем папку:
 mkdir app

# Заходим в нее:
cd app/

# Создаем пустой git репозиторий:
git init

# Клонируем проект из репозитория:
git clone git@github.com:Tokarev-Alexey/REST-API.git

# Заходим в нее:
cd REST-API

# Запускоем все сервисы
docker-compose up --build
```
Приложение будет доступно по http://localhost:80

Тестировать можно в браузере с SessionAuthentification, а можно и через Postman.

Формат вывода ответа:
```
{
    "count": 100,
    "next": "http://localhost/posts/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "id": 100,                                                  # Пост
            "author": "ultrachel",
            "title": "Title 10 поста от ultrachel",
            "text": "Текст поста.",
            "pub_date": "2025-09-26T10:58:29.783000Z",
            "comments": [
                {
                    "id": 1189,                                         # Комментарий к этому посту
                    "author_comm": "admin",
                    "text_comm": "1 комментарий от admin",
                    "pub_date": "2025-09-26T11:01:48.875000Z",
                    "post": 100
                },
                {
                    "id": 1190,                                         # Комментарий к этому посту
                    "author_comm": "admin",
                    "text_comm": "2 комментарий от admin",
                    "pub_date": "2025-09-26T11:01:48.879000Z",
                    "post": 100
                },...
```
# API Endpoints

 Аутентификация
```
http POST /api-token-auth/ 
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```
Response (Должен вернуть токен для авторизации):
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
# На главной странице вас встретят следующие адреса:

```
Лента постов:
    http GET /posts/
    Authorization: Token <your_token>
    
Лента ВСЕХ комментарие:
    http GET /comments/
    Authorization: Token <your_token>

Лента со ВСЕМИ пользователями:
    http GET /users/
    Authorization: Token <your_token>

Система подписок /supscriptions/ содержащая внутри ссылки на:
    Ленту с подписчиками:
    http GET /subscribers/
    Authorization: Token <your_token>

    Ленту с подписками:
    http GET /subscriptions/
    Authorization: Token <your_token>
    
    Кнопка подписаться/отписаться:
    http POST /pk/subscription_on_or_off где pk - id пользователя на которого хотим подписаться/отписаться
```
Так же можно...
Всем зарегистрированным пользователям можно выполнять GET POST PUT DELETE запросы, неавторизованным доступен только просмотр.
```
# Посмотерть определенный пост или удалить DELETE или изменить PUT:
http GET /posts/1 где 1 - id поста
Authorization: Token <your_token>

# Создать пост:
http POST /posts/
Authorization: Token <your_token>
Content-Type: application/json

{
  "title": "Мой первый пост",
  "text": "Содержание поста..."
}

# Посмотреть определенный комментарий или удалить DELETE или изменить PUT:
http GET /comments/1
Authorization: Token <your_token>

# Создать комментарий:
http POST /comments/
Authorization: Token <your_token>
Content-Type: application/json

{
  "post": 1,
  "text": "Отличный пост!"
}

# Лента пользователя

http GET /feed/
Authorization: Token <your_token>
```

# Структура проекта

```
REST-API/
├── api/            # REST API endpoints
├── media/          # Хранилище медиафайлов
├── nginx/          # Конфигурация nginx
├── posts/          # Модели постов и комментариев
├── project_config/ # Конфигурация проекта обычно называют myapp
├── staticfiles/    # Статические файлы проекта
├── users/          # Кастомная модель пользователя
├── conftest.py     # Фикстуры pytest
├── docker-compose.yml  # Сборка проекта
├── Dockerfile      # Для создания образа проекта
├── manage.py
└── Readme.md
```

# Разработка
Запуск тестов.

```bash
# Все тесты
pytest

# С покрытием кода
coverage run -m pytest
coverage report

# Конкретный модуль
pytest posts/tests/ -v
```

Создание миграций.

```bash
python manage.py makemigrations
python manage.py migrate
```

Создание суперпользователя (уже создан -u:-p admin:admin).

```bash
python manage.py createsuperuser
или
python3 manage.py createsuperuser
```

# Документация API

    После запуска доступна интерактивная документация:
- Swagger UI: http://localhost/swagger/
- ReDoc: http://localhost/redoc/

# Переменные окружения

```bash
DEBUG=False
DB_HOST=db
DB_NAME=firstdb
DB_USER=firstuser
DB_PASSWORD=firstpassword
```

# Примеры использования

    Создание поста через curl

```bash
curl -X POST http://localhost/posts/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Тестовый пост", "text": "Содержание"}'
```

    Получение ленты

```bash
curl -X GET http://localhost/feed/ \
  -H "Authorization: Token <your_token>"
```

