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

        self.eatable_sprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()

        self.portal_sprite = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.pacman_Sprite = pg.sprite.Group()

        self.ghostNumber = 4
        self.blinky_pos = (280,280)
        self.pinky_pos = (300,280)
        self.inky_pos = (280, 300)
        self.clyde_pos = (300, 300)
        self.createMap()

        self.PowerUp = pg.USEREVENT

        self.pacmanEaten = False

    def PacmanCollisionLogic(self):

        if self.pacman_Sprite:

            for pacman in self.pacman_Sprite:
                collisionSprite = pg.sprite.spritecollide(pacman, self.eatable_sprites, False)

                if collisionSprite:

                    for target_sprite in collisionSprite:
                        if target_sprite.object_type == "pellet":

                            target_sprite.eat()

                        if target_sprite.object_type == "PowerPellet":

                            target_sprite.powerUp(self.pacman)
                            pg.time.set_timer(self.PowerUp,12000)
                            target_sprite.eat()

                        if target_sprite.object_type == "Ghost":

                            if self.pacman.PowerUp:

                                target_sprite.currentState.SwitchState(target_sprite.stateCache.EatenState())

                            else:
                                self.pacmanEaten = True
                                self.pacman.kill()

    def createMap(self):

        for row_index,row in enumerate(map):
            for column_index,column in enumerate(row):

                x = column_index * tilesize
                y = row_index * tilesize

                if column == "*":
                    pass
                    self.smallPellet = Smol_pellet(Sprites["SmallPellet"], (x,y), [self.visible_sprites, self.eatable_sprites], "pellet")

                if column == "W":

                    self.walls = Tile(Sprites["Wall"], (x, y), [self.visible_sprites,self.collision_sprites])


                if column == "E":
                    self.Exit1Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                    self.Exit2Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                if column == "B":
                    Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                if column == "G":
                    Tile(Sprites["Gate"], (x, y), [self.visible_sprites])

                if column == "PP":
                    PowerPellet(Sprites["PowerPellet"], (x, y), [self.visible_sprites, self.eatable_sprites], "PowerPellet")

                if column == "N":
                    self.node = Node(Sprites["Blank"], (x, y), [self.visible_sprites, self.nodes_sprites])
                    self.smallPellet = Smol_pellet(Sprites["SmallPellet"], (x, y), [self.visible_sprites, self.eatable_sprites], "pellet")

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

        self.pacman = Pacman(Sprites["Pacman"], (300, 360), [self.visible_sprites, self.pacman_Sprite], self.collision_sprites, self.nodes_sprites, self.portal_sprite)

        self.blinky = Blinky(Sprites["Blinky"], self.blinky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite)
        self.pinky = Pinky(Sprites["Pinky"], self.pinky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite)
        self.inky = Inky(Sprites["Inky"], self.inky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite)
        self.clyde = Clyde(Sprites["Clyde"], self.clyde_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite)

    def GameOver(self):
        allPelletsConsumed = len(self.eatable_sprites) - self.ghostNumber <= 0

        if self.pacmanEaten:
            return True
        elif allPelletsConsumed:
            return True

        return False
    def Vector2(self,x,y):
        direction = pg.math.Vector2()

        direction.x = x
        direction.y = y

        return round(direction.x),round(direction.y)

    def run(self):
        self.visible_sprites.draw(self.screen)

        self.PacmanCollisionLogic()

        if not self.GameOver():
            self.blinky.update()
            self.pinky.update()
            self.inky.update()
            self.clyde.update()

        self.pacman.update()





