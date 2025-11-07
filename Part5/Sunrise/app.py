# import requests
# from pprint import pprint
# from datetime import datetime, timedelta

# LATITUDE = 48.8584
# LONGITUDE = 2.2945
# BASE_API_URL = "https://api.sunrise-sunset.org/json"

# MAIN_API_URL = f"{BASE_API_URL}?lat={LATITUDE}&lng={LONGITUDE}"

# print(f"Запрос данных для: Широта {LATITUDE}, Долгота {LONGITUDE}")
# print("-" * 30)

# try:
#     utc_offset_hours = int(input("Введите смещение часового пояса от UTC в часах (например, 2 или -4): "))
#     print("-" * 30)
# except ValueError:
#     print("Ошибка: Введите корректное целое число для смещения.")
#     exit()

# try:
#     response = requests.get(MAIN_API_URL)
#     response.raise_for_status()
#     json_data = response.json()
#     if json_data.get("status") == "OK":
#         results = json_data["results"]

#         sunrise_utc_str = results["sunrise"]
#         sunset_utc_str = results["sunset"]
#         DATE_STRING = "1970-01-01 " 
        
#         sunrise_utc = datetime.strptime(DATE_STRING + sunrise_utc_str, "%Y-%m-%d %I:%M:%S %p")
#         sunset_utc = datetime.strptime(DATE_STRING + sunset_utc_str, "%Y-%m-%d %I:%M:%S %p")
        
#         time_delta = timedelta(hours=utc_offset_hours)
        
#         sunrise_local = sunrise_utc + time_delta
#         sunset_local = sunset_utc + time_delta

#         print("✅ Успешно получено время восхода и заката:")
#         print(f"   Восход Солнца (UTC): **{sunrise_utc_str}**")
#         print(f"   Заход Солнца (UTC):   **{sunset_utc_str}**")
#         print("-" * 30)
#         print(f"🌍 Местное Время (UTC{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours}):")
#         print(f"   Восход Солнца (Местное): **{sunrise_local.strftime('%H:%M:%S')}**")
#         print(f"   Заход Солнца (Местное):   **{sunset_local.strftime('%H:%M:%S')}**")
#         print("-" * 30)
#     else:
#         print(f"API вернул ошибку: {json_data.get('status')}")
# except requests.exceptions.RequestException as e:
#     print(f"Произошла ошибка при выполнении запроса: {e}")
# except Exception as e:
#     print(f"Произошла непредвиденная ошибка: {e}")


import requests
from datetime import datetime, timedelta
import time
import sys

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

SUNRISE_SUNSET_URL = "https://api.sunrise-sunset.org/json"

ZIP_CODE_API_URL = "http://api.zippopotam.us"

TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json"

CURRENT_TIMESTAMP = int(time.time())

def get_coordinates_from_zip(country_code, zip_code):
    print(f"-> Шаг 1: Запрос координат для {country_code}/{zip_code}...")
    url = f"{ZIP_CODE_API_URL}/{country_code}/{zip_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        place = data.get('places', [{}])[0]
        
        latitude = place.get('latitude')
        longitude = place.get('longitude')
        city = place.get('place name', 'Неизвестный город')
        
        if latitude and longitude:
            print(f"   Успешно! Город: {city}. Координаты: {latitude}, {longitude}")
            return float(latitude), float(longitude), city
        else:
            print(f"Ошибка в Geocoding API: Координаты не найдены или неверный почтовый индекс/код страны.")
            return None, None, None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Zippopotam.us: {e}")
        return None, None, None
    except Exception as e:
        print(f"Непредвиденная ошибка при обработке координат: {e}")
        return None, None, None

