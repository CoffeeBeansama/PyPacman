import pygame as pg
from eventhandler import EventHandler


class GameOver:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 40)
        self.gameOverText = self.font.render("Game Over",True,(255,255,255))

    def handleRendering(self):
        self.screen.blit(self.gameOverText,(65, 60))
        self.playButton = self.screen.blit(self.play, (180, 170))
        self.exitButton = self.screen.blit(self.exit, (212, 250))
        self.sadFace = self.screen.blit(self.sadFace, (180, 320))

    def handleMouseEvent(self):
        if self.playButton.collidepoint(EventHandler.mousePosition()):
           if EventHandler.pressingLeftMouseButton():
              pass
        elif exit_button.collidepoint(mouse_pos):
           if EventHandler.pressingLeftMouseButton():
              pass

    def update(self):
        self.handleRendering()
        self.handleMouseEvent()


