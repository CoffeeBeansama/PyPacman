import pygame as pg
from pygame import mixer
from tile import Tile
from settings import *
from Pacman import Pacman
from node import *
from pellet import *
from ghost import *
from portal import Portal
from Sounds import *
class Level:

    def __init__(self,main):

        self.main = main
        self.screen = pg.display.get_surface()

        self.eatable_sprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()

        self.portal_sprite = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()
        self.nodes_sprites = pg.sprite.Group()
        self.pacman_Sprite = pg.sprite.Group()

        self.startLevel = False
        self.pacmanEaten = False
        self.displaySettings = False
        self.showTargetTile = False
        self.ghostNumber = 4

        self.score = 0
        self.highscore = 0

        self.textColor = (255, 255, 255)

        self.mainFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 40)
        self.controlFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 20)
        self.scoreFont = pg.font.Font("Font/NamcoRegular-lgzd.ttf", 12)

        self.importUISprites()

        self.pelletsEaten = []
        self.ghosts = []

        self.GhostchaseMode = pg.USEREVENT
        self.StartGame = pg.USEREVENT
        self.PowerPelletEaten = pg.USEREVENT

        PlayBGM("Menu")
        self.createMap()


    def PacmanCollisionLogic(self):
        if self.pacman_Sprite:
            for pacman in self.pacman_Sprite:
                collisionSprite = pg.sprite.spritecollide(pacman, self.eatable_sprites, False)
                if collisionSprite:
                    for target_sprite in collisionSprite:
                        if target_sprite.object_type == "pellet":
                            self.ObjectEaten("Pellet",target_sprite)
                        if target_sprite.object_type == "PowerPellet":
                            self.ObjectEaten("PowerPellet",target_sprite)
                        if target_sprite.object_type == "Ghost":
                            self.ObjectEaten("Ghost",target_sprite)

    def importUISprites(self):
        self.title = pg.transform.scale(pg.image.load(Sprites["Title"]), (350, 80)).convert_alpha()
        self.play = pg.transform.scale(pg.image.load(Sprites["Play Button"]), (200, 65)).convert_alpha()
        self.settings = pg.transform.scale(pg.image.load(Sprites["Settings Button"]), (100, 60)).convert_alpha()
        self.exit = pg.transform.scale(pg.image.load(Sprites["Exit Button"]), (140, 60)).convert_alpha()
        self.path = pg.transform.scale(pg.image.load(Sprites["Path Button"]), (200, 65)).convert_alpha()
        self.yes = pg.transform.scale(pg.image.load(Sprites["Yes Button"]), (60, 60)).convert_alpha()
        self.no = pg.transform.scale(pg.image.load(Sprites["No Button"]), (60, 60)).convert_alpha()
        self.back = pg.transform.scale(pg.image.load(Sprites["Back Button"]), (140, 65)).convert_alpha()
        self.sadFace = pg.transform.scale(pg.image.load(Sprites["GameOver"]), (200, 140)).convert_alpha()
        self.audio = pg.transform.scale(pg.image.load(Sprites["Audio Button"]), (160, 65)).convert_alpha()
        self.controls =  pg.transform.scale(pg.image.load(Sprites["Controls"]), (200, 140)).convert_alpha()

    def drawText(self,text,font,color,pos):
        text_image = font.render(text,True,color)
        self.screen.blit(text_image,pos)

    def createMap(self):
        for row_index,row in enumerate(map):
            for column_index,column in enumerate(row):

                x = column_index * tilesize
                y = row_index * tilesize

                if column == "*":
                    self.smallPellet = Smol_pellet(pelletSprites["SmallPellet"], (x,y), [self.visible_sprites, self.eatable_sprites], "pellet")

                if column == "PP":
                    PowerPellet(pelletSprites["PowerPellet"], (x, y), [self.visible_sprites, self.eatable_sprites], "PowerPellet")

                if column == "W":
                    self.walls = Tile(Sprites["Wall"], (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "E":
                    self.Exit1Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])
                    self.Exit2Tile = Tile(Sprites["Blank"], (x, y), [self.visible_sprites])

                if column == "G":
                    self.gate = Tile(Sprites["Gate"], (x, y), [self.visible_sprites,self.collision_sprites])

                if column == "N" or column == "B":
                    self.node = Node(Sprites["Blank"], (x, y), [self.visible_sprites, self.nodes_sprites])
                    smallPellet = Smol_pellet(pelletSprites["SmallPellet"], (x, y), [self.visible_sprites, self.eatable_sprites], "pellet")
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

        self.pacman = Pacman(Sprites["Pacman"],[self.visible_sprites, self.pacman_Sprite], self.collision_sprites, self.nodes_sprites, self.portal_sprite,self)

        self.blinky = Blinky(ghostSprites["Blinky"], [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)
        self.pinky = Pinky(ghostSprites["Pinky"], [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)
        self.inky = Inky(ghostSprites["Inky"], [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self.blinky,self)
        self.clyde = Clyde(ghostSprites["Clyde"], [self.visible_sprites, self.eatable_sprites], self.collision_sprites, self.nodes_sprites, self.node, "Ghost", self.pacman, self.portal_sprite,self)

        self.ghosts.extend([self.blinky,self.pinky,self.inky,self.clyde])

    def ObjectEaten(self, object,type):

        match object:
            case "Pellet":
                PlaySound("Pellet")
                self.score += 10
                type.Eaten([self.visible_sprites, self.eatable_sprites])
                self.pelletsEaten.append(type)

            case "PowerPellet":
                self.score += 50
                PlaySound("PowerPellet")
                pg.time.set_timer(self.PowerPelletEaten, 10000)
                type.Eaten(self.pacman, [self.visible_sprites, self.eatable_sprites])
                self.pelletsEaten.append(type)

            case "Ghost":
                self.pacman.GhostCollide(type)


    def DisablePowerUp(self):
        self.pacman.PowerUp = False
        StopPowerPelletSfx()

        for ghosts in self.ghosts:
            ghosts.eaten = False

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

    def OpenTheGates(self):
        if self.pinky.bounceCount >= self.pinky.homeDuration:
            self.gate.remove(self.collision_sprites)

    def PlayGame(self):
        self.visible_sprites.draw(self.screen)
        self.GetHighScore()
        self.PacmanCollisionLogic()
        self.OpenTheGates()
        self.blinky.update()
        self.pinky.update()
        self.inky.update()
        self.clyde.update()
        self.pacman.update()
        self.DrawScores()

    def GetHighScore(self):
        currentScore = self.score
        if currentScore >= self.highscore:
            self.highscore = currentScore

    def DrawScores(self):
        self.drawText(f"top score: {self.highscore}", self.scoreFont, self.textColor, (100, 3))
        self.drawText(f"score: {self.score}", self.scoreFont, self.textColor, (350, 3))

    def TitleScreen(self):
        mouse_pos = pg.mouse.get_pos()
        if not self.startLevel:
            title = self.drawText("pacman", self.mainFont, self.textColor, (120, 60))
            play_button = self.screen.blit(self.play, (180, 170))
            settings_button = self.screen.blit(self.settings ,(232, 250))
            exit_button = self.screen.blit(self.exit, (212, 320))

            if play_button.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    PlayBGM("Level")
                    self.startLevel = True
                    pg.time.set_timer(self.GhostchaseMode, 17000)

            elif exit_button.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    self.main.GameRunning = False

            elif settings_button.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    self.displaySettings = True

    def SettingsScreen(self):
        mouse_pos = pg.mouse.get_pos()
        ghostPath = self.screen.blit(self.path, (100, 170))
        yesBtn = self.screen.blit(self.yes, (310, 170))
        noBtn = self.screen.blit(self.no, (380, 170))
        backBtn = self.screen.blit(self.back ,(100, 310))
        audio = self.screen.blit(self.audio,(100, 240))
        self.drawText("controls",self.controlFont,self.textColor,(80, 520))
        contol = self.screen.blit(self.controls, (320, 460))

        if yesBtn.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
              self.showTargetTile = True

        if backBtn.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
              self.displaySettings = False

    def GameOverScreen(self):
        mouse_pos = pg.mouse.get_pos()
        if self.GameOver():

            self.drawText("game over", self.mainFont, self.textColor, (65, 60))
            play_button = self.screen.blit(self.play, (180, 170))
            exit_button = self.screen.blit(self.exit, (212,250 ))
            sadface = self.screen.blit(self.sadFace, (180, 320))

            if play_button.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    PlayBGM("Level")
                    self.ResetGame()
                    self.startLevel = True
                    pg.time.set_timer(self.GhostchaseMode, 17000)

            elif exit_button.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    self.main.GameRunning = False
    def ResetPellets(self):
        for pellets in self.pelletsEaten:
            pellets.add(self.visible_sprites,self.eatable_sprites)

        self.pelletsEaten.clear()


    def ResetGhosts(self):
        for ghosts in self.ghosts:
            ghosts.ResetState()

            #Resets the Drawing of Layers
            ghosts.remove(self.visible_sprites)
            ghosts.add(self.visible_sprites)

    def ResetGame(self):
        self.score = 0
        self.pacmanEaten = False
        self.ResetPellets()
        self.ResetGhosts()
        self.pacman.ResetState()
        self.gate.add(self.collision_sprites)



    def run(self):

        if self.GameOver():
            self.GameOverScreen()
        else:
            if self.displaySettings:
                self.SettingsScreen()
            else:

                self.TitleScreen()

            if self.startLevel:
                self.PlayGame()












