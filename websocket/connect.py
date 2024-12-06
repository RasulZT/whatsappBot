import asyncio
import websockets
import json
from handlers.message_handler import handle_ws_messages

async def connect_websocket_hotkey(ws_url,ws_token,ws_channel):
    # Указываем WebSocket URL

    # Формируем данные для первого подключения
    connect_data = {
        "connect": {
            "token": ws_token,
            "name": "js"
        },
        "id": 1
    }

    # Формируем данные для подписки
    subscribe_data = {
        "subscribe": {
            "channel": ws_channel
        },
        "id": 2
    }

    # Подключаемся к WebSocket
    async with websockets.connect(ws_url) as websocket:
        # Отправляем запрос на подключение
        await websocket.send(json.dumps(connect_data))
        print("Отправлено сообщение для подключения:", connect_data)

        # Отправляем запрос на подписку
        await websocket.send(json.dumps(subscribe_data))
        print("Отправлено сообщение для подписки:", subscribe_data)

        # Запускаем обработку сообщений в другом потоке
        await handle_ws_messages(websocket,"ws_hotkey")


async def connect_websocket_backend(ws_url):
    async with websockets.connect(ws_url) as websocket:
        print(f"[WebSocket 2] Подключено к {ws_url}")
        await handle_ws_messages(websocket,"ws_back_status")

async def connect_websocket_backendNEW(ws_url):
    async with websockets.connect(ws_url) as websocket:
        print(f"[WebSocket 3] Подключено к {ws_url}")
        await handle_ws_messages(websocket,"ws_back_newOrder")
# Запуск WebSocket клиента
