import pygame
from tile import Tile
from settings import *
from Pacman import Pacman
from node import Node
from pellet import *
class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()

        self.eatableSprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.pacmanSprite = pg.sprite.Group()
        self.createMap()


    def pacmanEatLogic(self):

        if self.pacmanSprite:

            for pacman in self.pacmanSprite:
                collisionSprite = pg.sprite.spritecollide(pacman, self.eatableSprites, False)

                if collisionSprite:

                    for target_sprite in collisionSprite:
                        if target_sprite.object_type == "pellet":

                            target_sprite.eat()

                        elif target_sprite.object_type == "Ghost":
                            pass

    def createMap(self):

        for row_index,row in enumerate(map):
            for column_index,column in enumerate(row):

                x = column_index * tilesize
                y = row_index * tilesize

                if column == "*":
                    Smol_pellet(smolpellet,(x,y),[self.visible_sprites,self.eatableSprites],"pellet")

                if column == "W":
                    Tile(wall, (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "B":
                    Tile(blank, (x, y), [self.visible_sprites])

                if column == "b":
                    Big_pellet(bigpellet, (x, y), [self.visible_sprites,self.eatableSprites],"pellet")

                if column == "N":
                    Node(node, (x, y), [self.visible_sprites,self.nodes_sprites])


        self.pacman = Pacman(pacman,(300,360),[self.visible_sprites,self.pacmanSprite],self.collision_sprites,self.nodes_sprites)


    def run(self):
        self.visible_sprites.draw(self.screen)
        self.pacmanEatLogic()
        self.pacman.update()


