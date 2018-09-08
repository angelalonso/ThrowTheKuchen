# Import Modules
import numpy
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror

# load constants
# ENVIRONMENT constants

BLACK = (0, 0, 0) 
GREY_20 = (200, 200, 200) 
WHITE = (255, 255, 255) 
              
class UiTxt():
    # Initialize some variables
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

              
    def __init__(self, init_pos, values, infotype, txtalign):
        self.init_pos = init_pos
        self.infotype = infotype
        self.txtalign = txtalign
        if self.infotype == "txtWind":
            self.value = self.uiFormatWind(values)
        elif self.infotype == "txtScore":
            self.value = str(values[0]) + " : " + str(values[1])
        if self.infotype == "txtStatus":
            self.value = self.uiFormatStatus(values)
        elif self.infotype == "txtForce" or self.infotype == "txtAngle":
            self.value = values[0]
            self.value_min = values[1]
            self.value_max = values[2]
        elif self.infotype == "txtStatic" or self.infotype == "txtStaticTitle":
            self.value = str(values)
        pygame.font.init()
        #self.FONT = pygame.font.Font('freesansbold.ttf', 24) 
        if self.infotype == "txtScore":
            self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 24) 
        elif self.infotype == "txtStatus":
            self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 24) 
        elif self.infotype == "txtForce" or self.infotype == "txtAngle":
            self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 20) 
        elif self.infotype == "txtStaticTitle":
            self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 15) 
        else:
            self.FONT = pygame.font.Font('fonts/FantasqueSansMono_Regular.ttf', 12) 
        self._show()

    def draw(self, surfaceObject):
        self._show()
        surfaceObject.blit(self.surfText, self.position)

    def _show(self):
        if self.infotype == "txtStatus":
            self.surfText = self.FONT.render(str(self.value), 1, GREY_20)
        else:
            self.surfText = self.FONT.render(str(self.value), 1, WHITE)
        self.rect = self.surfText.get_rect()
        screen = pygame.display.get_surface()
        #self.area = screen.get_rect()
        self.size_x = self.rect.size[0]
        self.size_y = self.rect.size[1]
        self.position = self.uiTxtAlign(self.init_pos, self.txtalign)
        self.x = self.position[0]
        self.y = self.position[1]

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
 
    def set_pos(self, new_pos):
        self.init_pos = new_pos
        self.position = self.uiTxtAlign(self.init_pos, self.txtalign)
        self.x = self.position[0]
        self.y = self.position[1]
 
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
        if self.infotype == "txtWind":
            self.value = self.uiFormatWind(new_value)
        elif self.infotype == "txtScore":
            self.value = str(new_value[0]) + " : " + str(new_value[1])
        elif self.infotype == "txtStatus":
            self.value = self.uiFormatStatus(new_value)
        else:
            try:
                if new_value < self.value_min:
                    self.value = self.value_min
                elif new_value > self.value_max:
                    self.value = self.value_max
                else:
                    self.value = new_value
            except TypeError:
                self.value = new_value


    def increase_value(self, increase=1):
        new_value = self.value + increase 
        if new_value < self.value_min:
            self.value = self.value_min
        elif new_value > self.value_max:
            self.value = self.value_max
        else:
            self.value = new_value

    def decrease_value(self, decrease=1):
        new_value = self.value - decrease 
        if new_value < self.value_min:
            self.value = self.value_min
        elif new_value > self.value_max:
            self.value = self.value_max
        else:
            self.value = new_value

    def get_value(self):
        return self.value

    def uiFormatWind(self, wind):
        if wind < 0:
            uiText = "<-- " + str(abs(wind)) + "    "
        elif wind > 0:
            uiText = "    " + str(abs(wind)) + " -->"
        elif wind == 0:
            uiText = "No Wind"
        return uiText

    def uiFormatStatus(self, info):
        if info == "P1_Ready":
            uiText = "   Player 1 ready..."
        elif info == "P2_Ready":
            uiText = "   Player 2 ready..."
        elif info[2:] == "_Hit":
            uiText = " HIT!!"
        elif info[2:] == "_Missed":
            uiText = "   missed..."
        else:
            uiText = ""
        return uiText

    def uiTxtAlign(self, position, align):
        new_position_y = position[1]
        if align == "left":
            new_position_x = position[0] - self.size_x
        elif align == "center":
            new_position_x = position[0] - (self.size_x // 2)
        else:
            new_position_x = position[0]
        return (new_position_x, new_position_y)

 
    def update(self):
        # so far we only move
        self.rect = self._move()

    def _move(self):
        self.vx += self.ax
        self.vy += self.ay
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)
        
        return [self.x, self.y]

