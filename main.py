import asyncio
from core.bot import Bot
from websocket.connect import connect_websocket_hotkey, connect_websocket_backend,connect_websocket_backendNEW
from config import ws_url_status,ws_url_newOrder

async def main():
    bot = Bot()
    # bot.register_handler(message_handler.handle_message)
    # bot.register_handler(chat_handler.handle_command)
    bot.run()  # Предполагается, что это синхронная функция

    # Получаем данные для первого WebSocket
    data = bot.get_auth_data()
    ws_url = data['websocketUrl']
    ws_token = data['websocketToken']
    ws_channel = data['websocketChannel']

    # Запуск обоих WebSocket-соединений
    await asyncio.gather(
        connect_websocket_hotkey(ws_url, ws_token, ws_channel),
        connect_websocket_backend(ws_url_status),
        connect_websocket_backendNEW(ws_url_newOrder)
    )

    """
    """

if __name__ == "__main__":
    asyncio.run(main())
