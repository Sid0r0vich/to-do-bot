# Система управления задачами с уведомлениями
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)

## Содержание
- [Функциональность](#функциональность)
- [Архитектура](#архитектура)
- [Архитектура системы](#архитектура-системы)
- [Схема данных](#схема-данных)
- [API Эндпоинты](#api-эндпоинты)
- [Масштабирование](#масштабирование)
- [License](#license)
- [Команда проекта](#команда-проекта)

## Функциональность:

- Добавление задачи с текстом, датой и уведомлением

- Просмотр задач на конкретный день

- Получение списка невыполненных задач

- Отправка уведомлений пользователям

- Удаление задач

## Архитектура:

- Telegram Bot (Python, aiogram) — интерфейс для пользователей

- REST API (Go) — бизнес-логика и доступ к данным

- База данных (PostgreSQL) — хранение задач

### Архитектура системы

```plaintext
+-----------------------+         +------------------+         +---------------------+
| Telegram Bot (Python) |  <--->  | REST API (Go)    |  <--->  | PostgreSQL Database |
+-----------------------+         +------------------+         +---------------------+
                                                               
                                                                 
       
```

## Схема данных:

 Таблица tasks:

- id — уникальный ID задачи

- user_id — ID пользователя

- text — текст задачи

- day — день задачи

- notify_at — время уведомления (опционально)

- has_notification — флаг уведомления


## API Эндпоинты:

- POST /tasks — создать задачу [JSON с полями: user_id, text, day, notify_at]

- GET /tasks — получить задачи пользователя [user_id, day в query-параметрах]

- GET /notifications/pending — получить задачи с уведомлениями

- POST /notifications/:id/mark-sent — отметить уведомление отправленным [task id в URL]


## Масштабирование:

- Кэширование, изменение конфига, переезд на другую виртуалку
- По возможности добавить балансер или реплицировать базу данных при горизонтальном масштабировании

## License

[![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)](./LICENSE)

## Команда проекта

- [Дмитрий Сидоркин](https://t.me/sid00r) — Python разработчик, Cloud Engineer
- [Арина Павловская](https://t.me/yungeiren) - Go разработчик, технический писатель, DevOps
