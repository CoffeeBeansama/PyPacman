import pygame as pg
from tile import Tile
from settings import *
from Pacman import Pacman
from node import *
from pellet import *
from ghost import *
from portal import Portal
class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()

        self.eatableSprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()
        self.portal_sprite = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.pacmanSprite = pg.sprite.Group()

        self.blinky_pos = (280,280)
        self.pinky_pos = (300,280)
        self.inky_pos = (280, 300)
        self.clyde_pos = (300, 300)
        self.createMap()
        
        self.PowerUp = pg.USEREVENT







    def pacmanEatLogic(self):

        if self.pacmanSprite:

            for pacman in self.pacmanSprite:
                collisionSprite = pg.sprite.spritecollide(pacman, self.eatableSprites, False)

                if collisionSprite:

                    for target_sprite in collisionSprite:
                        if target_sprite.object_type == "pellet":

                            target_sprite.eat()

                        if target_sprite.object_type == "PowerPellet":
                            target_sprite.powerUp(self.pacman)
                            pg.time.set_timer(self.PowerUp,12000)
                            target_sprite.eat()




                        elif target_sprite.object_type == "Ghost":
                            pass




    def createMap(self):

        for row_index,row in enumerate(map):
            for column_index,column in enumerate(row):

                x = column_index * tilesize
                y = row_index * tilesize



                if column == "*":
                    Smol_pellet(Sprites["SmallPellet"],(x,y),[self.visible_sprites,self.eatableSprites],"pellet")

                if column == "W":

                    self.walls = Tile(Sprites["Wall"], (x, y), [self.visible_sprites,self.collision_sprites])


                if column == "E":
                    self.Exit1Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])
                    self.Exit2Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                if column == "B":
                    Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                if column == "G":
                    Tile(Sprites["Gate"], (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "PP":
                    PowerPellet(Sprites["PowerPellet"], (x, y), [self.visible_sprites, self.eatableSprites],"PowerPellet")

                if column == "N":
                    self.node = Node(Sprites["Node"], (x, y), [self.visible_sprites, self.nodes_sprites])

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

        self.portal = Portal(Sprites["Blank"], (20, 300), [self.portal_sprite],(560, 310))
        self.portal = Portal(Sprites["Blank"], (560, 300), [self.portal_sprite],(40, 310))

        self.pacman = Pacman(Sprites["Pacman"], (300, 360), [self.visible_sprites, self.pacmanSprite],self.collision_sprites,self.nodes_sprites,self.portal_sprite)

        self.blinky = Blinky(Sprites["Blinky"],self.blinky_pos,[self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node,"Ghost",self.pacman,self.portal_sprite)
        self.pinky = Pinky(Sprites["Pinky"],self.pinky_pos,[self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node,"Ghost",self.pacman,self.portal_sprite)
        self.inky = Inky(Sprites["Inky"], self.inky_pos, [self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node, "Ghost",self.pacman,self.portal_sprite)
        self.clyde = Clyde(Sprites["Clyde"], self.clyde_pos, [self.visible_sprites],self.collision_sprites,self.nodes_sprites,self.node, "Ghost",self.pacman,self.portal_sprite)

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





