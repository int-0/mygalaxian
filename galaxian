#!/usr/bin/env python

import os
import os.path
import sys
sys.path.append(os.getcwd())
import pygame
import random

import game.shots
import game.common
import game.player
from game.common import ImageRegistry

GAME_FPS = 30

MAX_STARS = 50

class Space:
    def __init__(self, destination):
        self.__layout = destination

        self.__maxx = self.__layout.get_rect().width
        self.__maxy = self.__layout.get_rect().height

        self.bg = ImageRegistry().get_image('data/playground.png')

        self.stars_spr = []
        self.stars_spr.append((ImageRegistry().get_image('data/star1.png'),
                               6, 8))
        self.stars_spr.append((ImageRegistry().get_image('data/star2.png'),
                               3, 5))
        self.stars_spr.append((ImageRegistry().get_image('data/star3.png'),
                               1, 2))

        self.stars = []
        for i in range(MAX_STARS):
            star = random.choice(self.stars_spr)
            self.stars.append((random.randint(0, self.__maxx),
                               random.randint(0, self.__maxy),
                               random.randint(star[1], star[2]),
                               star[0]))
            
    def update(self):
        self.__layout.blit(self.bg, (0, 0))

        for i in range(MAX_STARS):
            if random.randint(0, 50) != 5 or self.stars[i][2] > 4:
                self.__layout.blit(self.stars[i][3],
                                   (self.stars[i][0], self.stars[i][1]))
            self.stars[i] = (self.stars[i][0],
                            self.stars[i][1] + self.stars[i][2],
                            self.stars[i][2],
                            self.stars[i][3])
            if self.stars[i][1] > (self.__maxy + 10):
                star = random.choice(self.stars_spr)
                self.stars[i] = (random.randint(0, self.__maxx), -5,
                                 random.randint(star[1], star[2]),
                                 star[0])

class AsteroidField:
    def __init__(self, destination, max_asteroids = 10):
        self.__layout = destination
        self.__max_asteroids = max_asteroids

        self.asteroid = ImageRegistry().get_images('data/asteroid_1_')
        self.__nasteroids = len(self.asteroid)
        self.__maxx = (self.__layout.get_rect().width - 
                       self.asteroid[0].get_rect().width)
        self.__maxy = self.__layout.get_rect().height

        self.__asteroids = []

    def __rotate(self, surface, angle):
        original_rect = surface.get_rect()
        rotated_image = pygame.transform.rotate(surface, angle)
        rotated_rect = rotated_image.get_rect()
        clipped_rect = pygame.Rect(
            (rotated_rect.width - original_rect.width) / 2,
            (rotated_rect.height - original_rect.height) / 2,
            original_rect.width, original_rect.height)
        return rotated_image.subsurface(clipped_rect)

    def create_asteroid(self, x = None, vy = None):
        if len(self.__asteroids) >= self.__max_asteroids:
            return
        if x is None:
            x = random.randint(0, self.__maxx)
        if vy is None:
            vy = random.randint(1, 3)
        self.__asteroids.append((random.randint(0, self.__nasteroids - 1),
                                 x, -100, vy))

    def update(self, shots = None):
        destroy = []
        for a in range(len(self.__asteroids)):
            ast = self.__asteroids[a]
            self.__layout.blit(self.asteroid[ast[0]], (ast[1], ast[2]))
            self.__asteroids[a] = ((ast[0] + 1) % self.__nasteroids,
                                   ast[1], ast[2] + ast[3], ast[3])
            if ast[2] > self.__maxy + 10:
                destroy.append(a)

            if not (shots is None):
                ar = pygame.Rect(ast[1], ast[2],
                                 self.asteroid[ast[0]].get_rect().width,
                                 self.asteroid[ast[0]].get_rect().height)
                collision = ar.collidelist(shots.areas())
                if (collision != -1):
                    destroy.append(a)
                    shots.destroy_shot(collision)

        for a in destroy:
            del(self.__asteroids[a])

class PlayerShoot:
    def __init__(self, layout, max_shots = 1):
        self.__layout = layout

        self.shoot_sound = pygame.mixer.Sound('data/shoot.wav')

        self.__max_shots = max_shots
        self.__shots = []

    @property
    def can_shoot(self):
        return len(self.__shots) < self.__max_shots

    def create(self, position):
        if self.can_shoot:
            self.__shots.append(game.shots.PlayerBasic(self.__layout,
                                                       position))
            self.shoot_sound.play()

    def destroy_shot(self, sid):
        if sid < len(self.__shots):
            del(self.__shots[sid])

    def areas(self):
        areas = []
        for bullet in self.__shots:
            areas.append(bullet.area)
        return areas

    def update(self):
        destroy = []
        for sid in range(len(self.__shots)):
            if self.__shots[sid].destroy:
                destroy.append(sid)
            else:
                self.__shots[sid].update()
        for d in destroy:
            del(self.__shots[d])

class Game:
    def __init__(self, screen):

        self.__clock = pygame.time.Clock()

        self.__scr = screen.surface

        self.__playground = ImageRegistry().get_image('data/playground.png')
        self.__scr.blit(ImageRegistry().get_image('data/background.png'),
                        (0, 0))

        self.space = Space(self.__playground)
        self.pshots = PlayerShoot(self.__playground, 2)
        self.player = game.player.Ship(self.__playground,         
                                       self.pshots.create)
        self.asteroids = AsteroidField(self.__playground)

    def run(self):

        while 1:

            self.__clock.tick(GAME_FPS)

            if random.randint(1, 20) == 3:
                self.asteroids.create_asteroid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_ESCAPE):
                    return
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_LEFT):
                    self.player.go_left()
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_RIGHT):
                    self.player.go_right()
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_LEFT)):
                    self.player.no_left()
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_RIGHT)):
                    self.player.no_right()
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_SPACE) and self.pshots.can_shoot:
                    self.player.shoot()

            # Draw everything
            self.space.update()
            self.pshots.update()
            self.asteroids.update(self.pshots)
            self.player.update()

            self.__scr.blit(self.__playground, (150, 0))
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = game.common.Screen(windowed=('-win' in sys.argv),
                                caption='MyGalaxian')

    # Load all images
    ImageRegistry().load_image('data/background.png')
    ImageRegistry().load_image('data/playground.png')
    ImageRegistry().load_image('data/shoot.png')
    ImageRegistry().load_images('data/shoot_')
    ImageRegistry().load_image('data/ship.png')
    ImageRegistry().load_images('data/ship_left_')
    ImageRegistry().load_images('data/ship_right_')
    ImageRegistry().load_images('data/ship_shoot_')
    ImageRegistry().load_images('data/ship_shoot_left_')
    ImageRegistry().load_images('data/ship_shoot_right_')
    ImageRegistry().load_images('data/asteroid_1_')
    ImageRegistry().load_image('data/star1.png')
    ImageRegistry().load_image('data/star2.png')
    ImageRegistry().load_image('data/star3.png')

    main_game = Game(screen)
    main_game.run()
