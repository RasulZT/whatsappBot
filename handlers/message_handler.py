import asyncio

import aiohttp

from config import *
import requests
import websockets
import json
import os

from core.utils import send_interactive_message_async
from handlers.order_handler import handle_order_update, handle_order_create

USERS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "users.json")


# Функция для обработки сообщений
async def handle_ws_messages(websocket, ws_name):
    while True:
        # Ждём ответа
        response = await websocket.recv()

        # Принт полученного сообщения с WebSocket
        print("Получено сообщение:", response)

        # Проверяем, если получено сообщение "{}"
        if response == "{}":
            # Отправляем обратно то же самое сообщение
            await websocket.send("{}")
            print("Отправлено сообщение: {}")

        else:
            try:
                # Преобразуем строку в JSON
                response_data = json.loads(response)

                # Проверяем наличие ключа 'push' в ответе
                if "push" in response_data:
                    push_data = response_data["push"]
                    print(f"[{ws_name}] Получено push-сообщение: {push_data}")

                    if "pub" in push_data and "data" in push_data["pub"]:
                        message_data = push_data["pub"]["data"]
                        print(f"[{ws_name}] Информация о сообщении: {message_data}")

                        # Обработка сообщения
                        await process_message(ws_name, message_data)

                else:
                    print(f"[{ws_name}] Сообщение не содержит ключ 'push'.")
                    await process_message(ws_name, response_data)

            except websockets.ConnectionClosed:
                print(f"[{ws_name}] Соединение закрыто.")
                break
            except json.JSONDecodeError:
                print(f"[{ws_name}] Ошибка при разборе JSON.")
            except Exception as e:
                print(f"[{ws_name}] Ошибка: {e}")


async def process_message(ws_name, message_data):
    """Обрабатывает логику сообщения в зависимости от источника."""
    if ws_name == "ws_hotkey":
        # Логика для первого WebSocket
        if "chat" in message_data and "message" in message_data:
            print(f"Message_data:{message_data}")
            chat_id = message_data["chat"]["id"]
            message = message_data["message"]["message_preview"]
            message_payload=message_data["message"]["message_payload"]
            phone_number = message_data["chat"]["customer"]["phone_number"]
            full_name = message_data["chat"]["customer"]["full_name"]

            # Обработка исходящих или входящих сообщений
            if message_data["message"]["system_type"] == "incoming":
                await check_and_send_message(chat_id, message, full_name, phone_number,message_payload)
            else:
                print(f"[{ws_name}] Сообщение уже обработано ранее.")

    elif ws_name == "ws_back_status":
        # Логика для второго WebSocketw
        print(f"[{ws_name}] Обработка специфического сообщения: {message_data}")
        await handle_order_update(message_data)

    elif ws_name == "ws_back_newOrder":
        # Логика для второго WebSocket
        print(f"[{ws_name}] Обработка специфического сообщения: {message_data}")
        await  handle_order_create(message_data)

    else:
        print(f"[{ws_name}] Неизвестный источник сообщения.")


