#!/usr/bin/env python3
"""
Simple RoboCop Shooter Game
A retro-style side-scrolling shooter inspired by RoboCop
"""

import pygame
import sys

#initialize game
pygame.init()

#define display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Roboocop")
background = pygame.image.load("assets/background.png")

#fps
clock = pygame.time.Clock()
FPS = 60

#player
orig_img = pygame.image.load("assets/robotside.png")
orig_size = orig_img.get_size()
#the size is sent in an array
new_size = (orig_size[0] // 2, orig_size[1] // 2)
player_image = pygame.transform.scale(orig_img, new_size)

player_rect = player_image.get_rect()
# #center player in the middle of the screen
# player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
PLAYER_X = 200
player_rect.x = PLAYER_X
player_rect.y = SCREEN_HEIGHT // 2 - 50


#player speed
player_speed = 5

#bullets
bullets = []
bullet_speed = 10
#background position and speed to make bg move like scroll
bg_x = 0
bg_speed = 5


#game logic
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         # player_rect.x += player_speed
        #         bg_x -= bg_speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        bg_x -= bg_speed
                
    if player_rect.x > SCREEN_WIDTH - player_rect.width:
        player_rect.x = SCREEN_WIDTH - player_rect.width

    player_rect.x = PLAYER_X                
    #give it black background
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + background.get_width(), 0))

    if bg_x <= -background.get_width():
        bg_x = 0
    #draw the character
    screen.blit(player_image, player_rect)

    #display everything
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()