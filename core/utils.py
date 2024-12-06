import aiohttp


async def send_interactive_message_async(api_url, access_token, chat_id):
    """
    Асинхронно отправляет интерактивное сообщение с кнопками.

    :param api_url: str - URL API для отправки сообщений.
    :param access_token: str - Токен авторизации API.
    :param chat_id: str - Идентификатор чата, куда будет отправлено сообщение.
    :param text: str - Текст сообщения.
    :param buttons: list - Список кнопок. Каждая кнопка должна быть словарем с ключами: "id" и "title".
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "interactive",
        "recipient": {
            "chat_id": chat_id  # Укажите идентификатор чата
        },
        "message": {
            "type": "list",
            "text": "Для удобства общения с ботом, используйте наши команды. Также написав слово <Команды> в чат вы можете вызвать доступные команды 😊 ",
            # Текст сообщения
            "button": "Команды",  # Текст кнопки, открывающей список
            "sections": [
                {
                    "title": "Для заказа",  # Заголовок секции
                    "rows": [
                        {
                            "id": "menu_open",  # Уникальный идентификатор элемента списка
                            "title": "Меню",  # Название элемента списка
                            "description": "Закажите вкусную пиццу"  # Описание элемента списка (может быть пустым)
                        },
                        {
                            "id": "order_info",  # Уникальный идентификатор элемента списка
                            "title": "Информация о заказах",  # Название элемента списка
                            "description": ""  # Описание элемента списка (может быть пустым)
                        }
                    ]
                },
                {
                    "title": "Для связи с нами",  # Заголовок секции
                    "rows": [
                        {
                            "id": "call_manager",
                            "title": "Мэнеджер",
                            "description": ""
                        }
                    ]
                },
                {
                    "title": "Помощь",  # Заголовок секции
                    "rows": [
                        {
                            "id": "help_commands",
                            "title": "Команды",
                            "description": "Покажет все нужные команды"
                        }
                    ]
                }
            ]
        }
    }

    async with aiohttp.ClientSession() as session:
        print(api_url)
        print(chat_id)
        async with session.post(api_url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Интерактивное сообщение успешно отправлено.")
                return await response.json()
            else:
                print(f"Ошибка при отправке интерактивного сообщения. Статус: {response.status}")
                print(await response.text())
                return None


async def send_interactive_message_between_async(api_url, access_token, chat_id):
    """
    Асинхронно отправляет интерактивное сообщение с кнопками.

    :param api_url: str - URL API для отправки сообщений.
    :param access_token: str - Токен авторизации API.
    :param chat_id: str - Идентификатор чата, куда будет отправлено сообщение.
    :param text: str - Текст сообщения.
    :param buttons: list - Список кнопок. Каждая кнопка должна быть словарем с ключами: "id" и "title".
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "interactive",
        "recipient": {
            "chat_id": chat_id  # Укажите идентификатор чата
        },
        "message": {
            "type": "list",
            "text": "Для общения с ботом используйте наши команды:",  # Текст сообщения
            "button": "Команды",  # Текст кнопки, открывающей список
            "sections": [
                {
                    "title": "Для заказа",  # Заголовок секции
                    "rows": [
                        {
                            "id": "menu_open",  # Уникальный идентификатор элемента списка
                            "title": "Меню",  # Название элемента списка
                            "description": "Закажите вкусную пиццу"  # Описание элемента списка (может быть пустым)
                        },
                        {
                            "id": "order_info",  # Уникальный идентификатор элемента списка
                            "title": "Информация о заказах",  # Название элемента списка
                            "description": ""  # Описание элемента списка (может быть пустым)
                        }
                    ]
                },
                {
                    "title": "Для связи с нами",  # Заголовок секции
                    "rows": [
                        {
                            "id": "call_manager",
                            "title": "Мэнеджер",
                            "description": ""
                        }
                    ]
                },
                {
                    "title": "Помощь",  # Заголовок секции
                    "rows": [
                        {
                            "id": "help_commands",
                            "title": "Команды",
                            "description": "Покажет все нужные команды"
                        }
                    ]
                }
            ]
        }
    }

    async with aiohttp.ClientSession() as session:
        print(api_url)
        print(chat_id)
        async with session.post(api_url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Интерактивное сообщение успешно отправлено.")
                return await response.json()
            else:
                print(f"Ошибка при отправке интерактивного сообщения. Статус: {response.status}")
                print(await response.text())
                return None


async def send_interactive_message_end_async(api_url, access_token, chat_id):
    """
    Асинхронно отправляет интерактивное сообщение с кнопками.

    :param api_url: str - URL API для отправки сообщений.
    :param access_token: str - Токен авторизации API.
    :param chat_id: str - Идентификатор чата, куда будет отправлено сообщение.
    :param text: str - Текст сообщения.
    :param buttons: list - Список кнопок. Каждая кнопка должна быть словарем с ключами: "id" и "title".
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "interactive",
        "recipient": {
            "chat_id": chat_id  # Укажите идентификатор чата
        },
        "message": {
            "type": "list",
            "text": "🎉 Ваш заказ успешно завершён! \n Спасибо за ваш выбор! 🙌 \n Чтобы сделать новый заказ или воспользоваться нашими сервисами, просто используйте команды:",
            # Текст сообщения
            "button": "Команды",  # Текст кнопки, открывающей список
            "sections": [
                {
                    "title": "Для заказа",  # Заголовок секции
                    "rows": [
                        {
                            "id": "menu_open",  # Уникальный идентификатор элемента списка
                            "title": "Меню",  # Название элемента списка
                            "description": "Закажите вкусную пиццу"  # Описание элемента списка (может быть пустым)
                        },
                        {
                            "id": "order_info",  # Уникальный идентификатор элемента списка
                            "title": "Информация о заказах",  # Название элемента списка
                            "description": ""  # Описание элемента списка (может быть пустым)
                        }
                    ]
                },
                {
                    "title": "Для связи с нами",  # Заголовок секции
                    "rows": [
                        {
                            "id": "call_manager",
                            "title": "Мэнеджер",
                            "description": ""
                        }
                    ]
                },
                {
                    "title": "Помощь",  # Заголовок секции
                    "rows": [
                        {
                            "id": "help_commands",
                            "title": "Команды",
                            "description": "Покажет все нужные команды"
                        }
                    ]
                }
            ]
        }
    }

    async with aiohttp.ClientSession() as session:
        print(api_url)
        print(chat_id)
        async with session.post(api_url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Интерактивное сообщение успешно отправлено.")
                return await response.json()
            else:
                print(f"Ошибка при отправке интерактивного сообщения. Статус: {response.status}")
                print(await response.text())
                return None


async def send_interactive_orderInfo_async(api_url, access_token, chat_id, text):
    """
    Асинхронно отправляет интерактивное сообщение с кнопками.

    :param api_url: str - URL API для отправки сообщений.
    :param access_token: str - Токен авторизации API.
    :param chat_id: str - Идентификатор чата, куда будет отправлено сообщение.
    :param text: str - Текст сообщения.
    :param buttons: list - Список кнопок. Каждая кнопка должна быть словарем с ключами: "id" и "title".
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "text",
        "message": {
            "text": text
        }
    }

    async with aiohttp.ClientSession() as session:
        print(api_url)
        print(chat_id)
        async with session.post(api_url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Интерактивное сообщение успешно отправлено.")
                return await response.json()
            else:
                print(f"Ошибка при отправке интерактивного сообщения. Статус: {response.status}")
                print(await response.text())
                return None


async def send_Location_async(api_url, access_token, chat_id, text):
    """
    Асинхронно отправляет интерактивное сообщение с кнопками.

    :param api_url: str - URL API для отправки сообщений.
    :param access_token: str - Токен авторизации API.
    :param chat_id: str - Идентификатор чата, куда будет отправлено сообщение.
    :param text: str - Текст сообщения.
    :param buttons: list - Список кнопок. Каждая кнопка должна быть словарем с ключами: "id" и "title".
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "interactive",
        "message": {
            "type": "location_request_message",
            "text": "Поделитесь вашей геолокацией"
        }
    }

    async with aiohttp.ClientSession() as session:
        print(api_url)
        print(chat_id)
        async with session.post(api_url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Интерактивное сообщение успешно отправлено.")
                return await response.json()
            else:
                print(f"Ошибка при отправке интерактивного сообщения. Статус: {response.status}")
                print(await response.text())
                return None
