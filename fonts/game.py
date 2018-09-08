#!/usr/bin/env python3
"""
Game class for "Throw the kuchen"
Based on pygame's chimp example
"""
# TODO:
# UI message for score
# UI message for next instruction
# Show and hide UI accordingly
# SHIFT + up/down = 10x
# show hints button (Press Enter, Next up Player 2...etc), popup help with keys to use


#Import Modules
import os 
import pygame, random
from pygame.locals import *
from pygame.compat import geterror
from item import Item
#from uitext import UiText
from uitxt import UiTxt
from background import Background
from collision import check_collision_boundaries, check_collision

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
snd_dir = os.path.join(main_dir, 'sounds')
img_dir = os.path.join(main_dir, 'drawables')


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(snd_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

class Game():
    FPS = 60
    MAX_X = 1024
    MAX_Y = 580
    CENTER_X = MAX_X // 2
    CENTER_Y = MAX_Y // 2
    gravity = 0.1
    status = "P1_Ready"
    wind = 0
    player1_force = player2_force = 5
    player1_angle = player2_angle = 45


    def __init__(self, fps):
        # load variables
        self.FPS = fps
        self.wind = random.randint(-5, 5) / 100
    
        #Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAX_X, self.MAX_Y))
        pygame.display.set_caption('Throw the Kuchen')
        pygame.mouse.set_visible(0)

        #Create The Backgound 
        self.background = Background("bg.png")

        #Display The self.background
        self.background.draw(self.screen)
        pygame.display.flip()

        #Prepare Game Objects
        self.clock = pygame.time.Clock()
        whiff_sound = load_sound('whiff.wav')
        punch_sound = load_sound('punch.wav')
        self.snowItems = []
        self.manageSnow()
        self.snowSprites = pygame.sprite.RenderPlain((self.snowItems))

        self.playerItems = []
        # TODO: correct the - 20 on the class itself
        self.player1 = Item(0, self.MAX_Y - 20, "player1.png")
        self.playerItems.append(self.player1)
        self.player2 = Item(self.MAX_X - 20, self.MAX_Y - 20, "player2.png")
        self.playerItems.append(self.player2)
        self.playerSprites = pygame.sprite.RenderPlain((self.playerItems))

        self.kuchenItems = []
        self.kuchen = Item(15, self.MAX_Y - 15, "kuchen.png")
        self.kuchenItems.append(self.kuchen)
        self.kuchenSprites = pygame.sprite.RenderPlain((self.kuchenItems))
                    
        self.uiItems = []
        self.txtWindTitle = UiTxt((self.CENTER_X, 5), " WIND:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtWindTitle)
        self.txtWind = UiTxt((self.CENTER_X, 20), self.wind, "txtWind", "center")
        self.uiItems.append(self.txtWind)
        p1_pos = self.player1.get_pos()
        new_pos = (p1_pos[0] + 150, p1_pos[1] - 100)

        self.txtForceTitle = UiTxt(new_pos, " FORCE:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtForceTitle)
        self.txtForce = UiTxt((new_pos[0], new_pos[1] + 15), (self.player1_force, 0, 24), "txtForce", "center")
        self.uiItems.append(self.txtForce)
        self.txtAngleTitle = UiTxt((new_pos[0], new_pos[1] + 50), " ANGLE:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtAngleTitle)
        self.txtAngle = UiTxt((new_pos[0], new_pos[1] + 65), (self.player1_angle, 0, 90), "txtAngle", "center")
        self.uiItems.append(self.txtAngle)

    def uiShowWind(self):
        if self.wind < 0:
            uiText = "<- " + str(abs(self.wind))
        elif self.wind > 0:
            uiText = str(abs(self.wind)) + " ->"
        elif self.wind == 0:
            uiText = "No Wind"
        return uiText


    def drawAll(self):
        #Display The self.background
        self.background.draw(self.screen)
        pygame.display.flip()

        self.playerSprites = pygame.sprite.RenderPlain((self.playerItems))
        self.kuchenSprites = pygame.sprite.RenderPlain((self.kuchenItems))


    def manageSnow(self):
        max_snow = 100
        new_snow = random.randint(0, self.MAX_Y)
        if len(self.snowItems) < max_snow:
            if new_snow < self.MAX_Y // max_snow:
                snow = Item(random.randint(0, self.MAX_X), 0, "snowflake.png")
                snow.set_vy(1)
                self.snowItems.append(snow)

        for i in self.snowItems:
            i.set_vx(self.wind * 25)
            if i.get_y() >= self.MAX_Y:
                i.set_y(0)
            if i.get_x() > self.MAX_X:
                i.set_x(0)
            elif i.get_x() < 1:
                i.set_x(self.MAX_X)
    

    def getKeys(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if (self.status[0:2] == "P1"):
                    self.txtForce.increase_value()
                else:
                    self.txtForce.decrease_value()
            elif event.type == KEYDOWN and event.key == K_LEFT:
                if (self.status[0:2] == "P1"):
                    self.txtForce.decrease_value()
                else:
                    self.txtForce.increase_value()
            elif event.type == KEYDOWN and event.key == K_UP:
                self.txtAngle.increase_value()
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.txtAngle.decrease_value()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                if (self.status[2:] == "_Ready"):
                    self.throw(self.kuchen)
                elif (self.status[2:] == "_Hit" or self.status[2:] == "_Missed"):
                    self.changeTurn()


    def changeTurn(self):
        # save each player's values and change turn
        if self.status[0:2] == "P1": 
            self.player1_force = self.txtForce.get_value()
            self.player1_angle = self.txtAngle.get_value()
            self.status = "P2_Ready"
            self.txtForce.set_value(self.player2_force)
            self.txtAngle.set_value(self.player2_angle)
        elif self.status[0:2] == "P2": 
            self.player2_force = self.txtForce.get_value()
            self.player2_angle = self.txtAngle.get_value()
            self.status = "P1_Ready"
            self.txtForce.set_value(self.player1_force)
            self.txtAngle.set_value(self.player1_angle)
             
        self.drawAll()
        if self.status[0:2] == "P2":
            self.kuchen.set_pos(self.MAX_X - 20 - (self.kuchen.get_size_x() // 2), self.MAX_Y - 15)
            p2_pos = self.player2.get_pos()
            new_pos = (p2_pos[0] - 150, p2_pos[1] - 100)
        elif self.status[0:2] == "P1":
            self.kuchen.set_pos(20 - (self.kuchen.get_size_x() // 2), self.MAX_Y - 15)
            p1_pos = self.player1.get_pos()
            new_pos = (p1_pos[0] + 150, p1_pos[1] - 100)
        self.txtForceTitle.set_pos(new_pos)
        self.txtForce.set_pos((new_pos[0], new_pos[1] + 15))
        self.txtAngleTitle.set_pos((new_pos[0], new_pos[1] + 50))
        self.txtAngle.set_pos((new_pos[0], new_pos[1] + 65))
             
        self.wind = random.randint(-5, 5) / 100
        self.txtWind.set_value(self.wind)


    def throw(self, thrownObject):
        self.status = self.status.split('_')[0] + "_Threw"
        angle = self.txtAngle.get_value()
        if self.status[0:2] == "P1":         
            corrected_angle = 90 - int(angle)
        elif self.status[0:2] == "P2":       
            corrected_angle = 270 + int(angle)
        thrownObject.set_v_vector(self.txtForce.get_value(), corrected_angle)
        thrownObject.set_a(self.wind, self.gravity)


    def getCollisions(self):                                                                                                 
        new_pos = self.kuchen.get_pos()
        if (self.status[0:2] == "P1"):
            self.status = check_collision(self.kuchen, self.player2, self.status)
        elif (self.status[0:2] == "P2"):
            self.status = check_collision(self.kuchen, self.player1, self.status)
        if self.status != "P1_Hit" and self.status != "P2_Hit":
            self.status = check_collision_boundaries(self.kuchen, 0, 0, self.MAX_X, self.MAX_Y, self.status)
        return new_pos


    def run(self):
            """this function is called when the program starts.
               it initializes everything it needs, then runs in
               a loop until the function returns."""

        #Main Loop
            self.going = True
            while self.going:
                self.clock.tick(self.FPS)

                self.getKeys()
                if (self.status[2:] == "_Threw"):
                    kuchenPos = self.getCollisions() 
                elif (self.status[2:] == "_Hit"):
                    self.kuchen.stop()
                elif (self.status[2:] == "_Missed"):
                    self.kuchen.stop()

                #Draw Background's parts
                self.background.update(self.screen, self.snowItems)
                self.background.update(self.screen, self.playerItems)
                self.background.update(self.screen, self.kuchenItems)
                self.background.update(self.screen, self.uiItems)

                self.manageSnow()
                self.snowSprites.update()
                self.snowSprites = pygame.sprite.RenderPlain((self.snowItems))
                self.playerSprites.update()
                self.kuchenSprites.update()
                for uiItem in self.uiItems: uiItem.update()

                #Draw Everything Else
                self.snowSprites.draw(self.screen)
                self.playerSprites.draw(self.screen)
                self.kuchenSprites.draw(self.screen)
                for uiItem in self.uiItems: uiItem.draw(self.screen)
                pygame.display.flip()

            pygame.quit()

        #Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    newgame = Game(60)
    newgame.run()
