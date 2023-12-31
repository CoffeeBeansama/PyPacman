import sys
import pygame as pg
from level import Level
from settings import *

class Game:
    def __init__(self):
        pg.init()


        self.GameRunning = True
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        pg.display.set_caption("PyPacman")
        self.clock = pg.time.Clock()
        self.level = Level(self)

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







            self.screen.fill("black")
            self.level.run()
            pg.display.update()

            self.clock.tick(FPS)


game = Game()
game.run()