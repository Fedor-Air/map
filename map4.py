import os
import sys
import pygame
import requests


class MapParams:
    def __init__(self):
        self.type = 'map'
        self.scale = 10
        self.coord = [37.620070, 55.753630]
        self.step = 1

    def update(self, event):
        print(event)
        print(self.coord)
        print(pygame.mouse.get_pos())
        print(pygame.KEYUP, pygame.MOUSEBUTTONUP)
        print(event.type)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP and self.scale < 19:    # K_KP9, K_PAGEUP
                self.scale += 1
            elif event.key == pygame.K_PAGEDOWN and self.scale > 2:    # K_KP3, K_PAGEDOWN
                self.scale -= 1
            elif event.key == pygame.K_LEFT:
                self.coord[0] -= (20 - self.scale) ** 2 / 120
            elif event.key == pygame.K_RIGHT:
                self.coord[0] += (20 - self.scale) ** 2 / 120
            elif event.key == pygame.K_UP and self.coord[1] < 85:
                self.coord[1] += (20 - self.scale) ** 2 / 300
            elif event.key == pygame.K_DOWN and self.coord[1] > -85:
                self.coord[1] -= (20 - self.scale) ** 2 / 300
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if 0 <= mouse[0] <= 200 and 450 <= mouse[1] <= 500:
                self.type = 'map'
            elif 201 <= mouse[0] <= 400 and 450 <= mouse[1] <= 500:
                self.type = 'sat'
            elif 401 <= mouse[0] <= 600 and 450 <= mouse[1] <= 500:
                self.type = 'sat,skl'


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
    screen = pygame.display.set_mode([600, 500])
    mp = MapParams()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type in (pygame.KEYUP, pygame.MOUSEBUTTONUP):
            mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        screen.blit(pygame.font.SysFont('Corbel', 35).render('Схема', True, (255, 255, 255)), (0, 450))
        screen.blit(pygame.font.SysFont('Corbel', 35).render('Спутник', True, (255, 255, 255)), (201, 450))
        screen.blit(pygame.font.SysFont('Corbel', 35).render('Гибрид', True, (255, 255, 255)), (401, 450))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
