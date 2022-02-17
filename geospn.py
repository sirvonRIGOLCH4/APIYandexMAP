import requests
from dotenv import load_dotenv
from os import environ  # для чтения переменных среды окружения

load_dotenv("env")  # берем свой файл
#print(environ["API_KEY"])  # проверяем доступ к ключу
#static_maps_SERVICE = 'https://static-maps.yandex.ru/1.x/'
geocoder_SERVICE = f"http://geocode-maps.yandex.ru/1.x/"
API_KEY = environ["API_KEY"]


# Получаем параметры объекта для рисования карты вокруг него.
def llspan(address):
    # Собираем запрос для геокодера.
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    # Выполняем запрос.
    response = requests.get(geocoder_SERVICE, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_SERVICE)
        print("Http статус:", response.status_code, "(", response.reason, ")")

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_adress = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

    if not toponym:
        return None, None

    # Координаты центра топонима:
    toponym_coordinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_lon, toponym_lat = toponym_coordinates.split(" ")
    ll = ",".join([toponym_lon, toponym_lat])

    envelope = toponym["boundedBy"]["Envelope"]
    lowerCorner, left = envelope["lowerCorner"].split(" ")
    upperCorner, right = envelope["upperCorner"].split(" ")
    delta_x = abs(float(right) - float(left)) / 2.0
    delta_y = abs(float(upperCorner) - float(lowerCorner)) / 2.0

    spn = f"{delta_x},{delta_y}"

    return float(toponym_lon), float(toponym_lat)


def adres(address):
    # Собираем запрос для геокодера.
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    # Выполняем запрос.
    response = requests.get(geocoder_SERVICE, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_SERVICE)
        print("Http статус:", response.status_code, "(", response.reason, ")")

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_adress = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

    if not toponym:
        return None

    return toponym_adress


def post(address):
    # Собираем запрос для геокодера.
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    # Выполняем запрос.
    response = requests.get(geocoder_SERVICE, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_SERVICE)
        print("Http статус:", response.status_code, "(", response.reason, ")")

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_adress = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

    if not toponym:
        return None

    try:
        return toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"] + ", " + toponym_adress
    except KeyError:
        return toponym_adress
