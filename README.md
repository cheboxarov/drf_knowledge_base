# README.md

## Документация для Django API

Этот документ предоставляет обзор Django API для управления статьями, разделами, пользователями и тестами внутри статей. Включает информацию о доступных конечных точках, аутентификации и правах доступа.

## Содержание

- [Введение](#введение)
- [Установка](#установка)
- [Аутентификация](#аутентификация)
- [Конечные точки](#конечные-точки)
  - [Статьи](#статьи)
  - [Разделы](#разделы)
  - [Пользователи](#пользователи)
  - [Тесты](#тесты)
- [Права доступа](#права-доступа)

## Введение

Этот проект представляет собой Django API для управления статьями, разделами, пользователями и тестами внутри статей. Приложение использует Django REST Framework для создания API и PostgreSQL для хранения данных.

## Установка

### Установка с использованием Docker Compose

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/cheboxarov/drf_knowledge_base.git
    cd drf_knowledge_base
    ```

2. Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:
    ```env
    DATABASE_URL=postgresql://django:django-QWErty!2@db:5432/django
    DEBUG=1
    ```

3. Запустите Docker Compose:
    ```bash
    docker-compose up --build
    ```

4. Выполните миграции и создайте суперпользователя:
    ```bash
    docker-compose exec django python project/manage.py migrate
    docker-compose exec django python project/manage.py createsuperuser
    ```

## Аутентификация

Для аутентификации используется uuid пользователя в амо СРМ. UUID пользователя и Suburl должны быть переданы в заголовках `Authorization` и `Suburl`.

Пример заголовков:
```
Authorization: Bearer your_token_here
Suburl: your_suburl_here
```

## Конечные точки

### Статьи

- **GET /api/v1/articles**: Получить список статей.
- **GET /api/v1/articles?section=section_id**: Получить список статей в секции section_id.
- **POST /api/v1/articles**: Создать новую статью.
  - Пример JSON тела запроса:
    ```json
    {
        "name": "Новая статья",
        "section": 1,
        "parent": null,
        "author": 1,
        "content": "Содержание новой статьи",
        "position": 0
    }
    ```
- **GET /api/v1/articles/{id}**: Получить детальную информацию о статье.
- **PATCH /api/v1/articles/{id}**: Обновить статью.
  - Пример JSON тела запроса:
    ```json
    {
        "name": "Обновленная статья",
        "section": 1,
        "parent": null,
        "author": 1,
        "content": "Обновленное содержание статьи",
        "position": 0
    }
    ```
- **DELETE /api/v1/articles/{id}**: Удалить статью.

### Разделы

- **GET /api/v1/sections**: Получить список разделов.
- **POST /api/v1/sections**: Создать новый раздел.
  - Пример JSON тела запроса:
    ```json
    {
        "name": "Новый раздел",
        "description": "Описание нового раздела",
        "position": 0
    }
    ```
- **GET /api/v1/sections/{id}**: Получить детальную информацию о разделе.
- **PATCH /api/v1/sections/{id}**: Обновить раздел.
  - Пример JSON тела запроса:
    ```json
    {
        "name": "Обновленный раздел",
        "description": "Обновленное описание раздела",
        "position": 0
    }
    ```
- **DELETE /api/v1/sections/{id}**: Удалить раздел.

### Пользователи

- **GET /api/v1/users**: Получить список пользователей.
- **GET /api/v1/users/{amo_id}**: Получить детальную информацию о пользователе.
- **PATCH /api/v1/users/{amo_id}**: Обновить пользователя.
  - Пример JSON тела запроса:
    ```json
    {
        "username": "updated_user",
        "amo_id": 12345,
        "change_list": [1, 2, 3],
        "view_list": [1, 2, 3],
        "is_staff": false
    }
    ```

### Тесты

- **GET /api/v1/articles/{id}/test**: Получить тест, связанный со статьей.
  - Пример JSON ответа:
    ```json
    {
        "questions": [
            {
                "type": "single",
                "question": "kak",
                "answers": [
                    "asdasd",
                    "qweqwe"
                ],
                "right_answers": [
                    "asdasd"
                ]
            }
        ]
    }
    ```
- **POST /api/v1/articles/{id}/test**: Создать тест для статьи.
  - Пример JSON тела запроса:
    ```json
    {
        "questions": [
            {
                "type": "single",
                "question": "Новый вопрос",
                "answers": [
                    "Ответ 1",
                    "Ответ 2"
                ],
                "right_answers": [
                    "Ответ 1"
                ]
            }
        ]
    }
    ```
- **PATCH /api/v1/articles/{id}/test**: Обновить тест в статье.
  - Пример JSON тела запроса:
    ```json
    {
        "questions": [
            {
                "type": "single",
                "question": "Обновленный вопрос",
                "answers": [
                    "Обновленный ответ 1",
                    "Обновленный ответ 2"
                ],
                "right_answers": [
                    "Обновленный ответ 1"
                ]
            }
        ]
    }
    ```
- **DELETE /api/v1/articles/{id}/test**: Удалить тест из статьи.

## Права доступа

- **Администраторы (is_staff=True)**: Полный доступ ко всем операциям (создание, чтение, обновление, удаление).
- **Пользователи**: Могут читать статьи и разделы, которые находятся в их списке просмотра (`view_list`). Могут создавать, обновлять и удалять статьи и разделы, которые находятся в их списке изменений (`change_list`).

- **Тесты**: Могут создавать, обновлять, удалять и просматривать тесты внутри статей, если у пользователя есть права на изменение статьи.