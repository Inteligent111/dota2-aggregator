# Dota 2 Carry Stats Aggregator

Микросервис на FastAPI для агрегации статистики игроков на позиции керри через OpenDota API. 
Реализовано кэширование ответов для обхода rate-лимитов и ускорения выдачи результатов.

## 🛠 Технологии
* **Язык:** Python 3.10+
* **Фреймворк:** FastAPI
* **Кэширование:** Redis (асинхронный клиент `redis.asyncio`)
* **HTTP-клиент:** Httpx (для асинхронных запросов к OpenDota)
* **Валидация данных:** Pydantic

## 📋 Требования
До того как вы скачаете код, убедитесь, что у вас установлены:
1. Python 3.10 или выше.
2. Локально запущенный сервер Redis (стандартный порт `6379`).

## 🚀 Быстрый старт

**1. Клонирование репозитория:**
```bash
git clone https://github.com/твое-имя/dota-carry-stats.git
cd dota-carry-stats
```

**2. Создание и активация виртуального окружения:**
```bash
python -m venv venv
# Для Windows: venv\Scripts\activate
# Для Mac/Linux: source venv/bin/activate
```

**3. Установка зависимостей:**
```bash
pip install -r requirements.txt
```

**4. Запуск сервера:**
```bash
uvicorn main:app --reload
```

## 📖 Использование (API Docs)
После успешного запуска сервера, интерактивная документация (Swagger UI) будет доступна по адресу:
👉 http://localhost:8000/docs

Пример запроса для получения статистики игрока (подставьте нужный `account_id`):
`GET /players/123456789/carry_stats`