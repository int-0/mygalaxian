#!/usr/bin/env python

import pygame
import os.path

DEFAULT_RESOLUTION = (1024, 768)


class ImageNotFound(Exception):
    def __init__(self, image):
        self.__image_name = image

    def __str__(self):
        return 'Image not found in registry: %s' % self.__image_name


class ActionNotFound(Exception):
    def __init__(self, action):
        self.__action_name = action

    def __str__(self):
        return "Action not found in actor's registry: %s" % self.__action_name


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


class Animation(object):
    def __init__(self, frame_sheet, callback=None):
        self.__frame = frame_sheet

        self.__max_frame = len(frame_sheet)
        self.__current = 0

        self.__callback = callback
        self.__fire_callback = True

        self.frame = self.__frame_no_loop

    def reset(self):
        self.__current = 0
        self.__fire_callback = True

    def set_callback(self, callback):
        self.__callback = callback

    @property
    def callback(self):
        return self.__callback

    @property
    def image(self):
        return self.__frame[self.__current]

    @property
    def rect(self):
        return self.image.get_rect()

    def set_loop(self, loop_mode):
        self.frame = self.__loop if loop_mode else self.__no_loop

    @property
    def __no_loop(self):
        image = self.image
        if (self.__current + 1) == self.__max_frame:
            if ((self.__callback is not None) and self.__fire_callback):
                self.__callback()
                self.__fire_callback = False
        else:
            self.__current += 1
        return image

    @property
    def __loop(self):
        image = self.image
        if (self.__current + 1) == self.__max_frame:
            if ((self.__callback is not None) and self.__fire_callback):
                self.__callback()
                self.__fire_callback = False
            self.reset()
        else:
            self.__current += 1
        return image


def new_animation(image_prefix, callback=None):
    return Animation(ImageRegistry().get_images(image_prefix), callback)


def new_loop(image_prefix, callback=None):
    anim = Animation(ImageRegistry().get_images(image_prefix), callback)
    anim.set_loop(True)
    return anim


class Actor(pygame.sprite.DirtySprite):
    def __init__(self, action_registry, steering, initial_position):
        pygame.sprite.DirtySprite.__init__(self)
        if 'initial' not in action_registry.keys():
            raise ActionNotFound('initial')

        # Frames
        self.__animation = action_registry
        self.__current = 'initial'

        # Position/movement
        self.rect = self.__animation[self.__current].rect
        self.rect.center = initial_position
        self.__steer = steering

    def add_action(self, action_name, action):
        self.__animation[action_name] = action

    def set_callback(self, action_name, callback):
        if action_name not in self.__animation.keys():
            raise ActionNotFound(action_name)
        self.__action[action_name].set_callback(callback)

    def get_callback(self, action_name):
        if action_name not in self.__animation.keys():
            raise ActionNotFound(action_name)
        return self.__action[action_name].callback

    @property
    def action(self):
        return self.__current

    @action.setter
    def action(self, new_action):
        # Check if new_action exists!
        self.__current = new_action
        self.__animation[self.__current].reset()

    @property
    def callback(self):
        return self.get_callback(self.__current)

    @callback.setter
    def callback(self, new_callback):
        self.set_callback(self.__current, callback)

    def update(self):
        self.image = self.__animation[self.__current].frame

    def process(self, event):
        self.__steer.process(event)
