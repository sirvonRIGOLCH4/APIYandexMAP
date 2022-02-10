import requests
import pygame
import os
import sys


spn = [0.05, 0.05]

coords = [40.403477, 56.144662]

maps_server = 'http://static-maps.yandex.ru/1.x/'

map_params = {
    'll': str(coords[0]) + ',' + str(coords[1]),
    'spn': str(spn[0]) + ',' + str(spn[1]),
    'l': 'map'}

response = requests.get(maps_server, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
width = 600
height = 450
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption('APIYandexMAP')
picture = pygame.image.load('map.png')

running = True
while running:
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
