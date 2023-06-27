import random
import sys
import pygame as pg
from settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        self.screen = pg.display.get_surface()
        self.direction = pg.math.Vector2()
        self.next_direction = pg.math.Vector2()
        self.previous_direction = pg.math.Vector2()

        self.Direction = {"Up": (0,-1), "Down": (0,1),
                          "Left": (-1,0), "Right": (1,0)
                          }

        self.wallCollided = False



    def movement(self,speed):

        self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.checkCollisions("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkCollisions("Vertical")
        self.rect.center = self.hitbox.center

    def HorizontalMovement(self,direction,value):
        direction.y = 0
        direction.x = value
    def VerticalMovement(self,direction,value):
        direction.y = value
        direction.x = 0



    def savePreviousDirection(self, direction):
        self.previous_direction.x = direction.x
        self.previous_direction.y = direction.y

    def setNextDirection(self, nextDirection):
        self.next_directioyy = nextDirection

    def NodeCollided(self):

        for sprite in self.nodes:
            if sprite.hitbox.center == self.hitbox.center:
                self.node_object = sprite

                return True

        return False




    def CheckPortalCollision(self):
        for sprite in self.portals:
            if sprite.hitbox.center == self.hitbox.center:
                self.hitbox.center = sprite.transport_pos




    def setDirection(self,direction):
        if self.NodeCollided():
            self.direction = direction


    def checkCollisions(self,direction):

        if direction == "Horizontal":
            for sprite in self.collision_sprite:
                if sprite.hitbox.colliderect(self.hitbox):

                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left


                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "Vertical":
            for sprite in self.collision_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom


