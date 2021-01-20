import pygame
from gameConfig import *
from config import *
import character
import sys, os


def load_image(name, colorkey=None):
    fullname = os.path.join('..', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def render(arr_groups, screen):
    if not(isinstance(arr_groups, list)):
        raise TypeError("arr_groups must be list")
    for group in arr_groups:
        if isinstance(group, pygame.sprite.Group):
            group.draw(screen)
        else:
            print("error of layer number", arr_groups.index(group))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    player = character.Character((20, 20))
    clock = pygame.time.Clock()
    running = True
    playerGroup = pygame.sprite.Group(player)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_w:
                player.movement(0, 10)
                print(player.x, player.y)
        screen.fill('gray')
        render([playerGroup], screen)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()