from fastapi import APIRouter, HTTPException
import json 
import redis.asyncio as redis  # Используем асинхронный клиент!
from httpx import HTTPError
from app.api.schemas import CarryStatsResponse
from app.services.analyzer import calculate_carry_stats
from app.clients.opendota import OpenDotaClient


router = APIRouter()

redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True, socket_connect_timeout=5, 
    socket_timeout=5)
dota_client = OpenDotaClient()


@router.get("/players/{account_id}/carry_stats", response_model=CarryStatsResponse)
async def get_carry_stats(account_id: int):
    cache_key = f"carry_stats_{account_id}"
    try:
        cached_data = await redis_client.get(cache_key)
    except redis.RedisError as e:
        cached_data = None 
        print(f"Предупреждение: не удалось прочитать из кэша Redis: {e}")

    if cached_data:
        return json.loads(cached_data)


    # Если в кэше пусто, идем по тяжелому пути:
    
    try:
    # Дергаем внешнее API
        matches = await dota_client.get_player_matches(account_id)
    except HTTPError as e:
        print(f"Ошибка HTTP-клиента: {e}")
    # Если OpenDota лежит, отдаем 503
        raise HTTPException(status_code=503, detail="Ошибка при обращении к OpenDota API")

    if not matches:
        raise HTTPException(status_code=404, detail="Игрок не найден или профиль скрыт")

    stats_response = calculate_carry_stats(account_id, matches)

    stats_string = stats_response.model_dump_json()

    try:

        await redis_client.set(cache_key, stats_string, ex=3600)

    except redis.RedisError as redis_error:
        print(f"Предупреждение: не удалось записать в кэш Redis: {redis_error}") 

    return stats_response

    