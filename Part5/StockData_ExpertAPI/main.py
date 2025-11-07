import os
import time
from datetime import date
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import httpx

# 1. Безопасная загрузка ключа API из .env
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

if not API_KEY:
    raise ValueError("API-ключ не найден. Убедитесь, что POLYGON_API_KEY установлен в файле .env")

# 2. Инициализация FastAPI и асинхронного HTTP-клиента
app = FastAPI(title="Polygon Stock Data API")
HTTP_CLIENT = httpx.AsyncClient(timeout=10.0)

# 3. Реализация КЭША (экспертная особенность)
# Кэш хранит: {тикер: {"data": данные, "timestamp": время_создания_кэша}}
CACHE = {}
TTL_SECONDS = 60  # Время жизни кэша: 60 секунд

# Базовый URL для Polygon.io (агрегированные данные)
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"

# =========================================================================

@app.get("/stocks/{ticker}")
async def get_stock_aggregates(
    ticker: str, 
    timespan: str = "day",
    multiplier: int = 1
):
    """
    Получает агрегированные данные (свечи) для заданного тикера.
    Использует кэширование с TTL=60с.
    """
    ticker = ticker.upper()
    cache_entry = CACHE.get(ticker)
    current_time = time.time()
    
    # 3a. ПРОВЕРКА КЭША
    if cache_entry and (current_time - cache_entry["timestamp"]) < TTL_SECONDS:
        print(f"[{ticker}] Данные получены из кэша.")
        return {
            "source": "cache",
            "ttl_remaining": round(TTL_SECONDS - (current_time - cache_entry["timestamp"]), 2),
            "data": cache_entry["data"]
        }
    
    # 3b. ПОЛУЧЕНИЕ НОВЫХ ДАННЫХ
    print(f"[{ticker}] Кэш устарел. Запрос к Polygon.io...")
    
    # Для примера: данные за последние 30 дней
    today = date.today().strftime("%Y-%m-%d")
    from_date = date.fromordinal(date.today().toordinal() - 30).strftime("%Y-%m-%d")

    url = (
        f"{BASE_URL}/{ticker}/{multiplier}/{timespan}/{from_date}/{today}"
        f"?adjusted=true&sort=desc&limit=120&apiKey={API_KEY}"
    )

    try:
        # Асинхронный запрос с httpx (экспертная особенность)
        response = await HTTP_CLIENT.get(url)
        response.raise_for_status() # Вызывает исключение для 4xx/5xx ответов

        data = response.json()
        
        if data.get("status") == "OK" and data.get("results"):
            # 3c. ОБНОВЛЕНИЕ КЭША
            CACHE[ticker] = {
                "data": data,
                "timestamp": current_time
            }
            return {
                "source": "polygon",
                "ttl_remaining": TTL_SECONDS,
                "data": data
            }
        else:
            # Если статус не 'OK' (например, тикер не найден)
            raise HTTPException(status_code=404, detail=f"Тикер '{ticker}' не найден или нет данных.")

    except httpx.HTTPStatusError as e:
        # Обработка ошибок HTTP (например, 429 Too Many Requests, 403 Forbidden)
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=f"Ошибка внешнего API: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        # Обработка сетевых ошибок (например, таймаут)
        raise HTTPException(
            status_code=503, 
            detail=f"Сетевая ошибка при запросе к Polygon.io: {e}"
        )

# =========================================================================

# Добавление хука для закрытия асинхронного клиента при завершении работы приложения
@app.on_event("shutdown")
async def shutdown_event():
    await HTTP_CLIENT.aclose()