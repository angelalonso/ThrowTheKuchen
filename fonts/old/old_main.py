import pygame
from sys import exit
import random
import screeninfo

from item import Item
from kuchen import Kuchen
from collision import check_collision_boundaries, check_collision
from button import Button
from textbox import Textbox

## Functions

def throw(thrownObject, Status, WIND):
    NewStatus = Status.split('_')[0] + "_Threw"
    # We correct angle for -y and both players here instead of under item.py
    if Status[0:2] == "P1":
        corrected_angle = 90 - int(throw_angle)
    elif Status[0:2] == "P2":
        corrected_angle = 270 + int(throw_angle)
    thrownObject.set_v_vector(throw_force, corrected_angle)
    thrownObject.set_a(WIND, GRAVITY)
    return NewStatus

def nextPlayer(Status): 
    if Status[0:2] == "P1":
        NewStatus = "P2_Ready"
        Kuchen.set_pos(MAX_X - 15, MAX_Y - 15)
    elif Status[0:2] == "P2":
        NewStatus = "P1_Ready"
        Kuchen.set_pos(15, MAX_Y - 15)
    else:
        NewStatus = Status
    NewWind = get_wind()
    return NewStatus, NewWind

def get_wind():
    #0.05 is fine
    newWind = random.randint(-5, 5) / 100
    return newWind

## Constants
FPS = 60
MAX_X = 1024
MAX_Y = 580
GRAVITY = 0.1
WIND = get_wind()

  # COLORS
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
BLACK = (0, 0, 0)

## Init Variables
  # Default Forces Values
throw_force = 5
throw_angle = 45
score_P1 = 0
score_P2 = 0

  # Images
Kuchen_sprite = pygame.image.load("drawables/kuchen.png")
P1_sprite = pygame.image.load("drawables/player1.png")
P2_sprite = pygame.image.load("drawables/player2.png")

  # Sizes
Kuchen_size_x = 10
Kuchen_size_y = 10 
P1_size_x = 20
P1_size_y = 20 
P2_size_x = 20
P2_size_y = 20 

  # Positions
Kuchen_pos = (15, MAX_Y - 15)
P1_pos = (0, MAX_Y - P1_size_y)
P2_pos = (MAX_X - P2_size_x, MAX_Y - P2_size_y)

  # Init of Items in the game
Kuchen = Kuchen(Kuchen_size_x, Kuchen_size_y, Kuchen_pos[0], Kuchen_pos[1])
Kuchen.set_v(0, 0)
#Kuchen.set_a(0, GRAVITY)
Player1 = Item(P1_size_x, P1_size_y, P1_pos[0], P1_pos[1])
Player1.set_v(0, 0)
Player1.set_a(0, GRAVITY)
Player2 = Item(P2_size_x, P2_size_y, P2_pos[0], P2_pos[1])
Player2.set_v(0, 0)
Player2.set_a(0, GRAVITY)

  # Pygame elements
pygame.init()
pygame.font.init()
gameDisplay = pygame.display
screen = gameDisplay.set_mode((MAX_X, MAX_Y))
gameDisplay.set_caption('Throw the Kuchen')
clock = pygame.time.Clock()

  # User Interface Elements
if WIND < 0: windMsg = str(abs(WIND)) + " ->"
elif WIND > 0: windMsg = "<- " + str(abs(WIND))
else: windMsg = str(abs(WIND))
windTxt = Textbox(windMsg , (200, 0))
forceTxt = Textbox(str(throw_force), (200, 50))
angleTxt = Textbox(str(int(throw_angle)), (200, 100))
throwButton = Button("drawables/button_throw.png", (200, 200), "Throw!")
continueButton = Button("drawables/button_continue.png", (200, 200), "Press to continue")

# Statuses: 
#  JustStarted
#  Px_Ready
#  Px_Threw
#  Px_Hit
#  Px_Missed
gameStatus = "JustStarted"
# Just in case we want to start randomly here
gameStatus = "P1_Ready"
score_added = False

