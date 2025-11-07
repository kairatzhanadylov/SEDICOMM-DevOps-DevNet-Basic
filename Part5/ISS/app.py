# import requests
# import time

# def get_iss_data():
#     iss_pass_url = "http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74"
#     print(f"Обращение к: {iss_pass_url}")
#     try:
#         response_pass = requests.get(iss_pass_url)
#         response_pass.raise_for_status()
#         data_pass = response_pass.json()
        
#         if data_pass['message'] == 'success':
#             passes = data_pass['response']
#             num_passes = len(passes)
            
#             request_lat = data_pass['request']['latitude']
#             request_lon = data_pass['request']['longitude']
            
#             print("---")
#             print("Прогнозы пролета МКС")
#             print(f"Количество пролетов над координатами ({request_lat}, {request_lon}) (Нью-Йорк, США): **{num_passes}**")
            
#             if passes:
#                 first_pass_risetime = passes[0]['risetime']
#                 first_pass_duration = passes[0]['duration']
#                 risetime_formatted = time.ctime(first_pass_risetime)
#                 print(f"Первый пролет:")
#                 print(f"  - Время подъема (Unix): {first_pass_risetime}")
#                 print(f"  - Время подъема (читаемое): {risetime_formatted}")
#                 print(f"  - Продолжительность (секунды): {first_pass_duration}")
#         else:
#             print(f"Ошибка при получении данных о пролетах: {data_pass['message']}")
            
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе данных о пролетах МКС: {e}")

#     iss_now_url = "http://api.open-notify.org/iss-now.json"
#     print("\n---")
#     print(f"Обращение к: {iss_now_url}")
#     try:
#         response_now = requests.get(iss_now_url)
#         response_now.raise_for_status()
#         data_now = response_now.json()

#         if data_now['message'] == 'success':
#             latitude = data_now['iss_position']['latitude']
#             longitude = data_now['iss_position']['longitude']
#             timestamp = data_now['timestamp']
            
#             print("Текущее местоположение МКС")
#             print(f"Широта: **{latitude}**")
#             print(f"Долгота: **{longitude}**")
#             print(f"Метка времени: {timestamp} ({time.ctime(timestamp)})")
#         else:
#             print(f"Ошибка при получении текущего местоположения МКС: {data_now['message']}")
            
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе текущего местоположения МКС: {e}")

#     astros_url = "http://api.open-notify.org/astros.json"
#     print("\n---")
#     print(f"Обращение к: {astros_url}")
#     try:
#         response_astros = requests.get(astros_url)
#         response_astros.raise_for_status()
#         data_astros = response_astros.json()

#         if data_astros['message'] == 'success':
#             number_of_people = data_astros['number']
            
#             print("Люди в космосе")
#             print(f"Общее количество людей в космосе: **{number_of_people}**")
#             print("Список людей:")
#             for person in data_astros['people']:
#                 print(f"  - {person['name']} (Корабль: {person['craft']})")
#         else:
#             print(f"Ошибка при получении данных о людях в космосе: {data_astros['message']}")

#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе данных о людях в космосе: {e}")

# if __name__ == "__main__":
#     get_iss_data()

import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 
ISS_NOW_URL = "http://api.open-notify.org/iss-now.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iss-location', methods=['GET'])
def get_iss_location():
    try:
        response = requests.get(ISS_NOW_URL)
        response.raise_for_status() 
        data = response.json()
        
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        
        return jsonify({
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': data['timestamp']
        })

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных МКС: {e}")
        return jsonify({'error': 'Не удалось получить данные МКС'}), 500

if __name__ == '__main__':
    app.run(debug=True)