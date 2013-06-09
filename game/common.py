#!/usr/bin/env python

import pygame
import os.path


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
    """ A python singleton """

    class __impl(object):
        """ Implementation of the singleton interface """
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

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if ImageRegistry.__instance is None:
            # Create and remember instance
            ImageRegistry.__instance = ImageRegistry.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_ImageRegistry__instance'] = ImageRegistry.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
