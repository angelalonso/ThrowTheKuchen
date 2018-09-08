import os
import pygame

class Background():
    def __init__(self, image_file):
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        img_dir = os.path.join(main_dir, 'drawables')
        fullname = os.path.join(img_dir, image_file)
        self.image = pygame.image.load(fullname)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def update(self, screen, elements):
        for i in elements:
            pos = i.get_pos()
            size = i.get_size()
            screen.blit(self.image, (pos[0], pos[1]), pygame.Rect(pos[0], pos[1], size[0], size[1] ))
