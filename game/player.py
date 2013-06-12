#!/usr/bin/env python

import common
from common import ImageRegistry

_MAX_SPEED = 6


class Ship(object):
    def __init__(self, destination):

        self.__layout = destination

        self.static_ship = [ImageRegistry().get_image('data/ship.png')]
        self.left_ship = ImageRegistry().get_images('data/ship_left_')
        self.right_ship = ImageRegistry().get_images('data/ship_right_')
        self.shot_ship = ImageRegistry().get_images('data/ship_shoot_')

        self.__current_frame = 0

        self.__maxx = self.__layout.get_rect().width
        self.__maxy = self.__layout.get_rect().height

        self.x = self.__maxx - (self.static_ship[0].get_rect().width / 2) / 2
        self.y = self.__maxy - self.static_ship[0].get_rect().height - 5

        self.__minpx = 0
        self.__maxpx = (self.__maxx - self.static_ship[0].get_rect().width)

        self.__req_spd = 0
        self.vx = 0
        self.max_v = 0

        self.__fr = 0
        self.__fl = 0

    def go_left(self):
        self.__req_spd = -_MAX_SPEED

    def go_right(self):
        self.__req_spd = _MAX_SPEED

    def no_left(self):
        if self.__req_spd < 0:
            self.stop()

    def no_right(self):
        if self.__req_spd > 0:
            self.stop()

    def stop(self):
        self.__req_spd = 0

    def shot(self):
        pass

    @property
    def __moving_left(self):
        if self.__fr > 0:
            self.__fr -= 1
            return self.right_ship[self.__fr]
        if self.__fl < len(self.left_ship) - 1:
            self.__fl += 1
        return self.left_ship[self.__fl]

    @property
    def __moving_right(self):
        if self.__fl > 0:
            self.__fl -= 1
            return self.left_ship[self.__fl]
        if self.__fr < len(self.right_ship) - 1:
            self.__fr += 1
        return self.right_ship[self.__fr]

    @property
    def __no_moving(self):
        if self.__fl > 0:
            self.__fl -= 1
            return self.left_ship[self.__fl]
        if self.__fr > 0:
            self.__fr -= 1
            return self.right_ship[self.__fr]
        return self.static_ship[0]

    def update(self):
        if self.vx != self.__req_spd:
            if self.vx < self.__req_spd:
                self.vx += 1
            else:
                self.vx -= 1

        self.x += self.vx

        if self.x < self.__minpx:
            self.x = self.__minpx
        if self.x > self.__maxpx:
            self.x = self.__maxpx

        if self.__req_spd == 0:
            self.__layout.blit(self.__no_moving, (self.x, self.y))
        elif self.__req_spd > 0:
            self.__layout.blit(self.__moving_right, (self.x, self.y))
        else:
            self.__layout.blit(self.__moving_left, (self.x, self.y))

    def laser_pos(self):
        return (self.x + 20, self.y + 5)
