import pygame
from tile import Tile
from settings import *
from Pacman import Pacman
from node import *
from pellet import *
from ghost import *
class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()

        self.eatableSprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()
        self.invisible_sprites = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.pacmanSprite = pg.sprite.Group()

        self.blinky_pos = (280,280)
        self.pinky_pos = (300,280)
        self.inky_pos = (280, 300)
        self.clyde_pos = (300, 300)
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

                    self.walls = Tile(wall, (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "E":
                    self.Exit1Tile = Tile(blank,(x,y),[self.visible_sprites])
                    self.Exit2Tile = Tile(blank,(x,y),[self.visible_sprites])

                if column == "B":
                    Tile(blank, (x, y), [self.visible_sprites])

                if column == "G":
                    Tile(gate, (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "b":
                    Big_pellet(bigpellet, (x, y), [self.visible_sprites,self.eatableSprites],"pellet")

                if column == "N":
                    self.node = Node(node, (x, y), [self.visible_sprites, self.nodes_sprites])

                    #top
                    if map[row_index-1][column_index] != "W":
                        self.node.availableDirections.append(self.Vector2(0,-1))
                    #bottom
                    if map[row_index+1][column_index] != "W":
                        self.node.availableDirections.append(self.Vector2(0,1))
                    #left
                    if map[row_index][column_index-1] != "W":
                        self.node.availableDirections.append(self.Vector2(-1,0))
                    #right
                    if map[row_index][column_index+1] != "W":
                        self.node.availableDirections.append(self.Vector2(1,0))


        self.pacman = Pacman(pacman, (300, 360), [self.visible_sprites, self.pacmanSprite],self.collision_sprites,self.nodes_sprites)

        self.blinky = Blinky(blinky,self.blinky_pos,[self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node,"Ghost",self.pacman)
        self.pinky = Pinky(pinky,self.pinky_pos,[self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node,"Ghost",self.pacman)
        self.inky = Inky(inky, self.inky_pos, [self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node, "Ghost",self.pacman)
        self.clyde = Clyde(clyde, self.clyde_pos, [self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node, "Ghost",self.pacman)

    def Vector2(self,x,y):
        direction = pg.math.Vector2()

        direction.x = x
        direction.y = y

        return round(direction.x),round(direction.y)



    def run(self):
        self.visible_sprites.draw(self.screen)
        self.pacmanEatLogic()


        self.blinky.update()
        self.pinky.update()
        self.inky.update()

        self.clyde.update()

        self.pacman.update()



