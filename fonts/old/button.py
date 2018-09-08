import pygame
from pygame.locals import *
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)


class Button:

    def __init__(self, sprite, position, text):
        self.sprite = sprite

        self.imagesurface = pygame.image.load(sprite)
        self.size = self.imagesurface.get_rect().size
        self.position = (position[0] - (self.size[0]//2), position[1])
        self.surface = pygame.surface.Surface(self.size) 

        #self.font = pygame.font.init()
        BUTTON_FONT = pygame.font.Font('freesansbold.ttf', 44)
        self._rect = pygame.Rect(position[0], position[1], 170, 60)
        self.surfNormal = pygame.Surface(self._rect.size)
        self._font = BUTTON_FONT
        self.text =  text
        self.surfText = self._font.render(self.text, True, BLACK, WHITE)
        self.positionText = (self.position[0] + (self._rect.size[0] // 2) - (self.surfText.get_width() // 2), 
                self.position[1] + (self._rect.size[1] // 2) - (self.surfText.get_height() // 2))
       # self._update()

    def draw(self, surfaceObject):
        self.surfNormal.fill(WHITE)
        surfaceObject.blit(self.surfNormal, self.position)
        surfaceObject.blit(self.surfText, self.positionText)

    def get_imagesurface(self):
        return self.imagesurface

    def get_pos(self):
        return self.position


    def get_area(self):
        area = (self.position[0], self.position[0] + self.size[0], 
                self.position[1], self.position[1] + self.size[1])
        return area