async def send_start_message(chat_id, message, full_name, phone_number):
    url = f"{API_URL}chat/{chat_id}/send-message"
    headers = {
        'Authorization': f'Bearer {Bearer_token}',  # Указываем токен авторизации
        'Content-Type': 'application/json'  # Указываем тип контента
    }
    payload = {
        "type": "interactive",
        "message": {
            "type": "button",
            "text": "Здравствуйте! 👋 Я — ваш личный бот для быстрого заказа пиццы и суши 🍕🍣. Откройте меню или узнайте наши команды ниже⬇️",
            "buttons": [
                {
                    "type": "reply",
                    "id": "menu",
                    "title": "Меню"
                },
                {
                    "type": "reply",
                    "id": "commands",
                    "title": "Команды"
                }
            ]
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно.")
            else:
                print(f"Ошибка при отправке сообщения. Статус код: {response.status}")
                print(await response.text())


async def send_menu_message(chat_id, message, full_name, phone_number):
    url = f"{API_URL}chat/{chat_id}/send-message"

    headers = {
        'Authorization': f'Bearer {Bearer_token}',  # Указываем токен авторизации
        'Content-Type': 'application/json'  # Указываем тип контента
    }

    payload = {
        "type": "interactive",
        "message": {
            "type": "cta_url",
            "header": "Меню",
            "text": "Нажмите на кнопку для открытия Меню",
            "cta": {
                "text": "Открыть Меню",
                "url": f"https://ws.monopizza.kz/?telegram_id={chat_id}&phone={phone_number}&name={full_name}"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно.")
            else:
                print(f"Ошибка при отправке сообщения. Статус код: {response.status}")
                print(await response.text())


async def send_manager_message(chat_id, message, full_name, phone_number):
    url = f"{API_URL}chat/{chat_id}/send-message"

    headers = {
        'Authorization': f'Bearer {Bearer_token}',  # Указываем токен авторизации
        'Content-Type': 'application/json'  # Указываем тип контента
    }

    payload = {
        "type": "interactive",
        "message": {
            "type": "cta_url",
            "header": "Мэнеджер",
            "text": "Свяжитесь с нашим мэнеджером⬇️",
            "footer": "TEST>",
            "cta": {
                "text": "Написать на Whatsapp",
                "url": "https://ws.monopizza.kz/wa/77021366697"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно.")
            else:
                print(f"Ошибка при отправке сообщения. Статус код: {response.status}")
                print(await response.text())


async def send_orderInfo_message(chat_id, message, full_name, phone_number):
    url = f"{API_URL}chat/{chat_id}/send-message"

    headers = {
        'Authorization': f'Bearer {Bearer_token}',  # Указываем токен авторизации
        'Content-Type': 'application/json'  # Указываем тип контента
    }

    payload = {
        "type": "interactive",
        "message": {
            "type": "cta_url",
            "header": "Ваш заказ",
            "text": "Нажмите на кнопку чтобы увидеть информаци",
            "footer": "TEST>",
            "cta": {
                "text": "Click",
                "url": f"https://ws.monopizza.kz/?telegram_id={chat_id}&order_id=64"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно.")
            else:
                print(f"Ошибка при отправке сообщения. Статус код: {response.status}")
                print(await response.text())


async def send_start_message_existing(chat_id, message, full_name, phone_number):
    url = f"{API_URL}chat/{chat_id}/send-message"
    headers = {
        'Authorization': f'Bearer {Bearer_token}',  # Указываем токен авторизации
        'Content-Type': 'application/json'  # Указываем тип контента
    }

    payload = payload = {
        "type": "interactive",
        "message": {
            "type": "button",
            "text": f"С возвращением {full_name}! Откройте меню или узнайте наши команды ниже⬇️",
            "buttons": [
                {
                    "type": "reply",
                    "id": "menu",
                    "title": "Меню"
                },
                {
                    "type": "reply",
                    "id": "commands",
                    "title": "Команды"
                }
            ]
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно.")
            else:
                print(f"Ошибка при отправке сообщения. Статус код: {response.status}")
                print(await response.text())


async def check_and_send_message(chat_id, message, full_name, phone_number,message_payload):
    """
    Проверяет наличие пользователя через API и, если его нет, регистрирует.
    Отправляет приветственное сообщение при успешной регистрации.
    """

    # Данные для отправки на регистрацию
    user_data = {
        "telegram_id": chat_id,
        "telegram_fullname": full_name,
        "phone": phone_number
    }
    print(f"Chat_id: {chat_id}")
    print(f"Message:{message}")
    print(f"Message_payload:{message_payload}")
    if message == "Команды" or message == "команды":

        await send_interactive_message_async(
            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id
        )
    elif message == "Меню":
        await send_menu_message(chat_id, "", full_name, phone_number)

    elif message == "Мэнеджер":

        await send_manager_message(chat_id, "", full_name, phone_number)

    elif message == "Информация о заказах":

        await send_orderInfo_message(chat_id, "", full_name, phone_number)

    else:
        async with aiohttp.ClientSession() as session:
            try:
                # POST-запрос на регистрацию пользователя
                async with session.post(f"{BACKEND_URL}auth/register/", json=user_data) as response:
                    if response.status == 201:
                        print("Пользователь успешно зарегистрирован.")

                        # Отправляем приветственное сообщение
                        await send_start_message(chat_id, "", full_name, phone_number)

                        # Небольшая задержка
                        await asyncio.sleep(1)


                    elif response.status == 200:
                        print("Пользователь уже существует.")
                        await send_start_message_existing(chat_id, "", full_name, phone_number)


                    else:
                        # Обработка случая, если статус ответа не 201
                        error_message = await response.text()
                        print(f"Ошибка регистрации: {response.status}, {error_message}")
                        # Например, отправить сообщение об ошибке
                        # await send_error_message(chat_id, f"Не удалось зарегистрировать пользователя. Ошибка: {response.status}")

            except aiohttp.ClientError as e:
                # Обработка ошибок сети или запроса
                print(f"Ошибка при выполнении запроса: {e}")
                # await send_error_message(chat_id, "Произошла ошибка при регистрации. Попробуйте позже.")
