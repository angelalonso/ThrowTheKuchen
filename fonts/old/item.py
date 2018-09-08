# TODO: get size from image
# make class decide whether to accept image or x, y sizes
import numpy
import pygame

class Item(pygame.sprite.Sprite):

    size_x = 1
    size_y = 1
    x = 0
    y = 0
    vx = 0
    vy = 0
    ax = 0
    ay = 0

    def __init__(self, size_x, size_y, init_x, init_y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.size_x = size_x
        self.size_y = size_y
        self.x = init_x
        self.y = init_y

    def set_size_x(self, new_size_x):
        self.size_x = new_size_x

    def set_size_y(self, new_size_y):
        self.size_y = new_size_y

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
        
    def update(self):
        #TODO: check all forces and velocities, calculate new position and return it
        #TODO: do aceleration with vectors too
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        
        return [self.x, self.y]


