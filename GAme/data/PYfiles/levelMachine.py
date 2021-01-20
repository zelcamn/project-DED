# class Level:
#     def __init__(self, file, summon_time=500, end_time=500):
#         self.enemys = []
#         self.summon_time = summon_time
#         self.end_time = end_time
#         self.end_time_run = False
#         with open(file, mode="r", encoding="utf-8") as fil:
#             self.arr = fil.readlines()
#             self.width = int(self.arr[0].split()[0])
#             self.heigth = int(self.arr[0].split()[1])
#             self.back_ground = self.arr[0].split()[2]
#
#             self.map = [i.split() for i in self.arr[2::]]
#
#             self.plaer_group = pygame.sprite.Group()
#             self.vertical_platforms_up = pygame.sprite.Group()
#             self.vertical_platforms_down = pygame.sprite.Group()
#             self.horisontal_platform_left = pygame.sprite.Group()
#             self.horisontal_platform_rigth = pygame.sprite.Group()
#             self.mask_platforms = pygame.sprite.Group()
#             self.enemy_group = pygame.sprite.Group()
#             self.objectile_group = pygame.sprite.Group()
#
#             self.arr_groups = [self.plaer_group, self.vertical_platforms_up,
#             self.vertical_platforms_down, self.horisontal_platform_left,
#             self.horisontal_platform_rigth, self.enemy_group, self.objectile_group, self.mask_platforms]
#
#             Platform(width, 1, (0, height - 1), self.vertical_platforms_up)
#             Platform(width, 1, (0, 0), self.vertical_platforms_down)
#             Platform(1, height, (width - 1, 0), self.horisontal_platform_left)
#             Platform(1, height, (0, 0), self.horisontal_platform_rigth)
#             print(*self.map, sep="\n")
#             for i in range(len(self.map)):
#                 for j in range(len(self.map[i])):
#                     if self.map[i][j] == "1":
#                         self.create_platform(width / self.width, height / self.heigth,
#                                              (j * height / self.heigth, i * width / self.width))
#
#     def summon_vragov(self):
#         self.enemys = [Enemy((randint(300, 600), 10)) for i in range(int(self.arr[1].split()[0]))]
#
#     def create_platform(self, width, heigth, pos):
#         Platform(width - 2, 1, (pos[0] + 1, pos[1]), self.vertical_platforms_up)
#         Platform(width - 2, 1,
#                  (pos[0] + 1, pos[1] + heigth - 1),
#                  self.vertical_platforms_down)
#         Platform(1, heigth - 2,
#                  (pos[0], pos[1] + 1),
#                  self.horisontal_platform_left)
#         Platform(1, heigth - 2,
#                  (pos[0] + width - 1, pos[1] + 1),
#                  self.horisontal_platform_rigth)
#         Platform(width, heigth, pos, self.mask_platforms)
#
#     def render(self, screen):
#         if not (isinstance(self.arr_groups, list)):
#             raise TypeError("arr_groups must be list")
#         for group in self.arr_groups:
#             if isinstance(group, pygame.sprite.Group):
#                 group.draw(screen)
#             else:
#                 print("Erore of layer number", self.arr_groups.index(group))
#
#     def update(self):
#         if not (isinstance(self.arr_groups, list)):
#             raise TypeError("arr_groups must be list")
#         for group in self.arr_groups:
#             if isinstance(group, pygame.sprite.Group):
#                 group.update()
#             else:
#                 print("Erore of layer number", self.arr_groups.index(group))
#
#     def end(self):
#         for i in self.enemys:
#             if not(i.killed):
#                 return False
#         return True
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, width, heigth, pos, group):
#         super().__init__(group)
#         self.image = pygame.Surface((width, heigth))
#         self.rect = self.image.get_rect()
#         self.image.fill("gray")
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]