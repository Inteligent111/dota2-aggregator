from pydantic import BaseModel, Field


class CarryStatsResponse(BaseModel):

    account_id: int = Field(..., description="Steam ID игрока")
    matches_analyzed: int = Field(..., description="Количество проанализированных матчей")
    winrate_percent: float = Field(..., description="Процент побед")

    avg_gpm: int = Field(..., description="Средний GPM")
    avg_kda: float = Field(..., description="Средний KDA")
    avg_tower_damage: int = Field(..., description="Средний урон по башням")
    damage_per_gold_ratio: float = Field(..., description="Соотношение урона к золоту")


