import pygame

BLACK = (0, 0, 0) 
GREY = (127, 127, 127) 
WHITE = (255, 255, 255) 
 
 
class Textbox:
 
    def __init__(self, text, position):
        pygame.font.init()
        FONT = pygame.font.Font('freesansbold.ttf', 24)
        self.surfText = FONT.render(text, True, BLACK, WHITE)
        self.size = self.surfText.get_rect().size
        self.position = (position[0] - (self.size[0]//2), position[1])

    def draw(self, surfaceObject):
        surfaceObject.blit(self.surfText, self.position)

