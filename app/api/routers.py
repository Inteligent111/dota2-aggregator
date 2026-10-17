from fastapi import APIRouter, HTTPException
import json 
import redis.asyncio as redis  # Используем асинхронный клиент!

from api.schemas import CarryStatsResponse
from services.analyzer import calculate_carry_stats
from clients.opendota import OpenDotaClient


router = APIRouter()

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
dota_client = OpenDotaClient()


@router.get("/players/{account_id}/carry_stats", response_model=CarryStatsResponse)
async def get_carry_stats(account_id: int):
    cache_key = f"carry_stats_{account_id}"

    cached_data = await redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)


    # Если в кэше пусто, идем по тяжелому пути:
    try:
        # Дергаем внешнее API
        matches = await dota_client.get_player_matches(account_id)

        if not matches:
            raise HTTPException(status_code=404, detail="Игрок не найден или профиль скрыт")

        stats_response = calculate_carry_stats(account_id, matches)

        stats_string = stats_response.model_dump_json()

        await redis_client.set(cache_key, stats_string, ex=3600)

        return stats_response

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        # Если OpenDota лежит, отдаем 503
        raise HTTPException(status_code=503, detail="Ошибка при обращении к OpenDota API")