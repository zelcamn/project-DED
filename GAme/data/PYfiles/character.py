import pygame
from gameConfig import *
from numpy import interp
from main import load_image


class Character(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("H:\project-DED\GAme\data\PYfiles\hero_right.jpg")
        self.rect = self.image.get_rect()
        self.x, self.y = pos

        self.killed = False
        self.orientation = 0
        self.isphysic = True
        self.speedX = 0
        self.speedY = 0

    def pos(self):
        return self.x, self.y

    def movement(self, thread, speed):
        if thread == 0:
            if self.isphysic:
                pass
            self.x += speed

        if thread == 1:
            if self.isphysic:
                pass
            self.x -= speed

        if thread == 3:
            if self.isphysic:
                pass
            self.y -= speed

        if thread == 4:
            if self.isphysic:
                pass
            self.y += speed

        if self.isphysic:
            if not self.collision(AllSprites):
                self.y += playerSpeed

    def collision(self, Object):
        if pygame.sprite.spritecollideany(self, Object):
            return True
        else:
            return False

    def update(self):
        pass

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.x, self.y))





# class Plaer(pygame.sprite.Sprite):
#     image_rigth = load_image("hero_right.jpg", colorkey="black")
#     image_left = load_image("hero_left.jpg", colorkey="black")
#
#     def __init__(self, pos):
#         super().__init__(level.plaer_group)
#         self.image = Plaer.image_rigth
#         self.rect = self.image.get_rect()
#
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#         self.a_x = 0
#         self.a_y = 0
#         self.onLader = False
#         self.step = 1
#         self.killed = False
#         # Характеристики
#         self.speed_x = 5
#         self.obj_spd = 5
#         self.obj_live = 10
#         self.obj_heigth = 40
#         self.obj_type = Objectile
#
#     def reload(self):
#         level.plaer_group.add(self)
#         if pygame.sprite.spritecollide(self, level.mask_platforms, False):
#             self.rect.x = 10
#             self.rect.y = 10
#
#     def update(self, *args):
#         for i in range(abs(self.a_x)):
#             if self.a_x > 0:
#                 if not(pygame.sprite.spritecollide(self, level.horisontal_platform_left, False)):
#                     self.rect.x += 1 * (self.a_x / abs(self.a_x))
#             if self.a_x < 0:
#                 if not(pygame.sprite.spritecollide(self, level.horisontal_platform_rigth, False)):
#                     self.rect.x += 1 * (self.a_x / abs(self.a_x))
#         if self.a_y > 0:
#             self.step = 1
#         elif self.a_y < 0:
#             self.step = -1
#         for i in range(abs(self.a_y)):
#             self.rect.y += 1 * self.step
#             if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
#                 break
#             if pygame.sprite.spritecollide(self, level.vertical_platforms_down, False):
#                 self.a_y = 1
#         if not(pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
#             self.a_y += 1
#         else:
#             self.a_y = 0
#
#         if pygame.sprite.spritecollide(self, level.enemy_group, False):
#             self.killed = True
#             self.kill()
#
#     def set_pos(self, pos):
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#
#     def get_pos(self):
#         return (self.rect.x, self.rect.y)
#
#     def move(self, event):
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_a:
#                 self.a_x = -self.speed_x
#                 self.image = Plaer.image_left
#                 self.obj_spd = -5
#             if event.key == pygame.K_d:
#                 self.a_x = self.speed_x
#                 self.image = Plaer.image_rigth
#                 self.obj_spd = 5
#             if event.key == pygame.K_SPACE:
#                 if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
#                     self.a_y += -20
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_a:
#                 self.a_x = 0
#             if event.key == pygame.K_d:
#                 self.a_x = 0
#
#     def summon_objectile(self):
#         if self.obj_spd > 0:
#             self.obj_type((self.rect.x + 40, self.rect.y + 20 - self.obj_heigth // 2),
#                           self.obj_spd,
#                           self.obj_live,
#                           self.obj_heigth)
#         if self.obj_spd < 0:
#             self.obj_type((self.rect.x, self.rect.y + 20 - self.obj_heigth // 2),
#                           self.obj_spd,
#                           self.obj_live,
#                           self.obj_heigth)
#
#
# class Enemy(pygame.sprite.Sprite):
#     image_right = load_image("zlov_right.png", colorkey="black")
#     image_left = load_image("zlov_left.png", colorkey="black")
#
#     def __init__(self, pos):
#         super().__init__(level.enemy_group)
#         self.image = Enemy.image_left
#         self.rect = self.image.get_rect()
#
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#         self.a_x = 0
#         self.a_y = 0
#         self.onLader = False
#         self.step = 1
#         self.speed_x = 1
#         self.killed = False
#
#     def update(self, *args):
#         self.move()
#         for i in range(abs(self.a_x)):
#             if self.a_x > 0:
#                 if not (pygame.sprite.spritecollide(self, level.horisontal_platform_left, False)):
#                     self.rect.x += 1 * (self.a_x / abs(self.a_x))
#             if self.a_x < 0:
#                 if not (pygame.sprite.spritecollide(self, level.horisontal_platform_rigth, False)):
#                     self.rect.x += 1 * (self.a_x / abs(self.a_x))
#         if self.a_y > 0:
#             self.step = 1
#         elif self.a_y < 0:
#             self.step = -1
#         for i in range(abs(self.a_y)):
#             self.rect.y += 1 * self.step
#             if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
#                 break
#             if pygame.sprite.spritecollide(self, level.vertical_platforms_down, False):
#                 self.a_y = 1
#         if not(pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
#             self.a_y += 1
#         else:
#             self.a_y = 0
#
#         if pygame.sprite.spritecollide(self, level.objectile_group, True):
#             self.killed = True
#             self.kill()
#
#     def set_pos(self, pos):
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#
#     def move(self):
#         possitinal_pos = plaer.get_pos()[0]
#         if possitinal_pos > self.rect.x:
#             self.a_x = self.speed_x
#             self.image = self.image_right
#         if possitinal_pos < self.rect.x:
#             self.a_x = -self.speed_x
#             self.image = self.image_left
