import aiohttp
from typing import Optional, Dict, Any


class RestClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        """
        :param base_url: Базовый URL для всех запросов.
        :param default_headers: Заголовки, которые будут использоваться по умолчанию.
        """
        self.base_url = base_url
        self.default_headers = default_headers or {"Content-Type": "application/json"}

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP-запрос.

        :param method: HTTP-метод ("GET", "POST", "PUT", "DELETE", и т.д.).
        :param endpoint: Конечная точка API (относительно base_url).
        :param params: Параметры запроса (для GET, DELETE).
        :param data: Тело запроса (для POST, PUT).
        :param headers: Дополнительные заголовки.
        :return: JSON-ответ от сервера.
        """
        url = f"{self.base_url}{endpoint}"  # Полный URL
        combined_headers = {**self.default_headers, **(headers or {})}

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=combined_headers,
            ) as response:
                response_data = await response.json()
                if response.status >= 400:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=response_data.get("error", "Unknown error"),
                    )
                return response_data

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return await self.request("GET", endpoint, params=params, headers=headers)

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return await self.request("POST", endpoint, data=data, headers=headers)

    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return await self.request("PUT", endpoint, data=data, headers=headers)

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return await self.request("DELETE", endpoint, params=params, headers=headers)
