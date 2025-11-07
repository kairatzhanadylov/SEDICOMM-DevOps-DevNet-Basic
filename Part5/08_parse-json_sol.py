# import requests
# import urllib.parse

# main_api = "https://mapquestapi.com/directions/v2/route?"
# key = "YOUR_API_KEY_HERE"
# exit = ['q', 'quit']

# while True:
#     orig = input("Starting Location: ")
#     dest = input("Destination: ")
#     url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest}) 
#     print("URL: " + (url))
#     json_data = requests.get(url).json()
#     json_status = json_data["info"]["statuscode"]
#     if orig.lower() in exit or dest.lower() in exit:
#         break
#     if json_status == 0:
#         print("API Status: " + str(json_status) + " = A successful route call.\n")
#         print("Directions from " + (orig) + " to " + (dest))
#         print("Trip Duration: " + (json_data["route"]["formattedTime"]))
#         print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
#         print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)) + "\n")
#         print("=============================================")
#         for each in json_data["route"]["legs"][0]["maneuvers"]:
#             print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
#         print("=============================================\n")
#     else:
#         print("Status Code: " + str(json_status) + " \n")



import requests
import urllib.parse

main_api = "https://mapquestapi.com/directions/v2/route?"
key = "YOUR_API_KEY_HERE" 
exit_commands = ['q', 'quit']

while True:
    unit_choice = input("Выберите систему измерений (m - метрическая, i - имперская): ").lower()
    if unit_choice == 'm':
        api_units = 'm' 
        distance_unit = "км"
        fuel_unit = "литров"
        break
    elif unit_choice == 'i':
        api_units = 'k' 
        distance_unit = "миль"
        fuel_unit = "галлонов"
        break
    elif unit_choice in exit_commands:
        print("Выход из программы.")
        exit() 
    else:
        print("Неверный ввод. Пожалуйста, введите 'm', 'i' или 'q/quit'.")

while True:
    orig = input("Starting Location: ")
    dest = input("Destination: ")
    
    if orig.lower() in exit_commands or dest.lower() in exit_commands:
        print("Выход из программы.")
        break

    url = main_api + urllib.parse.urlencode({
        "key": key, 
        "from": orig, 
        "to": dest, 
        "unit": api_units  
    }) 
    print("URL: " + (url))
    
    try:
        json_data = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        continue
        
    json_status = json_data.get("info", {}).get("statuscode")
    
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration: " + (json_data["route"]["formattedTime"]))

        distance_val = json_data["route"]["distance"]
        fuel_val = json_data["route"]["fuelUsed"]
        
        print(f"Расстояние: {distance_val:.2f} {distance_unit}")
        print(f"Расход топлива: {fuel_val:.2f} {fuel_unit}\n")
        
        print("=============================================")
      
        if "legs" in json_data["route"] and len(json_data["route"]["legs"]) > 0:
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                maneuver_distance = each["distance"]
                print(f"{each['narrative']} ({maneuver_distance:.2f} {distance_unit})")
        
        print("=============================================\n")
    else:
        error_message = json_data.get("info", {}).get("messages", ["Неизвестная ошибка"])[0]
        print(f"Status Code: {json_status}. Сообщение: {error_message} \n")