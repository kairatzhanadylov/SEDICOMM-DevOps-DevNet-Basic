import requests
import urllib.parse

MAIN_API = "https://mapquestapi.com/directions/v2/route?"
API_KEY = "YOUR_API_KEY_HERE" 

def get_directions(orig, dest, api_units='m'):
    url = MAIN_API + urllib.parse.urlencode({
        "key": API_KEY, 
        "from": orig, 
        "to": dest, 
        "unit": api_units
    })
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        json_data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка запроса к API: {e}"}

    json_status = json_data.get("info", {}).get("statuscode")
    
    if json_status == 0:
        return {
            "status": "success",
            "orig": orig,
            "dest": dest,
            "duration": json_data["route"]["formattedTime"],
            "distance": json_data["route"]["distance"],
            "fuel_used": json_data["route"]["fuelUsed"],
            "maneuvers": [
                {"narrative": m["narrative"], "distance": m["distance"]} 
                for m in json_data["route"]["legs"][0]["maneuvers"]
            ],
            "unit": "км" if api_units == 'm' else "миль"
        }
    else:
        error_message = json_data.get("info", {}).get("messages", ["Неизвестная ошибка"])[0]
        return {"error": f"Ошибка API (Код {json_status}): {error_message}"}