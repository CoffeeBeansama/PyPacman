import random
import sys
import pygame as pg
from settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        self.direction = pg.math.Vector2()
        self.next_direction = pg.math.Vector2()
        self.previous_direction = pg.math.Vector2()



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

    def setNextDirection(self, value1, value2):
        self.next_direction.x = value1
        self.next_direction.y = value2

    def NodeCollided(self):

        for sprite in self.nodes:
            if sprite.hitbox.center == self.hitbox.center:
                self.node_object = sprite

                return True

        return False




    def ScatterDirection(self,direction):

        if self.NodeCollided():

            randomDirection = random.randrange(len(self.node_object.availableDirections))
            print(self.node_object.rect.x)
            print(self.node_object.rect.y)

            x = self.node_object.availableDirections[randomDirection][0]
            y = self.node_object.availableDirections[randomDirection][1]
            print(f"x is : {x}")
            print(f"y is : {y}")
            direction.x = x
            direction.y = y

    def ChaseDirection(self):

            direction = pg.math.Vector2()
            minDistance = sys.float_info.max

            for directions in self.node_object.availableDirections:

                newPosition = pg.math.Vector2(self.rect.center + pg.math.Vector2(directions[0],directions[1]))
                distance = (self.player.rect.center - newPosition).magnitude_squared()

                if distance < minDistance:

                    direction.x = directions[0]

                    direction.y = directions[1]


                    minDistance = distance


            self.setDirection(direction)







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


