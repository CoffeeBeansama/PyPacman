import pygame as pg
from entity import Entity
from settings import *

class Pacman(Entity):
    def __init__(self,image,pos,sprite_group,collidable_sprite,node_sprite):
        super().__init__(sprite_group)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.nodes = node_sprite
        self.hitbox = self.rect.inflate(0,0)
        self.collision_sprite = collidable_sprite

        self.current_direction = "Left"
        self.next_direction.x = -1
        self.next_direction.y  = 0

        self.HorizontalMovement(self.direction, -1)


    def HorizontalMovement(self,direction,value):
        direction.y = 0
        direction.x = value
    def VerticalMovement(self,direction,value):
        direction.y = value
        direction.x = 0

    def savePreviousDirection(self,direction):
        self.previous_direction.x = direction.x
        self.previous_direction.y = direction.y



    def setNextDirection(self,value1,value2):
        self.next_direction.x = value1
        self.next_direction.y = value2

    def setDirection(self,direction):



        if self.current_direction == "Up":
            self.savePreviousDirection(direction)

            if self.previous_direction.y == 1:
                self.VerticalMovement(direction, -1)
            else:
                if not self.NodeCollided():
                    direction.x = self.previous_direction.x
                    direction.y = self.previous_direction.y

                else:
                    self.VerticalMovement(direction, -1)
                    self.setNextDirection(0, -1)

        elif self.current_direction == "Down":
            self.savePreviousDirection(direction)
            if self.previous_direction.y == -1:
                self.VerticalMovement(direction, 1)
            else:
                if not self.NodeCollided():
                    direction.x = self.previous_direction.x
                    direction.y = self.previous_direction.y

                else:
                    self.VerticalMovement(direction, 1)
                    self.setNextDirection(0, 1)

        elif self.current_direction == "Left":
            self.savePreviousDirection(direction)
            if self.previous_direction.x == 1:
                self.HorizontalMovement(direction, -1)
            else:

                if not self.NodeCollided():
                    direction.x = self.previous_direction.x
                    direction.y = self.previous_direction.y


                else:
                    self.HorizontalMovement(direction, -1)
                    self.setNextDirection(-1, 0)

        elif self.current_direction == "Right":

            self.savePreviousDirection(direction)
            if self.previous_direction.x == -1:
                self.HorizontalMovement(direction, 1)
            else:
                if not self.NodeCollided():

                    direction.x = self.previous_direction.x
                    direction.y = self.previous_direction.y

                else:
                    self.HorizontalMovement(direction, 1)
                    self.setNextDirection(1, 0)



    def get_inputs(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_w]: # Up
            self.current_direction = "Up"

        elif keys[pg.K_s]: # Down
            self.current_direction = "Down"

        if keys[pg.K_a]: # Left
            self.current_direction = "Left"

        elif keys[pg.K_d]: # Right
            self.current_direction = "Right"






    def update(self):
        print(self.current_direction)
        self.get_inputs()
        self.setDirection(self.direction)
        self.movement(speed)


