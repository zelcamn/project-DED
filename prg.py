import pygame
import pytmx

pygame.init()

display = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

gameMap = pytmx.load_pygame("map.tmx")

while True:

    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if keys[pygame.K_ESCAPE]:
        quit()

    for layer in gameMap.visible_layers:
        for x, y, gid, in layer:
            tile = gameMap.get_tile_image_by_gid(gid)
            if tile != None:
                display.blit(tile, (x * gameMap.tilewidth, y * gameMap.tileheight))

    pygame.display.update()

   
