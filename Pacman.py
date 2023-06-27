import pygame as pg
from entity import Entity
from settings import *

class Pacman(Entity):
    def __init__(self,image,pos,sprite_group,collidable_sprite,node_sprite,portal_sprite):
        super().__init__(sprite_group)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.nodes = node_sprite
        self.hitbox = self.rect.inflate(0,0)
        self.collision_sprite = collidable_sprite

        self.PowerUp = False
        self.portals = portal_sprite

        self.current_direction = "Left"
        self.next_direction.x = -1
        self.next_direction.y = 0

        self.HorizontalMovement(self.direction, -1)


    def setDirection(self,direction):

        if self.current_direction == "Up":
            self.savePreviousDirection(direction)

            if self.previous_direction.y == 1:
                direction.y = direction.y * -1
            else:
                if self.NodeCollided():
                    self.VerticalMovement(direction, -1)
                    self.setNextDirection(self.Direction["Up"])

        elif self.current_direction == "Down":
            self.savePreviousDirection(direction)
            if self.previous_direction.y == -1:
                direction.y = direction.y * -1
            else:
                if self.NodeCollided():
                    self.VerticalMovement(direction, 1)
                    self.setNextDirection(self.Direction["Down"])

        elif self.current_direction == "Left":
            self.savePreviousDirection(direction)
            if self.previous_direction.x == 1:
                direction.x = direction.x * -1
            else:

                if self.NodeCollided():
                    self.HorizontalMovement(direction, -1)
                    self.setNextDirection(self.Direction["Left"])

        elif self.current_direction == "Right":

            self.savePreviousDirection(direction)
            if self.previous_direction.x == -1:
                direction.x = direction.x * -1
            else:
                if self.NodeCollided():
                    self.HorizontalMovement(direction, 1)


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
        self.get_inputs()
        self.CheckPortalCollision()
        self.setDirection(self.direction)
        self.movement(pacman_Speed)


