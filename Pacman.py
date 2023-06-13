import pygame as pg
from entity import Entity
from settings import *

class Pacman(Entity):
    def __init__(self,image,pos,sprite_group,collidable_sprite,node_sprite):
        super().__init__(sprite_group)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, 0)
        self.collision_sprite = collidable_sprite
        self.nodes = node_sprite

        self.HorizontalMovement(self.direction, -1)


    def HorizontalMovement(self,direction,value):
        direction.y = 0
        direction.x = value
    def VerticalMovement(self,direction,value):
        direction.y = value
        direction.x = 0

    def setNextDirection(self,value1,value2):
        self.next_direction.x = value1
        self.next_direction.y = value2
    def get_inputs(self,direction):

        keys = pg.key.get_pressed()

        if not self.NodeCollided():

            if keys[pg.K_w]: # Up
                self.setNextDirection(0,-1)

            elif keys[pg.K_s]: # Down
                self.setNextDirection(0,1)

            if keys[pg.K_a]: # Left
                self.setNextDirection(-1, 0)

            elif keys[pg.K_d]: # Right
                self.setNextDirection(1,0)

        else:

               direction.x = self.next_direction.x
               direction.y = self.next_direction.y









    def update(self):

        print(self.NodeCollided())
        self.get_inputs(self.direction)
        self.movement(speed)


