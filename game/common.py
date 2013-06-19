#!/usr/bin/env python

import pygame
import os.path

DEFAULT_RESOLUTION = (1024, 768)


class ImageNotFound(Exception):
    def __init__(self, image):
        self.__image_name = image

    def __str__(self):
        return 'Image not found in registry: %s' % self.__image_name


def load_image(filename):
    img = pygame.image.load(filename)
    return img.convert_alpha()


def load_images(filename_base):
    imgs = []
    frameno = 0
    while True:
        filename = '%s%02d.png' % (filename_base, frameno)
        if os.path.exists(filename):
            imgs.append(load_image(filename))
        else:
            break
        frameno += 1
    return imgs


class ImageRegistry(object):
    class __impl(object):
        __registry = {}

        def load_image(self, filename):
            self.__registry[filename] = load_image(filename)

        def load_images(self, filename_base):
            frameno = 0
            while True:
                filename = '%s%02d.png' % (filename_base, frameno)
                if os.path.exists(filename):
                    self.load_image(filename)
                else:
                    break
                frameno += 1

        def flush_all(self):
            self.__registry = {}

        @property
        def registered_images(self):
            return self.__registry.keys()

        def image_exists(self, filename):
            return filename in self.registered_images

        def get_image(self, filename):
            if self.image_exists(filename):
                return self.__registry[filename].copy()

        def get_images(self, filename_base):
            images = []
            frameno = 0
            while True:
                filename = '%s%02d.png' % (filename_base, frameno)
                if self.image_exists(filename):
                    images.append(self.get_image(filename))
                else:
                    break
                frameno += 1
            return images

    __instance = None

    def __init__(self):
        if ImageRegistry.__instance is None:
            ImageRegistry.__instance = ImageRegistry.__impl()
        self.__dict__['_ImageRegistry__instance'] = ImageRegistry.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class Screen(object):
    class __impl(object):
        def __init__(self, resolution=DEFAULT_RESOLUTION,
                     windowed=False,
                     caption='Sigame Screen'):
            if not pygame.display.get_init():
                pygame.display.init()
            pygame.display.set_caption(caption)

            self.__res = resolution
            flag = 0 if windowed else (pygame.FULLSCREEN +
                                       pygame.HWSURFACE +
                                       pygame.DOUBLEBUF)
            self.__scr = pygame.display.set_mode(self.__res,
                                                 flag)
            self.__gnd = pygame.Surface(resolution)

            self.__dirty = pygame.sprite.RenderUpdates()
            self.__raw_dirty = []

        def __load_image(self, filename):
            image = pygame.image.load(filename)
            return image.convert_alpha()

        def set_background(self, filename):
            self.__gnd = self.__load_image(filename)
            self.__scr.blit(self.__gnd, (0, 0))
            pygame.display.flip()

        # Add one sprite to screen
        def add(self, sprite):
            self.__dirty.add(sprite)

        # Update and draw render group
        def update(self):
            self.__dirty.update()
            dirty = self.__dirty.draw(self.__scr)
            pygame.display.update(dirty + self.__raw_dirty)
            self.__dirty.clear(self.__scr, self.__gnd)
            self.__raw_dirty = []

        def blit(self, surface, position):
            self.__raw_dirty.append(self.__scr.blit(surface, position))

        @property
        def surface(self):
            return self.__scr

    __instance = None

    def __init__(self, resolution=DEFAULT_RESOLUTION,
                 windowed=False,
                 caption='Sigame Screen'):
        if Screen.__instance is None:
            Screen.__instance = Screen.__impl(resolution,
                                              windowed,
                                              caption)
        self.__dict__['_Screen__instance'] = Screen.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
