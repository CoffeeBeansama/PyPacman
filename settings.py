import pygame as pg
from pygame import mixer


WIDTH,HEIGHT = (580,650)

directions = ["Horizontal","Vertical"]
direction_axis = [-1,1]


Sprites = {"Blank" : "Sprites/Blank.png", "Wall" : "Sprites/Wall.png", "SmallPellet": "Sprites/smol pellet.png",
            "PowerPellet": "Sprites/big pellet.png", "Node" : "Sprites/node.png","Pacman" : "Sprites/Pacman.png",
            "Blinky": "Sprites/Blinky.png", "Pinky": "Sprites/Pinky.png", "Inky" : "Sprites/Inky.png",
            "Clyde" : "Sprites/Clyde.png", "Gate" : "Sprites/gate.png", "Title": "Sprites/title.png",
            "Play Button" : "Sprites/PlayButton.png","GameOver": "Sprites/GameOver.png","Exit Button" : "Sprites/ExitButton.png",
           "Settings Button" : "Sprites/SettingsButton.png","Path Button" : "Sprites/GhostPath.png", "Yes Button" : "Sprites/Yes Button.png",
           "No Button": "Sprites/No Button.png", "Back Button" : "Sprites/Back Button.png","Audio Button": "Sprites/Audio Button.png"


            }

Sounds = { "Pellet1" : "Sounds/1.mp3", "Pellet2" : "Sounds/2.mp3","PowerPellet": "Sounds/Power Pellet.mp3",
            "GhostEaten": "Sounds/Ghost Eat.wav","BGM" : "Sounds/Siren.mp3","PacmanDeath" : "Sounds/Death.wav"
           ,"MainMenu" : "Sounds/Menu.wav"
}

ghost_speed = 0.9
ghost_EatenSpeed = 1.6
pacman_Speed = 1.3

tilesize = 20
FPS = 60

# * => small pellet, b => big pellet, P => Pacman, W => Wall, G1 => Blinky, G2 => Pinky, G3 => Inky, G4 => Clyde, E=> Exit

map = [
["B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","B"],
["B","W","N","*","*","*","*","N","*","*","*","*","*","N","W","N","*","*","*","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","PP","W","W","W","W","*","W","W","W","W","W","*","W","*","W","W","W","W","W","*","W","W","W","W","PP","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","N","*","*","N","*","*","N","*","N","*","*","N","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","*","W","B"],
["B","W","*","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","N","*","*","N","*","*","N","W","N","*","*","N","*","*","N","*","*","*","*","N","W","B"],
["B","W","W","W","W","W","W","*","W","W","W","W","W"," ","W"," ","W","W","W","W","W","*","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","W","*","W","W","W","W","W"," ","W"," ","W","W","W","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","N"," "," ","N","E","N"," "," ","N","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W"," ","W","W","W","G","W","W","W"," ","W","W","*","W","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","*","W","W"," ","W","B","B","B","B","B","W"," ","W","W","*","W","W","W","W","W","W","B"],
["B","PT"," "," "," "," "," ","N","*","*","N","W","B","B","B","B","B","W","N","*","*","N"," "," "," "," "," ","PT","B"],
["B","W","W","W","W","W","W","*","W","W"," ","W","B","B","B","B","B","W"," ","W","W","*","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","W","*","W","W"," ","W","W","W","W","W","W","W"," ","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","N"," "," "," "," "," "," "," ","N","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","B"],
["B","W","N","*","*","*","*","N","*","*","N","*","*","N","W","N","*","*","N","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","PP","W","W","W","W","*","W","W","W","W","W","*","W","*","W","W","W","W","W","*","W","W","W","W","PP","W","B"],
["B","W","N","*","N","*","*","N","*","*","N","*","*","N","*","N","*","*","N","*","*","N","*","*","N","*","N","W","B"],
["B","W","W","W","*","W","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","W","*","W","W","W","B"],
["B","W","W","W","*","W","W","*","W","W","*","W","W","W","W","W","W","W","*","W","W","*","W","W","*","W","W","W","B"],
["B","W","N","*","N","*","*","N","W","W","N","*","*","N","W","N","*","*","N","W","W","N","*","*","N","*","N","W","B"],
["B","W","*","W","W","W","W","W","W","W","W","W","W","*","W","*","W","W","W","W","W","W","W","W","W","W","*","W","B"],
["B","W","*","W","W","W","W","W","W","W","W","W","W","*","W","*","W","W","W","W","W","W","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","*","*","*","*","*","*","N","*","N","*","*","*","*","*","*","*","*","*","*","N","W","B"],
["B","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"],
]



