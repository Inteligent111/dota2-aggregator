from httpx import AsyncClient

class OpenDotaClient:
    def __init__(self, base_url: str = "https://api.opendota.com/api"):
        self.base_url = base_url


    async def get_player_matches(self, account_id: int):
        async with AsyncClient() as client:

            # Делаем GET-запрос к API OpenDota для получения матчей игрока по его account_id
            response = await client.get(f"{self.base_url}/players/{account_id}/matches")

            # Проверяем статус ответа, если он не успешный, вызываем исключение
            response.raise_for_status()

            
            return response.json()
        
