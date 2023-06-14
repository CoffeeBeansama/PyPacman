import pygame as pg

WIDTH,HEIGHT = (600,650)

blank = "Sprites/Blank.png"
wall = "Sprites/Wall.png"
smolpellet = "Sprites/smol pellet.png"
bigpellet = "Sprites/big pellet.png"
pacman = "Sprites/Pacman.png"
node = "Sprites/node.png"

speed = 1

tilesize = 20
FPS = 60

map = [
["B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","B"],
["B","W","N","*","*","*","*","N","*","*","*","*","*","N","W","W","N","*","*","*","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","b","W","W","W","W","*","W","W","W","W","W","*","W","W","*","W","W","W","W","W","*","W","W","W","W","b","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","N","*","*","N","*","*","N","*","*","N","*","*","N","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","*","W","B"],
["B","W","*","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","N","W","W","N","*","*","N","W","W","N","*","*","N","W","W","N","*","*","*","*","N","W","B"],
["B","W","W","W","W","W","W","*","W","W","W","W","W"," ","W","W"," ","W","W","W","W","W","*","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","W","*","W","W","W","W","W"," ","W","W"," ","W","W","W","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","N"," "," ","N"," "," ","N"," "," ","N","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W"," ","W","W","W","W","W","W","W","W"," ","W","W","*","W","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","*","W","W"," ","W","B","B","B","B","B","B","W"," ","W","W","*","W","W","W","W","W","W","B"],
["B"," "," "," "," "," "," ","N","*"," ","N","W","B","B","B","B","B","B","W","N"," ","*","N"," "," "," "," "," "," ","B"],
["B","W","W","W","W","W","W","*","W","W"," ","W","B","B","B","B","B","B","W"," ","W","W","*","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","W","*","W","W"," ","W","W","W","W","W","W","W","W"," ","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","N"," "," "," "," "," "," "," "," ","N","W","W","*","W","B","B","B","B","B","B"],
["B","B","B","B","B","B","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","B","B","B","B","B","B"],
["B","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","B"],
["B","W","N","*","*","*","*","N","*","*","N","*","*","N","W","W","N","*","*","N","*","*","N","*","*","*","*","N","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","*","W","W","W","W","*","W","W","W","W","W","*","W","W","*","W","W","W","W","W","*","W","W","W","W","*","W","B"],
["B","W","N","*","N","W","W","N","*","*","N","*","*","N","*","*","N","*","*","N","*","*","N","W","W","N","*","N","W","B"],
["B","W","W","W","*","W","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","W","*","W","W","W","B"],
["B","W","W","W","*","W","W","*","W","W","*","W","W","W","W","W","W","W","W","*","W","W","*","W","W","*","W","W","W","B"],
["B","W","N","*","N","*","*","N","W","W","N","*","*","N","W","W","N","*","*","N","W","W","N","*","*","N","*","N","W","B"],
["B","W","*","W","W","W","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","W","W","W","*","W","B"],
["B","W","*","W","W","W","W","W","W","W","W","W","W","*","W","W","*","W","W","W","W","W","W","W","W","W","W","*","W","B"],
["B","W","N","*","*","*","*","*","*","*","*","*","*","N","*","*","N","*","*","*","*","*","*","*","*","*","*","N","W","B"],
["B","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","B"],
["B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"],
]
