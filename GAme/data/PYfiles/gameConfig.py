import pygame


# player
playerIMG = ""
playerHP = 10
playerSpeed = 10
playerHeight = 40
playerWeight = 10

# physics const
G = 9.81 # ускорение свободного падения


# sprite groups
AllSprites = pygame.sprite.Group()
Enemies = pygame.sprite.Group()
