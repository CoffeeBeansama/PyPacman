import pygame as pg
from support import loadSprite
from settings import Sprites

class MainMenu:
    def __init__(self):

        self.displaySettings = False
        self.importUISprites()

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

    def titleScreen(self):
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

    def update(self):
        self.titleScreen()
