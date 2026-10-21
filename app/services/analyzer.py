from app.api.schemas import CarryStatsResponse

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
    total_gold = 0
    
    # 4. Проходим по нашим отфильтрованным матчам и суммируем всё
    for match in carry_matches:
        gpm = match.get("gold_per_min") or 0
        tower_dmg = match.get("tower_damage") or 0
        hero_dmg = match.get("hero_damage") or 0
        kills = match.get("kills") or 0
        assists = match.get("assists") or 0
        deaths = match.get("deaths") or 0
        duration = match.get("duration") or 0 



        # Логика определения победы:
        is_radiant = match["player_slot"] < 128
        if is_radiant and match["radiant_win"]:
            wins += 1
        elif not is_radiant and not match["radiant_win"]:
            wins += 1


        total_gpm += gpm
        total_kda += (kills + assists) / (deaths if deaths > 0 else 1)
        total_tower_damage += tower_dmg
        total_hero_damage += hero_dmg
        total_gold += gpm * (duration / 60)
        

    
    # 5. Считаем средние значения и возвращаем ответ
    return CarryStatsResponse(
        account_id=account_id,
        matches_analyzed=total_matches,
        winrate_percent= round((wins / total_matches) * 100, 2), 
        avg_gpm=int(total_gpm / total_matches),
        
        # ТВОЯ ЗАДАЧА: посчитай средний KDA, средний урон по башням 
        # и damage_per_gold_ratio (весь урон по героям / всё золото за эти матчи)
        avg_kda=round(total_kda / total_matches, 2), 
        avg_tower_damage=int(total_tower_damage / total_matches),
        damage_per_gold_ratio= round(total_hero_damage / total_gold, 2) if total_gold > 0 else 0.0
    )