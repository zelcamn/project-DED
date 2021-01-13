import os
from random import randint

import pygame


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


def create_platform(width, heigth, pos):
    Platform(width - 2, 1, (pos[0] + 1, pos[1]), vertical_platforms_up)
    Platform(width - 2, 1,
             (pos[0] + 1, pos[1] + heigth - 1),
             vertical_platforms_down)
    Platform(1, heigth - 2,
             (pos[0], pos[1] + 1),
             horisontal_platform_left)
    Platform(1, heigth - 2,
             (pos[0] + width - 1, pos[1] + 1),
             horisontal_platform_rigth)
    Platform(width, heigth, pos, mask_platforms)


def render(arr_groups, screen):
    if not(isinstance(arr_groups, list)):
        raise TypeError("arr_groups must be list")
    for group in arr_groups:
        if isinstance(group, pygame.sprite.Group):
            group.draw(screen)
        else:
            print("Erore of layer number", arr_groups.index(group))


def update(arr_groups):
    if not(isinstance(arr_groups, list)):
        raise TypeError("arr_groups must be list")
    for group in arr_groups:
        if isinstance(group, pygame.sprite.Group):
            group.update()
        else:
            print("Erore of layer number", arr_groups.index(group))


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, heigth, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((width, heigth))
        self.rect = self.image.get_rect()
        self.image.fill("gray")
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Plaer(pygame.sprite.Sprite):
    image_rigth = load_image("hero_right.jpg", colorkey="black")
    image_left = load_image("hero_left.jpg", colorkey="black")

    def __init__(self, pos):
        super().__init__(plaer_group)
        self.image = Plaer.image_rigth
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.a_x = 0
        self.a_y = 0
        self.onLader = False
        self.step = 1
        self.speed_x = 5
        self.killed = False

        self.obj_spd = 5

    def update(self, *args):
        for i in range(abs(self.a_x)):
            if self.a_x > 0:
                if not(pygame.sprite.spritecollide(self, horisontal_platform_left, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
            if self.a_x < 0:
                if not(pygame.sprite.spritecollide(self, horisontal_platform_rigth, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
        if self.a_y > 0:
            self.step = 1
        elif self.a_y < 0:
            self.step = -1
        for i in range(abs(self.a_y)):
            self.rect.y += 1 * self.step
            if pygame.sprite.spritecollide(self, vertical_platforms_up, False):
                break
            if pygame.sprite.spritecollide(self, vertical_platforms_down, False):
                self.a_y = 1
        if not(pygame.sprite.spritecollide(self, vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        if pygame.sprite.spritecollide(self, enemy_group, False):
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
                if pygame.sprite.spritecollide(self, vertical_platforms_up, False):
                    self.a_y += -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.a_x = 0
            if event.key == pygame.K_d:
                self.a_x = 0

    def summon_objectile(self):
        if self.obj_spd > 0:
            Objectile((self.rect.x + 40, self.rect.y), self.obj_spd, 10)
        if self.obj_spd < 0:
            Objectile((self.rect.x, self.rect.y), self.obj_spd, 10)


class Enemy(pygame.sprite.Sprite):
    image_right = load_image("zlov_right.png", colorkey="black")
    image_left = load_image("zlov_left.png", colorkey="black")

    def __init__(self, pos):
        super().__init__(enemy_group)
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
                if not (pygame.sprite.spritecollide(self, horisontal_platform_left, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
            if self.a_x < 0:
                if not (pygame.sprite.spritecollide(self, horisontal_platform_rigth, False)):
                    self.rect.x += 1 * (self.a_x / abs(self.a_x))
        if self.a_y > 0:
            self.step = 1
        elif self.a_y < 0:
            self.step = -1
        for i in range(abs(self.a_y)):
            self.rect.y += 1 * self.step
            if pygame.sprite.spritecollide(self, vertical_platforms_up, False):
                break
            if pygame.sprite.spritecollide(self, vertical_platforms_down, False):
                self.a_y = 1
        if not(pygame.sprite.spritecollide(self, vertical_platforms_up, False)):
            self.a_y += 1
        else:
            self.a_y = 0

        if pygame.sprite.spritecollide(self, objectile_group, True):
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
    def __init__(self, pos, a_x, time_of_live):
        super().__init__(objectile_group)
        self.image = pygame.Surface((10, 40))
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
        if pygame.sprite.spritecollide(self, horisontal_platform_rigth, False) or \
                pygame.sprite.spritecollide(self, horisontal_platform_left, False):
            self.kill()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


clock = pygame.time.Clock()

plaer_group = pygame.sprite.Group()
vertical_platforms_up = pygame.sprite.Group()
vertical_platforms_down = pygame.sprite.Group()
horisontal_platform_left = pygame.sprite.Group()
horisontal_platform_rigth = pygame.sprite.Group()
mask_platforms = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
objectile_group = pygame.sprite.Group()
arr_groups = [plaer_group, vertical_platforms_up,
              vertical_platforms_down, horisontal_platform_left,
              horisontal_platform_rigth, enemy_group, objectile_group, mask_platforms]
plaer = Plaer((10, 10))
enemys = [Enemy((500, 10))]
floor1 = Platform(width, 1, (0, height - 1), vertical_platforms_up)
floor2 = Platform(width, 1, (0, 0), vertical_platforms_down)
floor3 = Platform(1, height, (width - 1, 0), horisontal_platform_left)
floor4 = Platform(1, height, (0, 0), horisontal_platform_rigth)
for i in range(5):
    create_platform(randint(0, 300), randint(0, 300), (randint(0, 600), randint(0, 600)))
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
        if all([enemy.killed for enemy in enemys]):
            enemy_counter += 1
            enemys = [Enemy((randint(10, 580), 10)) for i in range(enemy_counter)]
    sc.fill("black")
    update(arr_groups)
    render(arr_groups, sc)
    pygame.display.flip()
    clock.tick(100)