import asyncio

from config import *
from core.utils import send_interactive_orderInfo_async, send_interactive_message_async, \
    send_interactive_message_end_async, send_interactive_message_between_async, send_Location_async


async def handle_order_update(message_data):
    """
    Обрабатывает сообщение об обновлении заказа.
    """
    order_id = message_data.get("order_id")
    chat_id = message_data.get("telegram_id")
    changes = message_data.get("changes", {})
    url = f"{API_URL}"
    # Обработка нового статуса
    new_status = changes.get("status", None)
    if new_status == "active":
        await send_interactive_orderInfo_async(

            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id,
            text="Мы подтвердили получение вашей оплаты. Приступили к готовке вашего заказа"
        )


    elif new_status == "on_delivery":
        await send_interactive_orderInfo_async(

            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id,
            text="Ваш заказ готов и передан службе доставки."
        )
    elif new_status == "rejected":
        await send_interactive_orderInfo_async(

            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id,
            text="Ваш заказ отклонен, свяжитис с мэнеджером чтобы узнать причину."
        )
    elif new_status == "inactive":
        await send_interactive_orderInfo_async(

            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id,
            text="Поздравляем с покупкой. Приятного аппетита."
        )
        await send_interactive_message_end_async(
            api_url=f"{API_URL}chat/{chat_id}/send-message",
            access_token=Bearer_token,
            chat_id=chat_id
        )


    else:
        print(f"Неизвестный статус для заказа {order_id}: {new_status}")


async def handle_order_create(message_data):
    order_data = message_data.get('order_data', {})
    order_id = order_data.get('order_id')
    chat_id = order_data.get('client_id')

    await send_interactive_orderInfo_async(

        api_url=f"{API_URL}chat/{chat_id}/send-message",
        access_token=Bearer_token,
        chat_id=chat_id,
        text=f"Ваш заказ создан, номер заказа - {order_id}. Теперь укажите ваш адрес😊"
    )

    await asyncio.sleep(1)

    await send_Location_async(api_url=f"{API_URL}chat/{chat_id}/send-message",
                              access_token=Bearer_token,
                              chat_id=chat_id, text="")
    ###


    await send_interactive_message_between_async(
        api_url=f"{API_URL}chat/{chat_id}/send-message",
        access_token=Bearer_token,
        chat_id=chat_id
    )


async def notify_manager_about_active_order(order_id):
    """
    Уведомляет менеджера о том, что заказ активен.
    """
    print(f"Уведомляем менеджера о том, что заказ {order_id} активен.")
    # Реализуйте логику отправки уведомления менеджеру
