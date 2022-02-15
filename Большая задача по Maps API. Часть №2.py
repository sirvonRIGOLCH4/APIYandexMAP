import requests
import pygame
import os
import sys

spn = [0.05, 0.05]
coords = [40.403477, 56.144662]


def show_map():
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

    picture = pygame.image.load('map.png')
    # Удаляем за собой файл с изображением.
    os.remove('map.png')

    return picture


def change_zoom(flag, coeff):
    spn2 = coeff
    if flag:
        spn2 = [spn2[0] * 2, spn2[1] * 2]
    else:
        spn2 = [spn2[0] / 2, spn2[1] / 2]
    return spn2


# Инициализируем pygame
pygame.init()
width = 600
height = 450
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption('APIYandexMAP')

picture = show_map()

running = True
while running:
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(picture, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn = change_zoom(True, spn)
                picture = show_map()
            elif event.key == pygame.K_PAGEDOWN:
                spn = change_zoom(False, spn)
                picture = show_map()
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
pygame.quit()
