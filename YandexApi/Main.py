import requests

API_KEY = '___________________-'
url = "https://geocode-maps.yandex.ru/1.x/"
params = {
    'apikey': API_KEY,
    'geocode': 'Москва',
    'format': 'json'
}

response = requests.get(url, params=params)
data = response.json()

print(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])