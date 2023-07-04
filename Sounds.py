import pygame as pg
from pygame import mixer
from settings import *

pg.init()

pelletSoundIndex = 0
pelletSound1 = mixer.Sound(Sounds["Pellet1"])
pelletSound2 = mixer.Sound(Sounds["Pellet2"])
PowerPelletSound = mixer.Sound(Sounds["PowerPellet"])


def PlayBGM():
    mixer.music.load(Sounds["BGM"])
    mixer.music.play(-1)
    mixer.music.set_volume(0.08)


def PelletSfx(index):
    sfx = [pelletSound1, pelletSound2]
    index += 1

    if index >= len(sfx):
        index = 0
    pg.mixer.Sound.play(sfx[index])


def PowerPelletSfx():
    mixer.music.stop()
    pg.mixer.Sound.play(PowerPelletSound)

def StopPowerPelletSfx():
    mixer.music.load(Sounds["BGM"])
    mixer.music.play(-1)
    pg.mixer.Sound.stop(PowerPelletSound)

