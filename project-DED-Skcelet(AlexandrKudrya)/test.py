import math
import os
import random
import sys

import pygame
import pytmx

pygame.init()
pygame.mixer.init()
width, height = 600, 600
sc = pygame.display.set_mode((width, height))

TILE_DICT = {"platform": 3,
             "zlov": 4,
             "spawn": 5,
             "door": 6,
             "heard": 7,
             "chest": 8}


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


class Shower(pygame.sprite.Sprite):
    def __init__(self, pos, group, target):
        super().__init__(group)
        self.f1 = pygame.font.Font(None, 36)
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
        text1 = self.f1.render(str(self.target.coins), True, (255, 200, 0))
        self.image = text1
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Helth_Shower(Shower):
    def __init__(self, pos, group, target):
        super().__init__(pos, group, target)

    def update(self):
        text1 = self.f1.render(str(self.target.health), True, (180, 0, 0))
        self.image = text1
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Plaer(pygame.sprite.Sprite):
    image_rigth = load_image("hero_right.jpg", colorkey="black")
    image_left = load_image("hero_left.jpg", colorkey="black")

    def __init__(self, pos, weapon):
        super().__init__()
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
        self.obj_spd = weapon.obj_spd
        self.obj_live = weapon.obj_live
        self.obj_heigth = weapon.obj_heigth
        self.obj_type = weapon.obj_type
        if weapon.is_aim:
            self.reaim_function = weapon.reaim
        else:
            self.reaim_function = (lambda x, y: x + y)

        self.coins = 0
        self.health = 3
        self.invisibility_counter_max = 100
        self.invisibility_counter = self.invisibility_counter_max

    def reload(self):
        level.plaer_group.add(self)
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.rect.x = 10
            self.rect.y = 10

    def update(self, *args):
        if pygame.sprite.spritecollide(self, level.enemy_group, False):
            if self.invisibility_counter >= self.invisibility_counter_max:
                self.health -= 1
                self.a_y -= 20
                Music.povrejen.play()
                if self.health <= 0:
                    self.killed = True
                    self.kill()
                    Music.gameover.play()
                else:
                    self.invisibility_counter = 0

        if pygame.sprite.spritecollide(self, level.heath_group, True):
            self.health += 1
            Music.healthup.play()

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
            self.a_y += 0.5
        else:
            self.a_y = 0

        if self.invisibility_counter < self.invisibility_counter_max:
            self.invisibility_counter += 1

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
                    self.a_y += -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.a_x = 0
            if event.key == pygame.K_d:
                self.a_x = 0

    def change_direction(self, pos, plaer_x_on_screen):
        x = pos[0]
        if x < plaer_x_on_screen:
            self.image = Plaer.image_left
            self.obj_spd = -5
        else:
            self.image = Plaer.image_rigth
            self.obj_spd = 5
        self.reaim(pos)

    def summon_objectile(self, target_pos, real):
        if self.obj_spd > 0:
            self.obj_type((self.rect.x + 40, self.rect.y + 20 - self.obj_heigth // 2),
                          self.obj_spd,
                          self.obj_live,
                          self.obj_heigth,
                          target_pos, real)
        if self.obj_spd < 0:
            self.obj_type((self.rect.x, self.rect.y + 20 - self.obj_heigth // 2),
                          self.obj_spd,
                          self.obj_live,
                          self.obj_heigth,
                          target_pos, real)

    def reaim(self, target):
        self.reaim_function((self.rect.x, self.rect.y), target)


class Enemy(pygame.sprite.Sprite):
    image_right = load_image("zlov_right.png", colorkey="black")
    image_left = load_image("zlov_left.png", colorkey="black")

    def __init__(self, pos, group):
        super().__init__(group)
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
        if not (pygame.sprite.spritecollide(self, level.vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        if pygame.sprite.spritecollide(self, level.objectile_group, True):
            plaer.coins += 10
            self.killed = True
            self.kill()
            Music.zlovded.play()

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
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real):
        super().__init__(level.objectile_group)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.a_x = a_x
        self.counter = 0
        self.counter_max = time_of_live

    def update(self, *args):
        pass

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Objectile_Sword(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real):
        self.image = pygame.Surface((10, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("white")
        self.heigth = heigth

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real)

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
    is_aim = False


class Objectile_Bow(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real):
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.image.fill("white")

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real)

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
        self.a_y += 0.1
        self.counter += 1
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.kill()


class Bow:
    obj_spd = 5
    obj_live = 10
    obj_heigth = 40
    obj_type = Objectile_Bow
    is_aim = False


class Objectile_Gun(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real):
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.image.fill("white")

        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real)

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
        if pygame.sprite.spritecollide(self, level.mask_platforms, False):
            self.kill()


class Gun:
    obj_spd = 5
    obj_live = 10
    obj_heigth = 10
    obj_type = Objectile_Gun
    is_aim = False


class Objectile_Axe(Objectile):
    def __init__(self, pos, a_x, time_of_live, heigth, target_pos, real):
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.image.fill("white")
        super().__init__(pos, a_x, time_of_live, heigth, target_pos, real)

    def update(self, *args):
        self.rect.x += self.a_x
        self.counter += 1
        if self.counter >= self.counter_max:
            self.kill()


class Axe:
    obj_spd = 1
    obj_live = 2
    obj_heigth = 40
    obj_type = Objectile_Axe
    is_aim = False


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
    def __init__(self, file, wrez, hrez, summon_time=500, end_time=500):
        self.enemys = []
        self.summon_time = summon_time
        self.end_time = end_time
        self.end_time_run = False

        self.map = pytmx.load_pygame(f"{file}")

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

        self.arr_unstatick_groups = [self.plaer_group, self.vertical_platforms_up,
                                     self.vertical_platforms_down, self.horisontal_platform_left,
                                     self.horisontal_platform_rigth, self.enemy_group, self.heath_group,
                                     self.objectile_group, self.mask_platforms, self.door_group]

        self.gui_group = pygame.sprite.Group()
        self.plaer_coins = Coin_Shower((10, 10), self.gui_group, plaer)
        self.plaer_helth = Helth_Shower((10, 50), self.gui_group, plaer)

        self.arr_statick_groups = [self.gui_group]

        self.start_pos = (0, 0)

        print(*self.map, sep="\n")
        for y in range(-1, self.map.height + 1):
            for x in range(-1, self.map.width + 1):
                if 0 <= y < self.map.height and 0 <= x < self.map.width:
                    image = self.map.get_tile_image(x, y, 0)
                    if not (image is None):
                        if self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["zlov"]:
                            self.enemys.append(Enemy((x * self.width_res, y * self.heigth_res), self.enemy_group))
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["spawn"]:
                            self.start_pos = (x * self.width_res, y * self.heigth_res)
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["door"]:
                            self.create_door((x * self.width_res, y * self.heigth_res), image)
                        elif self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] == TILE_DICT["heard"]:
                            Drop((x * self.width_res, y * self.heigth_res), self.heath_group, image)
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


def change_level():
    global level, plaer
    level = Level(f"data\levels\\{random.randint(1, 8)}.tmx", 60, 60)
    plaer.reload()
    level.start()


def menu():
    surf = pygame.sprite.Sprite()
    surf.image = pygame.Surface((width, height))
    surf.image.fill("cyan")
    Music.meinmusic.play()
    surf.rect = surf.image.get_rect()
    Menu(surf, [[load_image("play.png"), 150, 10, start_play]])
    menu = Menu(surf, [[load_image("play.png"), 150, 10, start_play]])
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos)
        menu.render(sc)
        pygame.display.flip()


def pause():
    global plaer, running_pause
    running_pause = True
    Music.gamemusic.pause()

    surf = pygame.sprite.Sprite()
    surf.image = pygame.Surface((width, height))
    surf.image.fill("red")
    surf.rect = surf.image.get_rect()
    menu = Menu(surf, [[load_image("pause.png"), 150, 10, unpause],
                       [load_image("stop.png"), 150, 150, stop_game]])
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
    global level, plaer
    plaer = Plaer((10, 10), Gun)
    change_level()
    running = True
    level.start()
    print(running)

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
        clock.tick(100)


clock = pygame.time.Clock()
running_pause = False
print(pygame.font.get_default_font())
menu()
