import pygame as pg
from support import loadSprite,drawButton
from settings import Sprites
from eventhandler import EventHandler
import sys

class MainMenu:
    def __init__(self,startGame):
        self.startGame = startGame
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 40)
        self.titleText = self.font.render("pacman",True,(255,255,255))
        
        self.displaySettings = False
        
        self.buttonFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 28)
        

    def playButton(self):
        text = self.buttonFont.render("play",True,(255,255,255))
        return drawButton(self.screen,200,220,180,55,text)

    def quitButton(self):
        text = self.buttonFont.render("quit",True,(255,255,255))
        return drawButton(self.screen,200,290,180,55,text)

    def handleRendering(self):
        self.playButton()
        self.quitButton()
        self.drawTitleText()

    def drawTitleText(self):
        return self.screen.blit(self.titleText,(120,62))
    

    def handleEventTriggers(self):
        if self.playButton().collidepoint(EventHandler.mousePosition()):
           if EventHandler.pressingLeftMouseButton():
              self.startGame()
              return

        if self.quitButton().collidepoint(EventHandler.mousePosition()):
           if EventHandler.pressingLeftMouseButton():
              pg.quit()
              sys.exit()

    def update(self):
        self.handleRendering()
        self.handleEventTriggers()
