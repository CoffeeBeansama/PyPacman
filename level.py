import pygame as pg
from pygame import mixer
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

        self.startLevel = False
        self.ghostNumber = 4
        self.blinky_pos = (280,300)
        self.pinky_pos = (280,300)
        self.inky_pos = (260, 300)
        self.clyde_pos = (300, 300)
        self.createMap()

        self.PowerUp = pg.USEREVENT
        self.StartGame = pg.USEREVENT

        self.pacmanEaten = False

        self.title = pg.transform.scale(pg.image.load(Sprites["Title"]),(350,80))
        self.play = pg.transform.scale(pg.image.load(Sprites["Play Button"]), (200, 65))
        self.pelletSoundIndex = 0

        self.pelletSound1 = mixer.Sound(Sounds["Pellet1"])
        self.pelletSound2 = mixer.Sound(Sounds["Pellet2"])

        mixer.music.load(Sounds["BGM"])
        mixer.music.set_volume(0.08)
        mixer.music.play(-1)



    def PlaySFX(self,object):

        if object == "Pellet":
            sfx = [self.pelletSound1,self.pelletSound2]
            self.pelletSoundIndex += 1

            if self.pelletSoundIndex >= len(sfx):
                self.pelletSoundIndex = 0

            pg.mixer.Sound.play(sfx[self.pelletSoundIndex])

        if object == "PowerPellet":
            pass

    def PacmanCollisionLogic(self):

        if self.pacman_Sprite:

            for pacman in self.pacman_Sprite:
                collisionSprite = pg.sprite.spritecollide(pacman, self.eatable_sprites, False)

                if collisionSprite:

                    for target_sprite in collisionSprite:
                        if target_sprite.object_type == "pellet":

                            self.PlaySFX("Pellet")
                            target_sprite.eat()


                        if target_sprite.object_type == "PowerPellet":

                            self.PlaySFX("PowerPellet")
                            target_sprite.powerUp(self.pacman)
                            pg.time.set_timer(self.PowerUp,12000)
                            target_sprite.eat()

                        if target_sprite.object_type == "Ghost":

                            if self.pacman.PowerUp:

                                notOnEatenState = target_sprite.currentState != target_sprite.stateCache.EatenState()
                                if notOnEatenState:
                                    target_sprite.currentState.SwitchState(target_sprite.stateCache.EatenState())

                            else:
                                pass
                                #self.pacmanEaten = True
                                #self.pacman.eaten = True


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
                    self.gate = Tile(Sprites["Gate"], (x, y), [self.visible_sprites,self.collision_sprites])
                    print(x,y)

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

        self.pacman = Pacman(Sprites["Pacman"], (300, 360), [self.visible_sprites, self.pacman_Sprite], self.collision_sprites, self.nodes_sprites, self.portal_sprite,self)

        self.blinky = Blinky(Sprites["Blinky"], self.blinky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)
        self.pinky = Pinky(Sprites["Pinky"], self.pinky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)
        self.inky = Inky(Sprites["Inky"], self.inky_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self.blinky,self)
        self.clyde = Clyde(Sprites["Clyde"], self.clyde_pos, [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)


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


    def PlayGame(self):
        self.visible_sprites.draw(self.screen)

        self.PacmanCollisionLogic()

        if self.pinky.bounceCount >= self.pinky.homeDuration:
            self.gate.remove(self.collision_sprites)


        self.blinky.update()
        self.pinky.update()
        self.inky.update()
        self.clyde.update()


        self.pacman.update()

    def TitleScreen(self):
        mouse_pos = pg.mouse.get_pos()
        
        title = self.screen.blit(self.title, (110, 60))
        play_button = self.screen.blit(self.play, (185, 170))
        
        if play_button.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.startLevel = True



    def run(self):

        if self.startLevel:
            self.PlayGame()
        else:
            self.TitleScreen()







