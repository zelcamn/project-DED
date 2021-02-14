import math
import os
import random
import sys

import pygame
import pytmx

import json

pygame.init()
pygame.mixer.init()
width, height = 600, 600
sc = pygame.display.set_mode((width, height))

TILE_DICT = {"platform": 3,
             "zlov": 2,
             "spawn": 3,
             "door": 4,
             "heard": 6,
             "chest": 5}


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


class Music:
    pygame.mixer.music.load('data/gamemus1.mp3')  # загружем музыку, по другому я не мгогу её остановить
    gamemusic = pygame.mixer.music
    pygame.mixer.music.set_volume(0.5)
    shoot = pygame.mixer.Sound('data/shot.wav')  # звуки можно не загружать
    povrejen = pygame.mixer.Sound('data/povrejen.mp3')
    gameover = pygame.mixer.Sound('data/gameover.mp3')
    zlovded = pygame.mixer.Sound('data/zlovded.mp3')
    healthup = pygame.mixer.Sound('data/healthup.mp3')
    meinmusic = pygame.mixer.Sound(f"data/m{random.randint(1, 3)}.mp3")


class Platform(pygame.sprite.Sprite):
    def __init__(self, width_of_platform, heigth, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((width_of_platform, heigth))
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


class Shower(pygame.sprite.Sprite):
    def __init__(self, pos, group, target):
        super().__init__(group)
        self.f1 = pygame.font.Font(None, SHOWER_SIZE)
        self.target = target
        text1 = self.f1.render("", True, (180, 0, 0))
        self.image = text1
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        pass


class Coin_Shower(Shower):
    def __init__(self, pos, group, target):
        super().__init__(pos, group, target)

    def update(self):
        text1 = self.f1.render(str(self.target.coins), True, COINS_SHOWER_COLOR)
        self.image = text1
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Helth_Shower(pygame.sprite.Sprite):
    def __init__(self, pos, group, target):
        self.target = target
        self.pos = pos
        super().__init__(group)
        self.image = pygame.Surface((self.target.health_max * HEALTH_SHOWER_SIZE, HEALTH_SHOWER_SIZE))
        self.image.fill("gray")
        for i in range(HEALTH_SHOWER_SIZE):
            for j in range(HEALTH_SHOWER_SIZE * self.target.health):
                self.image.set_at((j, i), "red")
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        self.image = pygame.Surface((self.target.health_max * HEALTH_SHOWER_SIZE, HEALTH_SHOWER_SIZE))
        self.image.fill("gray")
        for i in range(HEALTH_SHOWER_SIZE):
            for j in range(HEALTH_SHOWER_SIZE * self.target.health):
                self.image.set_at((j, i), "red")
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Plaer(pygame.sprite.Sprite):
    def __init__(self, pos, weapon, animations):
        super().__init__()
        self.animations = animations
        self.image_stack = [self.animations["static"]]
        self.image = self.image_stack.pop(0)
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
        self.obj_spd = weapon.obj_spd
        self.obj_live = weapon.obj_live
        self.obj_heigth = weapon.obj_heigth
        self.obj_type = weapon.obj_type
        self.a_obj_spd = self.obj_spd
        self.damage = weapon.damage

        self.coins = 0
        self.health = START_HEALTH
        self.health_max = START_HEALTH_MAX
        self.invisibility_counter_max = START_INVISIBILITY_MAX
        self.invisibility_counter = self.invisibility_counter_max

        self.damage_counter = 0
        self.killed_counter = 0

        self.tick_counter = 0
        self.tick_counter_max = 5

        self.image_counter = 0
        self.direction = True

    def reload(self):
        level.plaer_group.add(self)
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.rect.x = 10
            self.rect.y = 10

    def update(self, *args):
        for i in pygame.sprite.spritecollide(self, level.enemy_group, False):
            if self.invisibility_counter >= self.invisibility_counter_max:
                self.damage_counter += 1
                self.health -= 1
                self.a_y -= 20
                Music.povrejen.play()
                if self.health <= 0:
                    self.killed = True
                    self.kill()
                    Music.gameover.play()
                else:
                    self.invisibility_counter = 0

        if pygame.sprite.spritecollide(self, level.heath_group, True) and self.health < self.health_max:
            self.health += 1
            Music.healthup.play()

        for chest in pygame.sprite.spritecollide(self, level.chest_group, False):
            chest.summon_artefact()
            chest.kill()

        for artefact in pygame.sprite.spritecollide(self, level.artefact_group, False):
            self.speed_x += eval(artefact.arrey_of_changes.get("speed_x", "0"))
            self.obj_spd += eval(artefact.arrey_of_changes.get("obj_spd", "0"))
            self.obj_live += eval(artefact.arrey_of_changes.get("obj_live", "0"))
            self.obj_heigth += eval(artefact.arrey_of_changes.get("obj_heigth", "0"))
            self.obj_type = eval(artefact.arrey_of_changes.get("obj_type", "self.obj_type"))
            self.invisibility_counter_max += eval(artefact.arrey_of_changes.get("invisibility_counter_max", "0"))
            self.invisibility_counter += eval(artefact.arrey_of_changes.get("invisibility_counter", "0"))
            self.coins += eval(artefact.arrey_of_changes.get("coins", "0"))
            self.health += eval(artefact.arrey_of_changes.get("health", "0"))
            self.health_max += eval(artefact.arrey_of_changes.get("health_max", "0"))
            self.damage += eval(artefact.arrey_of_changes.get("damage", "0"))
            artefact.kill()

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
        for i in range(abs(int(self.a_y // 2))):
            self.rect.y += 1 * self.step
            if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
                break
            if pygame.sprite.spritecollide(self, level.vertical_platforms_down, False):
                self.a_y = 1
        if not (pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
            self.a_y += GRAVITY
        else:
            self.a_y = 0

        if self.invisibility_counter < self.invisibility_counter_max:
            self.invisibility_counter += 1

        if self.tick_counter > self.tick_counter_max:
            if abs(self.a_x) > 0:
                self.image_stack.append(self.animations["run"][self.image_counter % len(self.animations["run"])])
                self.image_counter += 1
            else:
                self.image_stack.append(self.animations["static"])
            try:
                self.image = self.image_stack.pop(0)
            except IndexError:
                pass
            if self.direction:
                self.image = pygame.transform.flip(self.image, True, False)
            self.tick_counter = 0
        else:
            self.tick_counter += 1

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.a_x = -self.speed_x
            if event.key == pygame.K_d:
                self.a_x = self.speed_x
            if event.key == pygame.K_SPACE:
                if pygame.sprite.spritecollide(self, level.vertical_platforms_up, False):
                    self.a_y -= JUMP_POWER
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.a_x = 0
            if event.key == pygame.K_d:
                self.a_x = 0

    def change_direction(self, pos, plaer_x_on_screen):
        x = pos[0]
        if x < plaer_x_on_screen:
            self.direction = True
            self.a_obj_spd = -1 * self.obj_spd
        else:
            self.direction = False
            self.a_obj_spd = self.obj_spd

    def summon_objectile(self, target_pos, real):
        self.image_stack = self.animations["attac"].copy()
        if self.a_obj_spd > 0:
            self.obj_type((self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2 - self.obj_heigth // 2),
                          self.a_obj_spd,
                          self.obj_live,
                          self.obj_heigth,
                          target_pos, real, self.damage)
        if self.a_obj_spd < 0:
            self.obj_type((self.rect.x, self.rect.y + self.rect.height // 2 - self.obj_heigth // 2),
                          self.a_obj_spd,
                          self.obj_live,
                          self.obj_heigth,
                          target_pos, real, self.damage)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, group, health):
        self.load_animations()
        super().__init__(group)
        self.image = self.animations["RUN"][0]
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.a_x = 0
        self.a_y = 0
        self.onLader = False
        self.step = 1
        self.speed_x = 1
        self.killed = False

        self.health = health + 1
        self.image_stack = []
        self.image_counter = 0

        self.tick_counter = 0
        self.tick_counter_max = 5

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
        if not (pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        for i in pygame.sprite.spritecollide(self, level.objectile_group, True):
            self.health -= i.damage
        if self.health <= 0:
            plaer.coins += COINS_4_ENEMY
            plaer.killed_counter += 1
            self.killed = True
            self.kill()
            Music.zlovded.play()

        if (abs(self.rect.x - plaer.rect.x) < STEP // 10 \
            or abs(self.rect.x - plaer.rect.x - plaer.rect.width) < STEP // 10) \
                and \
                (abs(self.rect.y - plaer.rect.y) < STEP // 10 \
                 or abs(self.rect.y - plaer.rect.y - plaer.rect.height) < STEP // 10):
            self.attact()

        if self.tick_counter > self.tick_counter_max:
            if abs(self.a_x) > 0:
                self.image_stack.append(self.animations["RUN"][self.image_counter % len(self.animations["RUN"])])
                self.image_counter += 1
            try:
                self.image = self.image_stack.pop(0)
            except IndexError:
                pass
            if self.a_x < 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.tick_counter = 0
        else:
            self.tick_counter += 1

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self):
        possitinal_pos = plaer.get_pos()[0]
        if possitinal_pos > self.rect.x:
            self.a_x = self.speed_x
        if possitinal_pos < self.rect.x:
            self.a_x = -self.speed_x

    def load_animations(self):
        global ENEMY_ANIMATIONS
        self.animations = {}
        for i in ENEMY_ANIMATIONS.keys():
            self.animations[i] = []
            for j in os.listdir(os.path.join("data", ENEMY_ANIMATIONS[i])):
                self.animations[i].append(pygame.transform.scale(load_image(f"{ENEMY_ANIMATIONS[i]}\\{j}"), (50, 50)))
        print(self.animations)

    def attact(self):
        self.image_stack = self.animations["ATTACK"] + self.image_stack


class Objectile(pygame.sprite.Sprite):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real, damage):
        super().__init__(level.objectile_group)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.a_x = a_x
        self.counter = 0
        self.counter_max = time_of_live
        self.damage = damage

    def update(self, *args):
        pass

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Objectile_Sword(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real, damage):
        self.image = pygame.Surface((10, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("white")
        self.heigth = heigth

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real, damage)

    def update(self, *args):
        self.rect.x += self.a_x
        self.counter += 1
        if self.counter >= self.counter_max:
            self.kill()


class Sword:
    obj_spd = 5
    obj_live = 10
    obj_heigth = 40
    obj_type = Objectile_Sword
    damage = 3


class Objectile_Bow(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real, damage):
        self.image = pygame.Surface((heigth, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("white")

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real, damage)

        dx = abs(real.x - target_pos[0])
        dy = abs(real.y - target_pos[1])
        self.a_y = 1

        if dx == 0:
            self.a_x = 0
            self.y_a = a_x
        else:
            angle = math.atan(dy / dx)
            self.a_x = a_x * math.cos(angle)
            if real.y < target_pos[1]:
                self.a_y = abs(a_x * math.sin(angle))
            else:
                self.a_y = -abs(a_x * math.sin(angle))

    def update(self, *args):
        self.rect.x += self.a_x
        self.rect.y += self.a_y // 1
        self.a_y += BOW_GRAVITY
        self.counter += 1
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.kill()


class Bow:
    obj_spd = 5
    obj_live = 10
    obj_heigth = 10
    obj_type = Objectile_Bow
    damage = 2


class Objectile_Gun(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real, damage):
        self.image = pygame.Surface((heigth, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("white")

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real, damage)

        dx = abs(real.x - target_pos[0])
        dy = abs(real.y - target_pos[1])
        self.a_y = 1

        if dx == 0:
            self.a_x = 0
            self.y_a = a_x
        else:
            angle = math.atan(dy / dx)
            self.a_x = a_x * math.cos(angle)
            if real.y < target_pos[1]:
                self.a_y = abs(a_x * math.sin(angle))
            else:
                self.a_y = -abs(a_x * math.sin(angle))

    def update(self, *args):
        self.rect.x += self.a_x
        self.rect.y += self.a_y // 1
        self.counter += 1
        if pygame.sprite.spritecollide(self, level.mask_platforms, False) or self.a_x == self.a_x == 0:
            self.kill()


class Gun:
    obj_spd = 5
    obj_live = 10
    obj_heigth = 10
    obj_type = Objectile_Gun
    damage = 2


class Artefact(pygame.sprite.Sprite):
    def __init__(self, pos, group, image, arrey_of_changes):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.arrey_of_changes = arrey_of_changes

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, group, image, artefact_group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.artefact_group = artefact_group
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def summon_artefact(self):
        artefact = ARTEFACTS[random.randrange(0, len(ARTEFACTS))]
        Artefact((self.pos[0], self.pos[1] - STEP * CHEST_ARTEFACT_DELAY), self.artefact_group, artefact[0],
                 artefact[1])


class Drop(pygame.sprite.Sprite):
    def __init__(self, pos, group, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Level:
    def __init__(self, file, wrez, hrez):
        self.enemys = []
        self.end_time_run = False
        print(file)
        self.map = pytmx.load_pygame(file)

        self.width_res = wrez
        self.heigth_res = hrez

        self.plaer_group = pygame.sprite.Group()
        self.aim_group = pygame.sprite.Group()
        self.vertical_platforms_up = pygame.sprite.Group()
        self.vertical_platforms_down = pygame.sprite.Group()
        self.horisontal_platform_left = pygame.sprite.Group()
        self.horisontal_platform_rigth = pygame.sprite.Group()
        self.mask_platforms = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.objectile_group = pygame.sprite.Group()
        self.door_group = pygame.sprite.Group()
        self.heath_group = pygame.sprite.Group()
        self.chest_group = pygame.sprite.Group()
        self.artefact_group = pygame.sprite.Group()

        self.arr_unstatick_groups = [self.plaer_group, self.vertical_platforms_up,
                                     self.vertical_platforms_down, self.horisontal_platform_left,
                                     self.horisontal_platform_rigth, self.enemy_group, self.heath_group,
                                     self.chest_group, self.artefact_group,
                                     self.objectile_group, self.mask_platforms, self.door_group]

        self.gui_group = pygame.sprite.Group()
        self.plaer_coins = Coin_Shower(COINS_SHOWER_POS, self.gui_group, plaer)
        self.plaer_helth = Helth_Shower(HEALTH_CHOWER_POS, self.gui_group, plaer)

        self.arr_statick_groups = [self.gui_group]

        self.start_pos = (0, 0)

        print(*self.map, sep="\n")
        for y in range(-1, self.map.height + 1):
            for x in range(-1, self.map.width + 1):
                if 0 <= y < self.map.height and 0 <= x < self.map.width:
                    image = self.map.get_tile_image(x, y, 0)
                    if not (image is None):
                        if self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["zlov"]:
                            self.enemys.append(
                                Enemy((x * self.width_res, y * self.heigth_res), self.enemy_group, LEVEL_COUNTER))
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["spawn"]:
                            self.start_pos = (x * self.width_res, y * self.heigth_res)
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["door"]:
                            self.create_door((x * self.width_res, y * self.heigth_res), image)
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["heard"]:
                            Drop((x * self.width_res, y * self.heigth_res), self.heath_group, image)
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["chest"]:
                            Chest((x * self.width_res, y * self.heigth_res), self.chest_group, image,
                                  self.artefact_group)
                        else:
                            self.create_platform(self.width_res, self.heigth_res,
                                                 (x * self.width_res, y * self.heigth_res),
                                                 image)
                else:
                    self.create_platform(self.width_res, self.heigth_res,
                                         (x * self.width_res, y * self.heigth_res),
                                         pygame.Surface((int(self.width_res), int(self.heigth_res))))

        total_level_width = self.map.width * self.width_res  # Высчитываем фактическую ширину уровня
        total_level_height = self.map.height * self.heigth_res  # высоту

        self.camera = Camera(camera_configure, total_level_width, total_level_height)

    def start(self):
        plaer.set_pos(self.start_pos)

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

    def create_door(self, pos, image):
        print("hi")
        Mask_Platform(pos, self.door_group, image)

    def render(self, screen):
        if not (isinstance(self.arr_unstatick_groups, list)):
            raise TypeError("arr_groups must be list")
        for usgroup in self.arr_unstatick_groups:
            if isinstance(usgroup, pygame.sprite.Group):
                for sprite in usgroup:
                    screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                print("Erore of layer number", self.arr_groups.index(usgroup))
        for sgroup in self.arr_statick_groups:
            if isinstance(usgroup, pygame.sprite.Group):
                sgroup.draw(screen)
            else:
                print("Erore of layer number", self.arr_groups.index(usgroup))

    def update(self):
        self.camera.update(plaer)
        if not (isinstance(self.arr_unstatick_groups, list)):
            raise TypeError("arr_groups must be list")
        for group in self.arr_unstatick_groups:
            if isinstance(group, pygame.sprite.Group):
                for sprite in group:
                    if self.camera.apply(sprite):
                        sprite.update()
            else:
                print("Erore of layer number", self.arr_groups.index(group))
        for sgroup in self.arr_statick_groups:
            if isinstance(sgroup, pygame.sprite.Group):
                sgroup.update()
            else:
                print("Erore of layer number", self.arr_groups.index(sgroup))

    def end(self):
        for i in self.enemys:
            if not (i.killed):
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


class Menu:
    def __init__(self, background, arr):
        self.background_group = pygame.sprite.Group()
        self.background_group.add(background)
        self.button_group = pygame.sprite.Group()
        self.stack = {}

        for i in arr:
            sprite = pygame.sprite.Sprite()
            sprite.image = i[0]
            sprite.rect = sprite.image.get_rect()
            print(sprite.rect.x, sprite.rect.y)
            sprite.rect.x = i[1]
            sprite.rect.y = i[2]
            self.button_group.add(sprite)
            self.stack[sprite] = i[3]

    def render(self, screen):
        self.background_group.draw(screen)
        self.button_group.draw(screen)

    def update(self, pos):
        for button in self.button_group:
            if button.rect.collidepoint(pos[0], pos[1]):
                self.stack[button]()


def generate_stack():
    global level_stack
    level_stack = [f"data\levels\\{i}.tmx" for i in range(1, 16)]
    random.shuffle(level_stack)


def change_level():
    global level, plaer, LEVEL_COUNTER, level_stack
    level = Level(level_stack.pop(0), 60, 60)
    if len(level_stack) <= 0:
        generate_stack()
    plaer.reload()
    LEVEL_COUNTER += 1
    level.start()


def change_hero_rigth():
    global choisen_character
    choisen_character += 1
    choisen_character = choisen_character % len(CHARACTERS)


def change_hero_left():
    global choisen_character
    choisen_character -= 1
    choisen_character = choisen_character % len(CHARACTERS)


def menu():
    surf = pygame.sprite.Sprite()
    surf.image = load_image("fone.png")
    Music.meinmusic.play()
    surf.rect = surf.image.get_rect()
    f1 = pygame.font.Font(None, 36)
    menu = Menu(surf, [[load_image("play.png", colorkey="white"), 150, 50, start_play],
                       [load_image("to_left.png", colorkey="white"), 50, 200, change_hero_left],
                       [load_image("to_rigth.png", colorkey="white"), width - 50 - 100, 200, change_hero_rigth],
                       [load_image("aboute_developers.png", colorkey="white"),
                                            width // 2 - 75, 400, aboute_razrabotchikav]]
                )
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos)
        menu.render(sc)
        sc.blit(pygame.transform.scale(CHARACTERS[choisen_character][2]["static"], (100, 100)), (width // 2 - 50, 200))
        text1 = f1.render(f"Золото: {COINS}", True,
                          (180, 0, 0))
        sc.blit(text1, (10, 10))
        pygame.display.flip()


def pause():
    global plaer, running_pause
    running_pause = True
    Music.gamemusic.pause()

    surf = pygame.sprite.Sprite()
    surf.image = load_image("fone.png")
    surf.rect = surf.image.get_rect()
    menu = Menu(surf, [[load_image("pause.png", colorkey="white"), 150, 50, unpause],
                       [load_image("stop.png", colorkey="white"), 150, 210, stop_game]])
    while running_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_pause = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos)
        menu.render(sc)
        pygame.display.flip()


def unpause():
    global running_pause
    running_pause = False
    Music.gamemusic.unpause()


def stop_game():
    global plaer, running_pause
    plaer.killed = True
    unpause()


def start_play():
    Music.meinmusic.stop()
    Music.gamemusic.play(-1)
    global level, plaer, choisen_character, LEVEL_COUNTER
    plaer = Plaer(*CHARACTERS[choisen_character])
    change_level()
    running = True
    level.start()
    print(running)
    LEVEL_COUNTER = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or plaer.killed:
                running = False
                Music.gamemusic.stop()
                Music.meinmusic.play()
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                else:
                    plaer.move(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    plaer.summon_objectile(event.pos, level.camera.apply(plaer))
                    Music.shoot.play()
            if event.type == pygame.MOUSEMOTION:
                plaer.change_direction(event.pos, level.camera.apply(plaer).x)

        if pygame.sprite.spritecollide(plaer, level.door_group, False):
            change_level()
        sc.fill("black")
        level.update()
        level.render(sc)
        pygame.display.flip()
        clock.tick(DBI)
    dead_screen()


def stop_dead_screen():
    global dead_screen_run
    dead_screen_run = False


def dead_screen():
    global dead_screen_run, plaer, COINS
    surf = pygame.sprite.Sprite()
    surf.image = load_image("fone.png")

    surf.rect = surf.image.get_rect()
    menu = Menu(surf, [[load_image("next.png", colorkey="white"), 200, 450, stop_dead_screen]])
    dead_screen_run = True
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    text = [f"Мобов Убито: {plaer.killed_counter}",
            f"Урона Получено: {plaer.damage_counter}",
            f"Этажей пройдено: {LEVEL_COUNTER}",
            f"Золота Получено: {plaer.killed_counter - plaer.damage_counter // LEVEL_COUNTER}"]
    COINS += plaer.killed_counter - plaer.damage_counter // LEVEL_COUNTER
    while dead_screen_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead_screen_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos)
        if counter1 <= len(text[0]) * 10:
            counter1 += 1
        else:
            if counter2 <= len(text[1]) * 10:
                counter2 += 1
            else:
                if counter3 <= len(text[2]) * 10:
                    counter3 += 1
                else:
                    if counter4 <= len(text[3]) * 10:
                        counter4 += 1
        menu.render(sc)
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(text[0][:counter1 // 10], True,
                          (180, 0, 0))
        text2 = f1.render(text[1][:counter2 // 10], True,
                          (180, 0, 0))
        text3 = f1.render(text[2][:counter3 // 10], True,
                          (180, 0, 0))
        text4 = f1.render(text[3][:counter4 // 10], True,
                          (180, 0, 0))
        sc.blit(text1, (90, 50))
        sc.blit(text2, (90, 150))
        sc.blit(text3, (90, 250))
        sc.blit(text4, (90, 350))
        pygame.display.flip()


def stop_aboute_razrabotchikav():
    global aboute_razrabotchikav_run
    aboute_razrabotchikav_run = False


def aboute_razrabotchikav():
    global aboute_razrabotchikav_run, plaer
    surf = pygame.sprite.Sprite()
    surf.image = load_image("fone.png")
    surf.rect = surf.image.get_rect()
    menu = Menu(surf, [[load_image("next.png", colorkey="white"), 210, 450, stop_aboute_razrabotchikav]])
    aboute_razrabotchikav_run = True
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    text = [f"Над игрой работали: ",
            f"Ну тут напишите свои имена",
            f"И тут",
            f"Александ Кудря - Разработка движка"]
    while aboute_razrabotchikav_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aboute_razrabotchikav_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos)
        if counter1 <= len(text[0]) * 10:
            counter1 += 1
        else:
            if counter2 <= len(text[1]) * 10:
                counter2 += 1
            else:
                if counter3 <= len(text[2]) * 10:
                    counter3 += 1
                else:
                    if counter4 <= len(text[3]) * 10:
                        counter4 += 1
        menu.render(sc)
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(text[0][:counter1 // 10], True,
                          (180, 180, 0))
        text2 = f1.render(text[1][:counter2 // 10], True,
                          (180, 180, 0))
        text3 = f1.render(text[2][:counter3 // 10], True,
                          (180, 180, 0))
        text4 = f1.render(text[3][:counter4 // 10], True,
                          (180, 180, 0))
        sc.blit(text1, (90, 50))
        sc.blit(text2, (90, 150))
        sc.blit(text3, (90, 250))
        sc.blit(text4, (90, 350))
        pygame.display.flip()


ARTEFACTS = [[load_image("Artefact\gold_heard.png", colorkey="black"), {"health_max": "1"}],
             [load_image("Artefact\\banana_sword.png", colorkey="black"), {"damage": "self.damage"}],
             [load_image("Artefact\\ne_poza_a_sahar.png", colorkey="black"), {"speed_x": "3"}],
             [load_image("Artefact\\maslo.png", colorkey="black"), {"obj_spd": "4", "speed_x": "-1"}],
             [load_image("Artefact\\headset.png", colorkey="black"), {"obj_live": "3"}],
             [load_image("Artefact\\udlenitel_ruki.png", colorkey="black"), {"obj_heigth": "30", "damage": "-1"}],
             [load_image("Artefact\\invizibility_powder.png", colorkey="black"),
                                                        {"invisibility_counter_max": "self.invisibility_counter_max"}],
             [load_image("Artefact\\coin.png", colorkey="black"), {"coins": "1000"}]]

ALL_CHARACTERS = [[(10, 10), Sword, {"static": load_image("characters\\sworder_right.png", colorkey="white"),
                                     "run": [load_image(f"characters\\run_sworder\\{i}", colorkey="white") for i
                                             in os.listdir("data\\characters\\run_sworder")],
                                     "attac": [load_image(f"characters\\sworder_attac\\{i}", colorkey="white") for i
                                             in os.listdir("data\\characters\\sworder_attac")]}],
                  [(10, 10), Bow, {"static": load_image("characters\\archer.png", colorkey="white"),
                                     "run": [load_image(f"characters\\run_archer\\{i}", colorkey="white") for i
                                             in os.listdir("data\\characters\\run_archer")],
                                     "attac": [load_image(f"characters\\archer_attac\\{i}", colorkey="white") for i
                                             in os.listdir("data\\characters\\archer_attac")]}],
                  [(10, 10), Gun, {"static": load_image("characters\\guner.png", colorkey="white"),
                                   "run": [load_image(f"characters\\run_guner\\{i}", colorkey="white") for i
                                           in os.listdir("data\\characters\\run_guner")],
                                   "attac": [load_image(f"characters\\guner_attac\\{i}", colorkey="white") for i
                                             in os.listdir("data\\characters\\guner_attac")]}]]

ENEMY_ANIMATIONS = {"RUN": "Enemies\\run",
                    "ATTACK": "Enemies\\attack"}
LEVEL_COUNTER = 0
COINS = 0
choisen_character = 0
with open('data\\configs\\resurses.json') as cat_file:
    data = json.load(cat_file)
COINS = data["coins"]
CHARACTERS = [ALL_CHARACTERS[i] for i in data["characters"]]

SHOWER_SIZE = 36
COINS_SHOWER_COLOR = (255, 200, 0)
HEALTH_SHOWER_SIZE = 20

START_HEALTH = 3
START_HEALTH_MAX = 3
START_INVISIBILITY_MAX = 100

ONE_HEARD_EQUAL = 1

GRAVITY = 0.5
JUMP_POWER = 20

COINS_4_ENEMY = 10

BOW_GRAVITY = 0.1

STEP = 60
CHEST_ARTEFACT_DELAY = 2

COINS_SHOWER_POS = (10, 10)
HEALTH_CHOWER_POS = (10, 50)

DBI = 100

level_stack = []
generate_stack()

clock = pygame.time.Clock()
running_pause = False
dead_screen_run = False
aboute_razrabotchikav_run = False
print(pygame.font.get_default_font())
menu()
with open('data\\configs\\resurses.json', mode="w") as cat_file:
    data["coins"] = COINS
    json.dump(data, cat_file)
