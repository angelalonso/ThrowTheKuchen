#!/usr/bin/env python3

# TODO:
# After hitting, change players' positions
# Use moving sprite for throwing players, block throw until playonce is done
# do not allow to change force or angle after throwing
# add drag to items
# Show and hide UI accordingly
# show hints button (Press Enter, Next up Player 2...etc), popup help with keys to use
# COnfig screen at start, Several game modes, different names...
# on p1 being hit, kuchen appears at pos_x -10
# Order and standard names and functions


#Import Modules
import os 
import pygame, random
from pygame.compat import geterror
from pygame.locals import *
from background import Background
from collision import check_collision_boundaries, check_collision
from item import Item
from uitxt import UiTxt

# Functions to manage generic objects, such as sound
# TODO: use or remove
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
main_dir = os.path.split(os.path.abspath(__file__))[0]
snd_dir = os.path.join(main_dir, 'sounds')


def load_sound(name):
    """
    Function to load a given Sound from a file
    """
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
    """
    Game class for "Throw the kuchen"
    Originally based on pygame's chimp example

    It manages the game itself
    """
    # Load constants
    ## ENVIRONMENT constants
    FPS = 60
    MAX_X = 1024
    MAX_Y = 580
    CENTER_X = MAX_X // 2
    CENTER_Y = MAX_Y // 2
    MAX_FORCE = 20
    ## game and object-related constants
    gravity = 0.1
    # Initialize some variables
    wind = 0
    status = "P1_Ready"
    player1_force = player2_force = 5
    player1_angle = player2_angle = 45
    player1_score = player2_score = 0
    kuchen_collision = "none"


    def __init__(self, fps):
        # Load variables
        self.FPS = fps
        self.wind = random.randint(-5, 5) / 100
        self.player1_height = random.randint(self.MAX_Y // 3, self.MAX_Y - 20)
        self.player2_height = random.randint(self.MAX_Y // 3, self.MAX_Y - 20)
        self.score = (0, 0)
    
        # Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAX_X, self.MAX_Y))
        pygame.display.set_caption('Throw the Kuchen')
        pygame.mouse.set_visible(0)

        # Create and display the Backgound 
        self.background = Background("bg.png")
        self.background.draw(self.screen)

        pygame.display.flip()

        # Prepare Game Objects
        self.clock = pygame.time.Clock()
        #whiff_sound = load_sound('whiff.wav')
        #punch_sound = load_sound('punch.wav')
        self.snowItems = []
        self.manageSnow()
        self.snowSprites = pygame.sprite.RenderPlain((self.snowItems))

        self.playerItems = []
        # TODO: correct the - 20 on the class itself
        self.player1 = Item(0, self.player1_height, "player1.png")
        self.playerItems.append(self.player1)
        self.player2 = Item(self.MAX_X - 20, self.player2_height, "player2.png")
        self.playerItems.append(self.player2)
        self.playerSprites = pygame.sprite.RenderPlain((self.playerItems))

        self.kuchenItems = []
        self.kuchen = Item(15, self.player1_height + 5, "kuchen_transparent.png", -1)
        self.kuchenItems.append(self.kuchen)
        self.kuchenSprites = self.kuchen.render_image()
                    
        self.uiItems = []
        self.txtWindTitle = UiTxt((self.CENTER_X, 5), " WIND:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtWindTitle)
        self.txtWind = UiTxt((self.CENTER_X, 20), self.wind, "txtWind", "center")
        self.uiItems.append(self.txtWind)
        self.txtScore = UiTxt((self.CENTER_X, self.CENTER_Y // 2), self.score, "txtScore", "center")
        self.uiItems.append(self.txtScore)
        self.txtStatus = UiTxt((self.CENTER_X, self.CENTER_Y), self.status, "txtStatus", "center")
        self.uiItems.append(self.txtStatus)

        # Some Ui elements show up relative to the Player's position
        p1_pos = self.player1.get_pos()
        new_pos = (p1_pos[0] + 150, p1_pos[1] - 100)
        self.txtForceTitle = UiTxt(new_pos, " FORCE:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtForceTitle)
        self.txtForce = UiTxt((new_pos[0], new_pos[1] + 15), (self.player1_force, 0, self.MAX_FORCE), "txtForce", "center")
        self.uiItems.append(self.txtForce)
        self.txtAngleTitle = UiTxt((new_pos[0], new_pos[1] + 50), " ANGLE:", "txtStaticTitle", "center")
        self.uiItems.append(self.txtAngleTitle)
        self.txtAngle = UiTxt((new_pos[0], new_pos[1] + 65), (self.player1_angle, 0, 90), "txtAngle", "center")
        self.uiItems.append(self.txtAngle)


    def drawAll(self):
        """
        Function to draw all elements, grouped and in order
        """
        # Display The Background first,
        self.background.draw(self.screen)
        pygame.display.flip()
        #  then render the players and finally the kuchen
        self.playerSprites = pygame.sprite.RenderPlain((self.playerItems))
        self.kuchenSprites = self.kuchen.render_image()


    def manageKuchen(self):
        """
        Function to change the image(s) to display for the kuchen,
         depending on the situation
        """
        if self.kuchen_collision in ("wall_left", "player_left"):
            kuchenimage = "kuchen_splash_left.png"
        elif self.kuchen_collision in ("wall_right", "player_right"):
            kuchenimage = "kuchen_splash_right.png"
        else:
            kuchenimage = "kuchen_splash_down.png"
        self.kuchen.load_image_playonce(kuchenimage, 20, -1, 5)


    def manageSnow(self):
        """
        Function to manage the amount and position of snowflakes
        """
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
                i.set_x(1)
            elif i.get_x() < 1:
                i.set_x(self.MAX_X)
    

    def getKeys(self):
        """
        Function to handle input events
        """
        keys = pygame.key.get_pressed()                                                                                      
        for event in pygame.event.get():
            if event.type == QUIT:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if (self.status[0:2] == "P1"):
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtForce.increase_value(10)
                    else:
                        self.txtForce.increase_value()
                else:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtForce.decrease_value(10)
                    else:
                        self.txtForce.decrease_value()
            elif event.type == KEYDOWN and event.key == K_LEFT:
                if (self.status[0:2] == "P1"):
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtForce.decrease_value(10)
                    else:
                        self.txtForce.decrease_value()
                else:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtForce.increase_value(10)
                    else:
                        self.txtForce.increase_value()
            elif event.type == KEYDOWN and event.key == K_UP:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtAngle.increase_value(10)
                    else:
                        self.txtAngle.increase_value()
            elif event.type == KEYDOWN and event.key == K_DOWN:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.txtAngle.decrease_value(10)
                    else:
                        self.txtAngle.decrease_value()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                if (self.status[2:] == "_Ready"):
                    self.throw(self.kuchen)
                elif (self.status[2:] == "_Hit" or self.status[2:] == "_Missed"):
                    self.changeTurn()


    def changeTurn(self):
        """
        Function to manage tasks to get the game ready for the next player
        """
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
             
        # "Reset" kuchen's image to the main static image
        self.kuchen.load_image_static("kuchen_transparent.png", -1)
        self.drawAll()
        # Change the position of kuchen relative to the player that will be throwing next
        if self.status[0:2] == "P2":
            self.kuchen.set_pos(self.MAX_X - 20 - (self.kuchen.get_size_x() // 2), self.player2_height + 5)
            p2_pos = self.player2.get_pos()
            new_pos = (p2_pos[0] - 150, p2_pos[1] - 100)
        elif self.status[0:2] == "P1":
            self.kuchen.set_pos(20 - (self.kuchen.get_size_x() // 2), self.player1_height + 5)
            p1_pos = self.player1.get_pos()
            new_pos = (p1_pos[0] + 150, p1_pos[1] - 100)
        # Change the position of some UI elements that remain relative to the player that will throw next
        self.txtForceTitle.set_pos(new_pos)
        self.txtForce.set_pos((new_pos[0], new_pos[1] + 15))
        self.txtAngleTitle.set_pos((new_pos[0], new_pos[1] + 50))
        self.txtAngle.set_pos((new_pos[0], new_pos[1] + 65))
             
        # On each new turn, the wind changes
        self.wind = random.randint(-5, 5) / 100
        self.txtWind.set_value(self.wind)
        # LAst but not least, update the score
        self.txtScore.set_value(self.score)
        self.txtStatus.set_value(self.status)


    def throw(self, thrownObject):
        """
        Function to manage the action of throwing the kuchen
        """
        self.kuchen.load_image_play("kuchen_rotate_clock.png", 10, -1)
        self.status = self.status.split('_')[0] + "_Threw"
        self.txtStatus.set_value(self.status)
        angle = self.txtAngle.get_value()
        # Adjust image rotation speed to force of throw
        if self.txtForce.get_value() < 5: 
            image_speed = 3
        elif self.txtForce.get_value() < 13: 
            image_speed = self.txtForce.get_value() - 2
        else: 
            image_speed = 10
        # The same angle needs to be modified to send the kuchen on one direction or the opposite,
        #  also, the direction of the rotation image has to change
        if self.status[0:2] == "P1":         
            corrected_angle = 90 - int(angle)
            self.kuchen.load_image_play("kuchen_rotate_clock.png", 10, -1, image_speed)
        elif self.status[0:2] == "P2":       
            corrected_angle = 270 + int(angle)
            self.kuchen.load_image_play("kuchen_rotate_counter.png", 10, -1, image_speed)
        # Finally, set a starting vector of velocity for the kuchen object
        thrownObject.set_v_vector(self.txtForce.get_value(), corrected_angle)
        thrownObject.set_a(self.wind, self.gravity)


    def getCollisions(self):                                                                                                 
        """
        Function to check if the kuche collides with one of the players or the boundaries
        """
        new_pos = self.kuchen.get_pos()
        self.kuchen_collision = "none"
        if (self.status[0:2] == "P1"):
            self.status, self.kuchen_collision = check_collision(self.kuchen, self.player2, self.status)
        elif (self.status[0:2] == "P2"):
            self.status, self.kuchen_collision = check_collision(self.kuchen, self.player1, self.status)

        if self.status != "P1_Hit" and self.status != "P2_Hit":
            self.status, self.kuchen_collision = check_collision_boundaries(self.kuchen, 0, 0, self.MAX_X, self.MAX_Y, self.status)
        else:
            if (self.status == "P1_Hit"):
                self.score = (self.score[0] + 1, self.score[1])
            elif (self.status == "P2_Hit"):
                self.score = (self.score[0], self.score[1] + 1)
        if (self.status[2:] == "_Hit") or (self.status[2:] == "_Missed"):
            #self.kuchen.load_image_play("kuchen_splash_down.png", -1)
            self.manageKuchen()
        self.txtStatus.set_value(self.status)
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

            # Update all objects
            self.manageSnow()
            self.snowSprites.update()
            self.snowSprites = pygame.sprite.RenderPlain((self.snowItems))

            self.playerSprites.update()
            self.kuchenSprites.update()
            for uiItem in self.uiItems: uiItem.update()

            #Draw those objects
            self.snowSprites.draw(self.screen)
            self.playerSprites.draw(self.screen)
            #self.kuchenSprites.draw(self.screen)
            self.kuchen._draw(self.screen)
            for uiItem in self.uiItems: uiItem.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

        #Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    newgame = Game(60)
    newgame.run()
