import numpy
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror

BLACK = (0, 0, 0) 
GREY = (127, 127, 127) 
WHITE = (255, 255, 255) 
              
class UiText():                                                                                                              

    size_x = 1
    size_y = 1
    x = 0
    y = 0
    vx = 0
    vy = 0
    ax = 0
    ay = 0
    value = 0
    value_min = 0
    value_max = 90

              
    def __init__(self, init_x, init_y, value, value_min, value_max):
        self.value = value
        self.value_max = value_max
        self.value_min = value_min
        pygame.font.init()
        #self.FONT = pygame.font.Font('freesansbold.ttf', 24) 
        self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 24) 
        self.surfText = self.FONT.render(str(self.value), True, BLACK, WHITE)
        self.rect = self.surfText.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.size_x = self.rect.size[0]
        self.size_y = self.rect.size[1]
        self.x = init_x
        self.y = init_y
        self.position = (self.x, self.y)

    def draw(self, surfaceObject):
        self.surfText = self.FONT.render(str(self.value), True, BLACK, WHITE)
        surfaceObject.blit(self.surfText, self.position)
        self.rect = self.surfText.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.size_x = self.rect.size[0]
        self.size_y = self.rect.size[1]

    def set_size_x(self, new_size_x):
        self.size_x = new_size_x
 
    def set_size_y(self, new_size_y):
        self.size_y = new_size_y
 
    def get_size(self):
        return (self.size_x, self.size_y)
 
    def get_size_x(self):
        return self.size_x
 
    def get_size_y(self):
        return self.size_y
 
    def set_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
 
    def set_x(self, new_x):
        self.x = new_x
 
    def set_y(self, new_y):
        self.y = new_y
 
    def get_pos(self):
        return (self.x, self.y)
 
    def get_x(self):
        return self.x
 
    def get_y(self):
        return self.y
 
    def set_v(self, new_vx, new_vy):
        self.vx = new_vx
        self.vy = new_vy
        
    def set_v_vector(self, vector_size, corrected_angle):
        self.vx = vector_size * numpy.sin(numpy.radians(corrected_angle))
        self.vy = - (vector_size * numpy.cos(numpy.radians(corrected_angle)))
        
    def get_vx(self):
        return self.vx
 
    def get_vy(self):
        return self.vy
 
    def set_a(self, new_ax, new_ay):
        self.ax = new_ax
        self.ay = new_ay

    def set_value(self, new_value):
        try:
            if new_value < self.value_min:
                self.value = self.value_min
            elif new_value > self.value_max:
                self.value = self.value_max
            else:
                self.value = new_value
        except TypeError:
            self.value = new_value


    def increase_value(self):
        new_value = self.value + 1
        if new_value < self.value_min:
            self.value = self.value_min
        elif new_value > self.value_max:
            self.value = self.value_max
        else:
            self.value = new_value

    def decrease_value(self):
        new_value = self.value - 1
        if new_value < self.value_min:
            self.value = self.value_min
        elif new_value > self.value_max:
            self.value = self.value_max
        else:
            self.value = new_value

    def get_value(self):
        return self.value
 
    def update(self):
        # so far we only move
        self.rect = self._move()

    def _move(self):
        self.vx += self.ax
        self.vy += self.ay
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)
        
        return [self.x, self.y]

