import pygame as pg
from eventhandler import EventHandler
from support import drawButton
import sys

class GameOver:
    def __init__(self,resetGame):
        self.screen = pg.display.get_surface()
        self.resetGame = resetGame
        self.gameOverFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf",40)
        self.gameOverText = self.gameOverFont.render("game over",True,(255,255,255))
        self.buttonFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 28)

    def playButton(self):
        text = self.buttonFont.render("play",True,(255,255,255))
        return drawButton(self.screen,200,260,180,55,text)

    def quitButton(self):
        text = self.buttonFont.render("quit",True,(255,255,255))
        return drawButton(self.screen,200,340,180,55,text)

    def handleRendering(self):
        gameOverText = self.screen.blit(self.gameOverText,(65, 80))
        
        self.playButton()
        self.quitButton()


    def handleMouseEvent(self):
        if self.playButton().collidepoint(EventHandler.mousePosition()):
           if EventHandler.pressingLeftMouseButton():
              self.resetGame()

        elif self.quitButton().collidepoint(EventHandler.mousePosition()):
           if EventHandler.pressingLeftMouseButton():
              pg.quit()
              sys.exit()


    def update(self):
        self.handleRendering()
        self.handleMouseEvent()


