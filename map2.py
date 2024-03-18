import os
import sys
import pygame
import requests


class MapParams:
    def __init__(self):
        self.type = 'map'
        self.scale = 10
        self.coord = [37.620070, 55.753630]

    def update(self, event):
        if event.key == pygame.K_PAGEUP and self.scale < 19:
            self.scale += 1
        elif event.key == pygame.K_PAGEDOWN and self.scale > 2:
            self.scale -= 1


def load_map(mp):
    map_request = f'http://static-maps.yandex.ru/1.x/?ll={mp.coord[0]},{mp.coord[1]}&z={mp.scale}&l={mp.type}'
    resp = requests.get(map_request)

    if not resp:
        print('Ошибка выполнения запроса:')
        print(map_request)
        print(f'Http статус: {resp.status_code} ({resp.reason})')
        sys.exit(1)

    map_file = "map.png"

    try:
        with open(map_file, "wb") as file:
            file.write(resp.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode([600, 450])
    mp = MapParams()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
