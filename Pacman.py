import pygame as pg
from entity import Entity
from settings import *

class Pacman(Entity):
    def __init__(self,image,pos,sprite_group,collidable_sprite):
        super().__init__(sprite_group)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, 0)
        self.collision_sprite = collidable_sprite



    def get_inputs(self,direction):

        keys = pg.key.get_pressed()
        if keys[pg.K_w]: # Up
            direction.y = -1
        elif keys[pg.K_s]: # Down
            direction.y = 1
        elif keys[pg.K_a]: # Left
            direction.x = -1
        elif keys[pg.K_d]: # Right
            direction.x = 1




    def update(self):
        self.get_inputs(self.direction)
        self.movement(speed)
        self.checkCollisions(self.direction)