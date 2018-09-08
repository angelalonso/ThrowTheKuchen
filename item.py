# Import Modules
import numpy
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror


class Item(pygame.sprite.Sprite):

    # Initialize some variables
    size_x = 1
    size_y = 1
    x = 0
    y = 0
    vx = 0
    vy = 0
    ax = 0
    ay = 0
    image_type = "static"
    frame = 0

    def __init__(self, init_x, init_y, imagefile, transparency=0):
        pygame.sprite.Sprite.__init__(self)
        if transparency == 0:
            self.image, self.rect = self.load_image(imagefile)
        else:
            self.image, self.rect = self.load_image(imagefile, transparency)
        # TODO: add transparency -> self.image, self.rect = self.load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()        
        self.size_x = self.rect.size[0]
        self.size_y = self.rect.size[1]
        self.x = init_x
        self.y = init_y
 
    def load_image(self, imagename, colorkey=None):
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        img_dir = os.path.join(main_dir, 'drawables')
        fullname = os.path.join(img_dir, imagename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def render_image(self):
        self.rendered = pygame.sprite.RenderPlain(self)
        return self.rendered

    def load_image_static(self, imagefile, transparency=0):
        self.image_type = "static"
        if transparency == 0:
            self.image, self.rect = self.load_image(imagefile)
        else:
            self.image, self.rect = self.load_image(imagefile, transparency)
        old_size_x = self.size_x
        old_size_y = self.size_y
        self.size_x = self.rect.size[0]
        self.size_y = self.rect.size[1]
        old_pos = self.get_pos()
        self.set_pos(old_pos[0] - (self.size_x - old_size_x), old_pos[1] - (self.size_y - old_size_y))


    def load_image_play(self, imagefile, new_size_x, transparency=0, speed=10):
        self.play_speed = speed
        self.image_type = "play"
        if transparency == 0:
            self.image, self.rect = self.load_image(imagefile)
        else:
            self.image, self.rect = self.load_image(imagefile, transparency)
        old_size_x = self.size_x
        old_size_y = self.size_y
        self.size_x = new_size_x
        self.size_y = self.rect.size[1]
        old_pos = self.get_pos()
        self.set_pos(old_pos[0] - (self.size_x - old_size_x), old_pos[1] - (self.size_y - old_size_y))

    def load_image_playonce(self, imagefile, new_size_x, transparency=0, speed=10):
        self.play_speed = speed
        self.image_type = "playonce"
        self.frame = 0
        if transparency == 0:
            self.image, self.rect = self.load_image(imagefile)
        else:
            self.image, self.rect = self.load_image(imagefile, transparency)
        old_size_x = self.size_x
        old_size_y = self.size_y
        self.size_x = new_size_x
        self.size_y = self.rect.size[1]
        old_pos = self.get_pos()
        new_pos = old_pos[0] - (self.size_x - old_size_x), old_pos[1] - (self.size_y - old_size_y)
        if (new_pos[0] < 0) and (old_pos[0] >= 0): new_pos = (0, new_pos[1])
        if (new_pos[1] < 0) and (old_pos[1] >= 0): new_pos = (new_pos[0], 0)
        # TODO: pos should get a vector and not two variables
        self.set_pos(new_pos[0], new_pos[1])

    def play_image(self, screen):
        total_play = self.image.get_rect().size[0]
        sprite = (int(self.frame) * self.size_x) % total_play
        screen.blit(self.image, (self.x, self.y), pygame.Rect(sprite, 0, self.size_x, self.size_y ))
        self.frame += (0.1 * self.play_speed)

    def playonce_image(self, screen):
        total_play = self.image.get_rect().size[0]
        sprite = (int(self.frame) * self.size_x) % total_play
        screen.blit(self.image, (self.x, self.y), pygame.Rect(sprite, 0, self.size_x, self.size_y ))
        if (int(self.frame) * self.size_x) != (total_play - self.size_x):
            self.frame += (0.1 * self.play_speed)


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
        
    def set_vx(self, new_vx):
        self.vx = new_vx
 
    def set_vy(self, new_vy):
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

    def stop(self):
        self.ax = 0 
        self.ay = 0
        self.vx = 0
        self.vy = 0


    def update(self):
        # so far we only move
        self.rect = self._move()
        return self.rect

    def _move(self):
        self.vx += self.ax
        self.vy += self.ay
        #self.x += self.vx
        #self.y += self.vy
        self.raw_x = self.x + self.vx
        self.raw_y = self.y + self.vy
        self.x = int(self.raw_x) 
        self.y = self.raw_y
        
        return [self.x, self.y]

    def _draw(self, screen):
        if self.image_type == "static":
            self.rendered.draw(screen)
        elif self.image_type == "play":
            self.play_image(screen)
        elif self.image_type == "playonce":
            self.playonce_image(screen)

