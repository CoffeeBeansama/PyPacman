import pygame
from tile import Tile
from settings import *
from Pacman import Pacman
from node import Node

class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()

        self.visible_sprites = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.createMap()


    def createMap(self):

        for row_index,row in enumerate(map):
            for column_index,column in enumerate(row):

                x = column_index * tilesize
                y = row_index * tilesize

                if column == "*":
                    Tile(smolpellet,(x,y),[self.visible_sprites])

                if column == "W":
                    Tile(wall, (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "B":
                    Tile(blank, (x, y), [self.visible_sprites])

                if column == "b":
                    Tile(bigpellet, (x, y), [self.visible_sprites])

                if column == "N":
                    Node(node, (x, y), [self.visible_sprites,self.nodes_sprites])


        self.pacman = Pacman(pacman,(300,360),[self.visible_sprites],self.collision_sprites,self.nodes_sprites)


    def run(self):
        self.visible_sprites.draw(self.screen)
        self.pacman.update()

