import os
import sys
from random import randint

import pygame
import pytmx


width, height = 600, 600

pygame.init()
sc = pygame.display.set_mode((width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, heigth, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((width, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("gray")
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Mask_Platform(pygame.sprite.Sprite):
    def __init__(self, pos, group, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Plaer(pygame.sprite.Sprite):
    image_rigth = load_image("hero_right.jpg", colorkey="black")
    image_left = load_image("hero_left.jpg", colorkey="black")

    def __init__(self, pos):
        super().__init__(level.plaer_group)
        self.image = Plaer.image_rigth
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.a_x = 0
        self.a_y = 0
        self.onLader = False
        self.step = 1
        self.killed = False
        # Характеристики
        self.speed_x = 5
        self.obj_spd = 5
        self.obj_live = 10
        self.obj_heigth = 40
        self.obj_type = Objectile

    def reload(self):
        level.plaer_group.add(self)
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.rect.x = 10
            self.rect.y = 10

    def update(self, *args):
        for i in range(abs(self.a_x)):
            if self.a_x > 0:
                if not(pygame.sprite.spritecollide(self, level.horisontal_platform_left, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
            if self.a_x < 0:
                if not(pygame.sprite.spritecollide(self, level.horisontal_platform_rigth, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
        if self.a_y > 0:
            self.step = 1
        elif self.a_y < 0:
            self.step = -1
        for i in range(abs(self.a_y)):
            self.rect.y += 1 * self.step
            if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
                break
            if pygame.sprite.spritecollide(self, level.vertical_platforms_down, False):
                self.a_y = 1
        if not(pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        if pygame.sprite.spritecollide(self, level.enemy_group, False):
            self.killed = True
            self.kill()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.a_x = -self.speed_x
                self.image = Plaer.image_left
                self.obj_spd = -5
            if event.key == pygame.K_d:
                self.a_x = self.speed_x
                self.image = Plaer.image_rigth
                self.obj_spd = 5
            if event.key == pygame.K_SPACE:
                if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
                    self.a_y += -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.a_x = 0
            if event.key == pygame.K_d:
                self.a_x = 0

    def summon_objectile(self):
        if self.obj_spd > 0:
            self.obj_type((self.rect.x + 40, self.rect.y + 20 - self.obj_heigth // 2),
                          self.obj_spd,
                          self.obj_live,
                          self.obj_heigth)
        if self.obj_spd < 0:
            self.obj_type((self.rect.x, self.rect.y + 20 - self.obj_heigth // 2),
                          self.obj_spd,
                          self.obj_live,
                          self.obj_heigth)


class Enemy(pygame.sprite.Sprite):
    image_right = load_image("zlov_right.png", colorkey="black")
    image_left = load_image("zlov_left.png", colorkey="black")

    def __init__(self, pos):
        super().__init__(level.enemy_group)
        self.image = Enemy.image_left
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.a_x = 0
        self.a_y = 0
        self.onLader = False
        self.step = 1
        self.speed_x = 1
        self.killed = False

    def update(self, *args):
        self.move()
        for i in range(abs(self.a_x)):
            if self.a_x > 0:
                if not (pygame.sprite.spritecollide(self, level.horisontal_platform_left, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
            if self.a_x < 0:
                if not (pygame.sprite.spritecollide(self, level.horisontal_platform_rigth, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
        if self.a_y > 0:
            self.step = 1
        elif self.a_y < 0:
            self.step = -1
        for i in range(abs(self.a_y)):
            self.rect.y += 1 * self.step
            if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
                break
            if pygame.sprite.spritecollide(self, level.vertical_platforms_down, False):
                self.a_y = 1
        if not(pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        if pygame.sprite.spritecollide(self, level.objectile_group, True):
            self.killed = True
            self.kill()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self):
        possitinal_pos = plaer.get_pos()[0]
        if possitinal_pos > self.rect.x:
            self.a_x = self.speed_x
            self.image = self.image_right
        if possitinal_pos < self.rect.x:
            self.a_x = -self.speed_x
            self.image = self.image_left


class Objectile(pygame.sprite.Sprite):
    def __init__(self, pos, a_x, time_of_live, heigth):
        super().__init__(level.objectile_group)
        self.image = pygame.Surface((10, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("white")

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.a_x = a_x
        self.counter = 0
        self.counter_max = time_of_live

    def update(self, *args):
        self.rect.x += self.a_x
        self.counter += 1
        if self.counter >= self.counter_max:
            self.kill()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Level:
    def __init__(self, file, wrez, hrez, summon_time=500, end_time=500):
        self.enemys = []
        self.summon_time = summon_time
        self.end_time = end_time
        self.end_time_run = False

        self.map = pytmx.load_pygame(f"{file}")

        self.width_res = wrez
        self.heigth_res = hrez

        self.plaer_group = pygame.sprite.Group()
        self.vertical_platforms_up = pygame.sprite.Group()
        self.vertical_platforms_down = pygame.sprite.Group()
        self.horisontal_platform_left = pygame.sprite.Group()
        self.horisontal_platform_rigth = pygame.sprite.Group()
        self.mask_platforms = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.objectile_group = pygame.sprite.Group()

        self.arr_groups = [self.plaer_group, self.vertical_platforms_up,
        self.vertical_platforms_down, self.horisontal_platform_left,
        self.horisontal_platform_rigth, self.enemy_group, self.objectile_group, self.mask_platforms]

        print(*self.map, sep="\n")
        for y in range(-1, self.map.height + 1):
            for x in range(-1, self.map.width + 1):
                print(y, x)
                if 0 <= y < self.map.height and 0 <= x < self.map.width:
                    image = self.map.get_tile_image(x, y, 0)
                    if not(image is None):
                        self.create_platform(self.width_res, self.heigth_res, (x * self.width_res, y * self.heigth_res),
                                                                           image)
                else:
                    self.create_platform(self.width_res, self.heigth_res,
                                         (x * self.width_res, y * self.heigth_res),
                                         pygame.Surface((int(self.width_res), int(self.heigth_res))))

        total_level_width = self.map.width * self.width_res  # Высчитываем фактическую ширину уровня
        total_level_height = self.map.height * self.heigth_res  # высоту

        self.camera = Camera(camera_configure, total_level_width, total_level_height)

    def summon_vragov(self):
        pass

    def create_platform(self, width, heigth, pos, image):
        Platform(width - 2, 1, (pos[0] + 1, pos[1]), self.vertical_platforms_up)
        Platform(width - 2, 1,
                 (pos[0] + 1, pos[1] + heigth - 1),
                 self.vertical_platforms_down)
        Platform(1, heigth - 2,
                 (pos[0], pos[1] + 1),
                 self.horisontal_platform_left)
        Platform(1, heigth - 2,
                 (pos[0] + width - 1, pos[1] + 1),
                 self.horisontal_platform_rigth)
        Mask_Platform(pos, self.mask_platforms, image)

    def render(self, screen):
        if not (isinstance(self.arr_groups, list)):
            raise TypeError("arr_groups must be list")
        for group in self.arr_groups:
            if isinstance(group, pygame.sprite.Group):
                for sprite in group:
                    screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                print("Erore of layer number", self.arr_groups.index(group))

    def update(self):
        self.camera.update(plaer)
        if not (isinstance(self.arr_groups, list)):
            raise TypeError("arr_groups must be list")
        for group in self.arr_groups:
            if isinstance(group, pygame.sprite.Group):
                group.update()
            else:
                print("Erore of layer number", self.arr_groups.index(group))

    def end(self):
        for i in self.enemys:
            if not(i.killed):
                return False
        return True


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + width / 2, -t + height / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - width), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - height), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def change_level():
    global level
    level = Level(f"data\levels\\1.tmx", 60, 60)


clock = pygame.time.Clock()
level = 0
change_level()
counter_start = 0
counter_end = 0
plaer = Plaer((10, 10))
running = True
enemy_counter = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or plaer.killed:
            running = False
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            plaer.move(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            plaer.summon_objectile()
    # if counter_start <= level.summon_time:
        #     counter_start += 1
    #     print(counter_start)
    # elif counter_start == level.summon_time + 1:
        #     level.summon_vragov()
    #     counter_start += 1
    # if counter_end <= level.end_time:
        #     counter_end += 1
    #     print(counter_end)
    # elif all(list(map(lambda x: x.killed, level.enemys))) and counter_end == level.end_time + 1 \
        #         and counter_start >= level.summon_time:
        #     change_level()
        #     plaer.reload()
        #    counter_start = 0
    #     counter_end = 0
    sc.fill("black")
    level.update()
    level.render(sc)
    pygame.display.flip()
    clock.tick(100)