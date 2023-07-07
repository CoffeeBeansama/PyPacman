import random
import pygame as pg
from pygame import mixer
from settings import *

pg.init()

pelletSound1 = mixer.Sound(Sounds["Pellet1"])
pelletSound2 = mixer.Sound(Sounds["Pellet2"])
PowerPelletSound = mixer.Sound(Sounds["PowerPellet"])
PacmanDyingSound = mixer.Sound(Sounds["PacmanDeath"])


def PlayBGM(bgm):
    if bgm == "Level":
        mixer.music.load(Sounds["BGM"])

    elif bgm == "Menu":
        mixer.music.load(Sounds["MainMenu"])

    mixer.music.play(-1)
    mixer.music.set_volume(0.08)



def PlaySound(sound):
    if sound == "Pellet":
        sfx = [pelletSound1, pelletSound2]
        pg.mixer.Sound.play(random.choice(sfx))

    elif sound == "PowerPellet":
        mixer.music.stop()
        pg.mixer.Sound.play(PowerPelletSound)

    elif sound == "PacmanDying":
        pg.mixer.Sound.play(PacmanDyingSound)


def StopPowerPelletSfx():
    mixer.music.load(Sounds["BGM"])
    mixer.music.play(-1)
    pg.mixer.Sound.stop(PowerPelletSound)