while not gameStatus == "Finished":
    Kuchen_pos = Kuchen.get_pos()
    screen.fill(0)
    screen.blit(P1_sprite, P1_pos)
    screen.blit(P2_sprite, P2_pos)
    screen.blit(Kuchen_sprite, Kuchen_pos)
    if (gameStatus[2:] == "_Ready"):
        windTxt.draw(screen)
        forceTxt.draw(screen)
        angleTxt.draw(screen)
        throwButton.draw(screen)
    elif (gameStatus[2:] == "_Threw"):
        Kuchen_pos = Kuchen.update()
        if (gameStatus[0:2] == "P1"):
            gameStatus = check_collision(Kuchen, Player2, gameStatus)
        elif (gameStatus[0:2] == "P2"):
            gameStatus = check_collision(Kuchen, Player1, gameStatus)
        if gameStatus != "P1_Hit" and gameStatus != "P2_Hit":
            gameStatus = check_collision_boundaries(Kuchen, 0, 0, MAX_X, MAX_Y, gameStatus)
    elif (gameStatus[2:] == "_Missed"):
        continueButton.draw(screen)
    elif (gameStatus[2:] == "_Hit"):
        if score_added == False:
            if gameStatus[0:2] == "P1":
                score_P1 += 1
            elif gameStatus[0:2] == "P2":
                score_P2 += 1
            score_added = True
        PxWinsTxt = Textbox(gameStatus[0:2] + " Wins!", (200, 50))
        WinCounterTxt = Textbox(str(score_P1) + " : " + str(score_P2), (200, 150))
        PxWinsTxt.draw(screen)
        WinCounterTxt.draw(screen)
        continueButton.draw(screen)

    delta_angle = 0
    delta_force = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if throw_angle < 90:
            throw_angle += 0.05
        else:
            throw_angle = 90
    if keys[pygame.K_DOWN]:
        if throw_angle > 0:
            throw_angle -= 0.05
        else:
            throw_angle = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mousepos = pygame.mouse.get_pos()
            tb_area = throwButton.get_area()
            cb_area = continueButton.get_area()
            if tb_area[0] < mousepos[0] < tb_area[1] and tb_area[2] < mousepos[1] < tb_area[3]:
                gameStatus = throw(Kuchen, gameStatus, WIND)
                if WIND < 0: windMsg = str(abs(WIND)) + " ->"
                elif WIND > 0: windMsg = "<- " + str(abs(WIND))
                else: windMsg = str(abs(WIND))
                windTxt = Textbox(windMsg , (200, 0))
            if cb_area[0] < mousepos[0] < cb_area[1] and cb_area[2] < mousepos[1] < cb_area[3]:
                if gameStatus[2:] == "_Hit":
                    score_added = False
                gameStatus, WIND = nextPlayer(gameStatus)
                if WIND > 0: windMsg = str(abs(WIND)) + " ->"
                elif WIND < 0: windMsg = "<- " + str(abs(WIND))
                else: windMsg = str(abs(WIND))
                windTxt = Textbox(windMsg , (200, 0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                delta_angle = 1
            if event.key == pygame.K_DOWN:
                delta_angle = -1
            if event.key == pygame.K_LEFT:
                delta_force = -1
            if event.key == pygame.K_RIGHT:
                delta_force = 1
            if event.key == pygame.K_RETURN:
                if gameStatus[2:] == "_Ready":
                    gameStatus = throw(Kuchen, gameStatus, WIND)
                elif gameStatus[2:] == "_Missed" or gameStatus[2:] == "_Hit":
                    if gameStatus[2:] == "_Hit":
                        score_added = False
                    gameStatus, WIND = nextPlayer(gameStatus)
                    if WIND > 0: windMsg = str(abs(WIND)) + " ->"
                    elif WIND < 0: windMsg = "<- " + str(abs(WIND))
                    else: windMsg = str(abs(WIND))
                    windTxt = Textbox(windMsg , (200, 0))
                    screen.blit(Kuchen_sprite, Kuchen_pos)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                delta_angle = 0
            if event.key == pygame.K_DOWN:
                delta_angle = 0
            if event.key == pygame.K_LEFT:
                delta_force = 0
            if event.key == pygame.K_RIGHT:
                delta_force = 0

    throw_angle += delta_angle
    throw_force += delta_force
    forceTxt = Textbox(str(throw_force), (200, 50))
    angleTxt = Textbox(str(int(throw_angle)), (200, 100))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()

