from api.schemas import CarryStatsResponse

def calculate_carry_stats(account_id: int, matches: list[dict]) -> CarryStatsResponse:
    CARRY_HEROES = [1, 8, 41, 93]
    
    # 1. Фильтруем список (собираем только нужные матчи)
    carry_matches = []
    for match in matches:
        if match["hero_id"] in CARRY_HEROES:
            carry_matches.append(match)
            
    # 2. Защита от деления на ноль (Edge Case)
    total_matches = len(carry_matches)
    if total_matches == 0:
        # Если игр на керри нет, возвращаем нули, чтобы не сломать фронтенд
        return CarryStatsResponse(
            account_id=account_id,
            matches_analyzed=0,
            winrate_percent=0.0,
            avg_gpm=0,
            avg_kda=0.0,
            avg_tower_damage=0,
            damage_per_gold_ratio=0.0
        )

    # 3. Подготовка переменных для суммирования
    wins = 0
    total_gpm = 0
    total_kda = 0.0
    total_tower_damage = 0
    total_hero_damage = 0
    
    
    # 4. Проходим по нашим отфильтрованным матчам и суммируем всё
    for match in carry_matches:
        total_gpm += match["gold_per_min"]
        
        # Логика определения победы:
        is_radiant = match["player_slot"] < 128
        if is_radiant and match["radiant_win"]:
            wins += 1
        elif not is_radiant and not match["radiant_win"]:
            wins += 1

        total_kda += (match["kills"] + match["assists"]) / (match["deaths"] if match["deaths"] > 0 else 1)

        total_tower_damage += match["tower_damage"]

        total_hero_damage += match["hero_damage"]
        
        # ТВОЯ ЗАДАЧА:
        # Допиши сюда суммирование KDA ( (kills + assists) / deaths )
        # Не забудь: если deaths == 0, считаем их за 1, иначе словим деление на ноль!
        # Допиши суммирование урона по башням, урона по героям и общего золота

    # 5. Считаем средние значения и возвращаем ответ
    return CarryStatsResponse(
        account_id=account_id,
        matches_analyzed=total_matches,
        winrate_percent=(wins / total_matches) * 100,
        avg_gpm=int(total_gpm / total_matches),
        
        # ТВОЯ ЗАДАЧА: посчитай средний KDA, средний урон по башням 
        # и damage_per_gold_ratio (весь урон по героям / всё золото за эти матчи)
        avg_kda=total_kda / total_matches, 
        avg_tower_damage=int(total_tower_damage / total_matches),
        damage_per_gold_ratio=total_hero_damage / total_gpm if total_gpm > 0 else 0.0
    )