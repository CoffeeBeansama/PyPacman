import sys
import pygame as pg
from level import Level
from settings import *
from eventhandler import EventHandler
from mainmenu import MainMenu
from gameover import GameOver

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.GameRunning = True
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        pg.display.set_caption("PyPacman")
        self.clock = pg.time.Clock()
        
        self.mainMenu = MainMenu(self.startGame,self.exitGame)
        self.level = Level(self)
        self.gameOver = GameOver()

        self.currentScene = "Level"
        self.scenes = {
            "Main Menu" : self.mainMenu.update,
            "Level" : self.level.update,
            "Game Over" : self.gameOver.update
        }   


    def onPacmanKilled(self):
        self.currentScene = "Game Over"
    

    def startGame(self):
        self.currentScene = "Level"

    def exitGame(self):
        self.GameRunning = False

    def run(self):
        while self.GameRunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == self.level.PowerPelletEaten:
                    self.level.DisablePowerUp()

                if event.type == self.level.GhostchaseMode:
                    for ghost in self.level.ghosts:
                        ghost.chaseState = True

            
            EventHandler.handlePlayerInput()
            self.screen.fill("black")
            
            scene = self.scenes.get(self.currentScene)
            scene()

            pg.display.update()

            self.clock.tick(FPS)


game = Game()
game.run()
