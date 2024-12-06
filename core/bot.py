import traceback

import requests
from config import API_URL, Bearer_token
import os


# Определяем путь к файлу в предыдущей директории


class Bot:
    def __init__(self):
        self.handlers = []

    def register_handler(self, handler):
        self.handlers.append(handler)

    def update_config_with_token(self, auth_data):
        if not auth_data:
            print("Токен не получен, обновление config.py пропущено.")
            return
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.py")
        try:
            with open(config_path, "r") as file:
                lines = file.readlines()

            # Ищем строку с Bearer_token и обновляем её
            data_updated = False
            channel_id = self.get_channel_id(auth_data['access_token'])
            # Обновляем конфигурацию
            with open(config_path, "w") as file:
                for line in lines:
                    if line.strip().startswith("Bearer_token ="):
                        file.write(f"Bearer_token = '{auth_data['access_token']}'\n")
                        data_updated = True
                    elif line.strip().startswith("websocketChannel ="):
                        file.write(f"websocketChannel = '{auth_data['websocketChannel']}'\n")
                        data_updated = True
                    elif line.strip().startswith("websocketToken ="):
                        file.write(f"websocketToken = '{auth_data['websocketToken']}'\n")
                        data_updated = True
                    elif line.strip().startswith("websocketUrl ="):
                        file.write(f"websocketUrl = '{auth_data['websocketUrl']}'\n")
                        data_updated = True
                    elif line.strip().startswith("channel_id ="):
                        file.write(f"channel_id = '{channel_id}'\n")
                        data_updated = True
                    else:
                        file.write(line)

                # Если данные не были найдены, добавляем их в конец файла
                if not data_updated:
                    file.write(f"\nBearer_token = '{auth_data['access_token']}'\n")
                    file.write(f"websocketChannel = '{auth_data['websocketChannel']}'\n")
                    file.write(f"websocketToken = '{auth_data['websocketToken']}'\n")
                    file.write(f"websocketUrl = '{auth_data['websocketUrl']}'\n")
                    file.write(f"channel_id = '{channel_id}'\n")

            print("Конфигурация успешно обновлена.")
        except FileNotFoundError:
            print(f"Файл {config_path} не найден.")
        except Exception as e:
            print(f"Ошибка при обновлении config.py: {e}")

    def get_channel_id(self,token):

        url = f"{API_URL}channel?page=1&per_page=20"
        headers = {
            'Authorization': f'Bearer {token}',  # Указываем токен авторизации
            'Content-Type': 'application/json'  # Указываем тип контента
        }
        try:
            response = requests.get(url, headers=headers)
            print(response.text)
            response.raise_for_status()  # Проверяем статус ответа
            data = response.json()
            channel_id = data["result"]["items"][0]["whatsapp"]["channel_id"]
            print(channel_id)
            return channel_id



        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            print("Полный стек ошибки:")
            print(traceback.format_exc())
            return None

    def get_auth_data(self):
        url = f"{API_URL}account/signin"
        payload = {
            "password": "Rhbgnjy2004",  # Замените на ваш пароль
            "phone_number": "77007382452",  # Замените на ваш номер
            "socket": True
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Проверяем статус ответа
            data = response.json()

            if data.get("ok") and data.get("result"):
                result = data["result"]
                return {
                    "access_token": result["access_token"],
                    "websocketChannel": result["socket"]["ws_channel"],
                    "websocketToken": result["socket"]["ws_token"],
                    "websocketUrl": result["socket"]["ws_url"]
                }
            else:
                print("Ошибка: Неверный ответ от сервера.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def run(self):
        # Логика запуска бота
        print("Bot is running...")
        # Например, подписка на webhook (если это реализуется через webhook)
        auth_data = self.get_auth_data()  # Получаем токен
        self.update_config_with_token(auth_data)
        # while True:
        #     # Имитация получения сообщения
        #     message = self.get_message()
        #     for handler in self.handlers:
        #         handler(message)

    def get_message(self):
        # Логика получения сообщения через WhatsApp API
        pass

    # def send_message(self, chat_id, text):
    #     response = requests.post(
    #         API_URL,
    #         json={"chat_id": chat_id, "text": text},
    #         headers={"Authorization": f"Bearer {API_KEY}"}
    #     )
    #     return response.json()