def get_timezone_offset(latitude, longitude):
    print("-> Шаг 2: Запрос смещения часового пояса (Timezone API)...")
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
        print("Ошибка: Необходим действующий GOOGLE_API_KEY для Timezone API.")
        return 0 

    params = {
        "location": f"{latitude},{longitude}",
        "timestamp": CURRENT_TIMESTAMP,
        "key": GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(TIMEZONE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "OK":
            raw_offset_sec = data.get("rawOffset", 0)
            dst_offset_sec = data.get("dstOffset", 0)
            
            total_offset_seconds = raw_offset_sec + dst_offset_sec
            total_offset_hours = total_offset_seconds / 3600
            
            timezone_id = data.get("timeZoneId", "N/A")
            
            print(f"Успешно! Часовой пояс: {timezone_id}. Общее смещение: UTC{'+' if total_offset_hours >= 0 else ''}{total_offset_hours:.1f} ч.")
            return total_offset_hours
        else:
            error_message = data.get("errorMessage", "Неизвестная ошибка")
            print(f"Ошибка в Timezone API: {data.get('status')}. Сообщение: {error_message}")
            return 0
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Timezone API: {e}")
        return 0

def get_sunrise_sunset(latitude, longitude):
    print("-> Шаг 3: Запрос времени восхода/захода (Sunrise-Sunset API)...")
    params = {
        "lat": latitude,
        "lng": longitude,
        "formatted": 0 
    }
    
    try:
        response = requests.get(SUNRISE_SUNSET_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "OK":
            results = data["results"]
            sunrise_utc_str = results["sunrise"]
            sunset_utc_str = results["sunset"]
            print("   Успешно получены данные UTC.")
            return sunrise_utc_str, sunset_utc_str
        else:
            print(f"Ошибка в Sunrise-Sunset API: {data.get('status')}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Sunrise-Sunset API: {e}")
        return None, None

def convert_utc_to_local(utc_time_str, utc_offset_hours):
    try:
        utc_dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        
        time_delta = timedelta(hours=utc_offset_hours)
        
        local_dt = utc_dt + time_delta
        
        return local_dt.strftime('%H:%M:%S')
    except ValueError as e:
        print(f"Ошибка парсинга времени: {e}")
        return "N/A"

def run_app():
    print("--- Автоматический Расчет Восхода и Захода ---")
    
    country_code = input("Введите двухбуквенный код страны (например, US, RU, FR): ").strip().upper()
    zip_code = input("Введите почтовый индекс (ZIP/Post Code): ").strip()
    
    if not country_code or not zip_code:
        print("Неверный ввод.")
        sys.exit()

    print("-" * 40)
    
    latitude, longitude, city = get_coordinates_from_zip(country_code, zip_code)
    
    if latitude is None:
        return

    print("-" * 40)
    
    utc_offset_hours = get_timezone_offset(latitude, longitude)
    
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY" and utc_offset_hours == 0:
        print("Расчет местного времени невозможен без действующего API-ключа Google.")
        print("Используется заглушка: Смещение = 0 ч.")

    print("-" * 40)

    sunrise_utc_str, sunset_utc_str = get_sunrise_sunset(latitude, longitude)
    
    if sunrise_utc_str is None:
        return
    
    local_sunrise_time = convert_utc_to_local(sunrise_utc_str, utc_offset_hours)
    local_sunset_time = convert_utc_to_local(sunset_utc_str, utc_offset_hours)

    print("\n" + "=" * 40)
    print(f"РЕЗУЛЬТАТЫ ДЛЯ {city} ({zip_code}, {country_code})")
    print("=" * 40)
    
    print("Время Восхода:")
    print(f"- UTC:   {sunrise_utc_str.split('T')[1].split('+')[0]}")
    print(f"- Местное: **{local_sunrise_time}** (UTC{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours:.1f})")
    
    print("\nВремя Захода:")
    print(f"- UTC:   {sunset_utc_str.split('T')[1].split('+')[0]}")
    print(f"- Местное: **{local_sunset_time}** (UTC{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours:.1f})")
    print("=" * 40)

if __name__ == "__main__":
    run_app()