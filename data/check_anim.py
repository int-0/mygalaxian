#!/usr/bin/env python

import os.path
import sys
import pygame
import random

GAME_FPS = 30

def load_image(filename):
    img = pygame.image.load(filename)
    return img.convert_alpha()

def load_images(filenames):
    imgs = []
    frameno = 0
    for filename in filenames:
        imgs.append(load_image(filename))
    return imgs

class Animation:
    def __init__(self, destination, frames):
        self.__layout = destination
        self.__frames = load_images(frames)
        self.pos = (300, 300)
        self.speed = (0, 0)
        self.frame = 0

        self.updater = self.next_frame

    def next_frame(self):
        self.frame = (self.frame + 1) % len(self.__frames)

    def prev_frame(self):
        self.frame = self.frame - 1
        if self.frame < 0:
            self.frame = len(self.__frames) - 1
        
    def update(self, pause):
        self.__layout.blit(self.__frames[self.frame], self.pos)
        if not pause:
            self.updater()
        self.pos = (self.pos[0] + self.speed[0],
                    self.pos[1] + self.speed[1])

class Tester:
    def __init__(self, screen, filenames):

        self.__clock = pygame.time.Clock()

        self.__scr = screen

        self.__playground = load_image('playground.png')

        self.animation = Animation(self.__scr, filenames)
        self.__scr.blit(load_image('background.png'), (0, 0))

        self.__pause = False

    def run(self):
        quit = False
        while not quit:
            self.__clock.tick(GAME_FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit = True
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_ESCAPE):
                    quit = True

                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_LEFT):
                    self.animation.speed = (self.animation.speed[0] - 2,
                                            self.animation.speed[1])
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_LEFT) and
                      (self.animation.speed[0] == -2)):
                    self.animation.speed = (0, self.animation.speed[1])
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_RIGHT):
                    self.animation.speed = (self.animation.speed[0] + 2,
                                            self.animation.speed[1])
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_RIGHT) and
                      (self.animation.speed[0] == 2)):
                    self.animation.speed = (0, self.animation.speed[1])
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_UP):
                    self.animation.speed = (self.animation.speed[0],
                                            self.animation.speed[1] - 2)
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_UP) and
                      (self.animation.speed[1] == -2)):
                    self.animation.speed = (self.animation.speed[0], 0)
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_DOWN):
                    self.animation.speed = (self.animation.speed[0],
                                            self.animation.speed[1] + 2)
                elif ((event.type == pygame.KEYUP) and
                      (event.key == pygame.K_DOWN) and
                      (self.animation.speed[1] == 2)):
                    self.animation.speed = (self.animation.speed[0], 0)

                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_SPACE):
                    self.__pause = not self.__pause
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_PAGEUP):
                    self.__pause = True
                    self.animation.updater = self.animation.prev_frame
                    self.animation.updater()
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_PAGEDOWN):
                    self.__pause = True
                    self.animation.updater = self.animation.next_frame
                    self.animation.updater()

            # Draw everything
            self.__scr.blit(self.__playground, (50, 138))
            self.animation.update(self.__pause)
            pygame.display.flip()

        return self.animation.frame
if __name__ == '__main__':
    pygame.init()
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] frame1 ... framen",
                          version="%prog 1.0")
    parser.add_option("-w", "--window", action = "store_true",
                      dest = "window", default = False,
                      help = "use window instead of fullscreen.")
    (options, args) = parser.parse_args()
    if options.window:
        screen = pygame.display.set_mode((1024, 768))
    else:
        screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
    game = Tester(screen, args)
    print 'Last showed frame: %s' % game.run()
