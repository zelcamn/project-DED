# # from GAme.data.PYfiles.levelMachine import Level
# # from GAme.data.PYfiles.character import Plaer, Enemy
# # import os
# # import sys
# # from random import randint
#
# import pygame
#
# pygame.init()
# sc = pygame.display.set_mode((width, height))
#
#
# def load_image(name, colorkey=None):
#     fullname = os.path.join('..', name)
#     # если файл не существует, то выходим
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#     if colorkey is not None:
#         image = image.convert()
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey)
#     else:
#         image = image.convert_alpha()
#     return image
#
#
#
#
# def update(arr_groups):
#     if not(isinstance(arr_groups, list)):
#         raise TypeError("arr_groups must be list")
#     for group in arr_groups:
#         if isinstance(group, pygame.sprite.Group):
#             group.update()
#         else:
#             print("Erore of layer number", arr_groups.index(group))
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, width, heigth, pos, group):
#         super().__init__(group)
#         self.image = pygame.Surface((width, heigth))
#         self.rect = self.image.get_rect()
#         self.image.fill("gray")
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#
#
# class Objectile(pygame.sprite.Sprite):
#     def __init__(self, pos, a_x, time_of_live, heigth):
#         super().__init__(level.objectile_group)
#         self.image = pygame.Surface((10, heigth))
#         self.rect = self.image.get_rect()
#         self.image.fill("white")
#
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#
#         self.a_x = a_x
#         self.counter = 0
#         self.counter_max = time_of_live
#
#     def update(self, *args):
#         self.rect.x += self.a_x
#         self.counter += 1
#         if self.counter >= self.counter_max:
#             self.kill()
#
#     def set_pos(self, pos):
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#
#
# def change_level():
#     global level
#     level = Level(f"data\levels\\{str(randint(1, 5))}.txt")
#
#
# clock = pygame.time.Clock()
# level = 0
# change_level()
# counter_start = 0
# counter_end = 0
# plaer = Plaer((10, 10))
# running = True
# enemy_counter = 1
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or plaer.killed:
#             running = False
#         if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
#             plaer.move(event)
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             plaer.summon_objectile()
#     if counter_start <= level.summon_time:
#         counter_start += 1
#         print(counter_start)
#     elif counter_start == level.summon_time + 1:
#         level.summon_vragov()
#         counter_start += 1
#     if counter_end <= level.end_time:
#         counter_end += 1
#         print(counter_end)
#     elif all(list(map(lambda x: x.killed, level.enemys))) and counter_end == level.end_time + 1 \
#             and counter_start >= level.summon_time:
#         change_level()
#         plaer.reload()
#         counter_start = 0
#         counter_end = 0
#     sc.fill("black")
#     level.update()
#     level.render(sc)
#     pygame.display.flip()
#     clock.tick(100)