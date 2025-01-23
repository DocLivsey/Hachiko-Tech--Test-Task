# Техническое задание
## ТЗ Телеграм бот IMEI

1. Общее описание

Необходимо разработать бэкенд-систему для проверки IMEI устройств, которая будет интегрирована с Telegram-ботом и предоставлять API для внешних запросов. В рамках тестового задания необходимо реализовать базовую работу с одним сервисом.

2. Функционал

2.1. Доступ

Белый список пользователей для Telegram:

Реализовать белый список для доступа к функционалу бота.

Авторизация через API:

Реализовать авторизацию по токену для доступа к API.

2.2. Telegram-бот

- Пользователь отправляет боту IMEI.

Бот должен:

- Проверить IMEI на валидность.

- Отправить в ответ информацию о IMEI.

2.3 Запросы API (пример)

Запрос на получение списка услуг:

Метод: POST /api/check-imei

Параметры запроса:

imei (строка, обязательный) — IMEI устройства.

token (строка, обязательный) — токен авторизации.

Ответ:

JSON с информацией о IMEI.

3. Список сервисов

В рамках тестового задания достаточно реализовать работу с одним сервисом:

https://imeicheck.net/

Токен API Sandbox: e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b

Токен API Live: sy5woSxuac7xKalljXFjgbB2hCRw7GQLueRtGp1974d8fe72


Документация: https://imeicheck.net/promo-api



Ответы на частые вопросы:

1. Сроки - дедлайна нет, средняя оценка 3-5 дней, мы готовы ждать до 14 дней

2. В каком виде присылать готовое выполнение - в тз достаточно информации и есть ответ на этот вопрос

Для сдачи задания  писать в телегу @ansukhareva. 