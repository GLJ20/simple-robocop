#!/usr/bin/env python3
"""
Simple RoboCop Shooter Game
A retro-style side-scrolling shooter inspired by RoboCop
"""

import pygame
import sys
import random

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

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

#player
orig_img = pygame.image.load("assets/robotside.png")
orig_size = orig_img.get_size()
#the size is sent in an array
new_size = (orig_size[0] // 2, orig_size[1] // 2)
player_image = pygame.transform.scale(orig_img, new_size)

player_rect = player_image.get_rect()
#have the player be in a specific position
PLAYER_X = 200
player_rect.x = PLAYER_X
player_rect.y = SCREEN_HEIGHT // 2 - 50


#player speed
player_speed = 5

#bullets
bullets = []
bullet_speed = 10

#enemies
enemies = []
enemy_speed = 4
enemy_spawn_timer = 0
enemy_spawn_delay = 120 # spawn enemy every 2 secs at 60 fps

#gmae state
paused = False
score = 0

#background position and speed to make bg move like scroll
bg_x = 0
bg_speed = 5


#game logic
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and not paused:
                new_bullet = {
                    "x": player_rect.x + player_rect.width,
                    "y": player_rect.y + player_rect.height // 2 - 40,
                    #we are creating a rectangle bullet, using pygame>rect which is a rectangle object and the arguments it needs is x,y,width, height
                    "rect": pygame.Rect(player_rect.x + player_rect.width, player_rect.y + player_rect.height //2 - 40, 25, 5)
                }
                bullets.append(new_bullet)
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_ESCAPE and paused:
                running = False
    if not paused:
        #for continous movement of player when user presses the right key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            bg_x -= bg_speed

        #for player boundries to ensure they dont leave screen            
        if player_rect.x > SCREEN_WIDTH - player_rect.width:
            player_rect.x = SCREEN_WIDTH - player_rect.width

        #to keep player at a fixed position to create the scroll effect of the bg moving and hte user moving like retro games
        player_rect.x = PLAYER_X                

        #Enemy spawn
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_delay:
            enemy_y = random.randint(100, SCREEN_HEIGHT - 150)
            new_enemy = {
                "x": SCREEN_WIDTH,
                "y": enemy_y,
                "rect": pygame.Rect(SCREEN_WIDTH, enemy_y, 60, 60)
            }
            enemies.append(new_enemy)
            enemy_spawn_timer = 0
    for bullet in bullets[:]:
        bullet["x"] += bullet_speed
        bullet["rect"].x = bullet["x"]
        if bullet["x"] > SCREEN_WIDTH:
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy["x"] -= enemy_speed
        enemy["rect"].x = enemy["x"]
        if enemy["x"] < -60:
            enemies.remove(enemy)
    
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy["rect"]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + background.get_width(), 0))

    if bg_x <= -background.get_width():
        bg_x = 0
    #draw the character
    screen.blit(player_image, player_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, (255,0,0), bullet["rect"])
    
    for enemy in enemies:
        pygame.draw.rect(screen, (0, 255,0), enemy["rect"])
    
    score_text = font.render(f'Score: {score}', True, (255,255,255))
    screen.blit(score_text, (10,10))

    if paused:
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pause_surface.set_alpha(128)
        pause_surface.fill((0,0,0))
        screen.blit(pause_surface, (0,0))

        pause_text = big_font.render("PAUSED", True, (255,255,255))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(pause_text, pause_rect)

        resume_text = font.render("Press P to RESUME", True, (255,255,255))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(resume_text, resume_rect)

        exit_text = font.render("Press ESC ro EXIT", True, (255,255,255))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        screen.blit(exit_text, exit_rect)
    #display everything
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()