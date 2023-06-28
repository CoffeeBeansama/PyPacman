import math
import random
import sys
from abc import ABC, abstractmethod
import pygame as pg
from entity import Entity
from enum import Enum
from settings import *
from support import import_folder


class States(Enum):
    Home = 1
    Scatter = 2
    Chase = 3
    Frightened = 4
    Eaten = 5


class StateCache:
    def __init__(self, main):
        self.main = main

        self.states = {
            "Home" : HomeState(self,self.main),
            "Scatter" : ScatterState(self,self.main),
            "Chase" : ChaseState(self,self.main),
            "Frightened": FrightenedState(self,self.main),
            "Eaten" : EatenState(self,self.main)
        }

    def HomeState(self):
        return self.states["Home"]
    def ScatterState(self):
        return self.states["Scatter"]
    def ChaseState(self):
        return self.states["Chase"]
    def FrightenedState(self):
        return self.states["Frightened"]
    def EatenState(self):
        return self.states["Eaten"]

class BaseState(ABC):


    @abstractmethod
    def EnterState(self):
        pass

    @abstractmethod
    def UpdateState(self):
        pass

    @abstractmethod
    def CheckSwitchState(self):
        pass
    @abstractmethod
    def ExitState(self):
        pass

    def __init__(self,stateCache,main):
        self.stateCache = stateCache
        self.main = main
        self.startTick = pg.time.get_ticks()
        self.HomeDuration = 0

    def SwitchState(self,newState):
        self.ExitState()
        newState.EnterState()
        self.main.currentState = newState

    def RandomValue(self):
        direction = random.choice(directions)
        value = random.choice(direction_axis)
        return direction,value



class HomeState(BaseState):

    def EnterState(self):
        self.main.hitbox.center = self.main.startingPos
    def CheckSwitchState(self):

        currentTime = pg.time.get_ticks()

        if currentTime - 0 >= self.main.homeDuration:
            self.SwitchState(self.stateCache.ScatterState())


    def UpdateState(self):
        self.CheckSwitchState()



    def ExitState(self):
        pass


class ScatterState(BaseState):

    def EnterState(self):
        self.main.hitbox.center = self.main.gatePos

        self.main.HorizontalMovement(self.main.direction,self.RandomValue()[1])

    def UpdateState(self):
        self.CheckSwitchState()

        if self.main.NodeCollided():

            index = random.randrange(0,len(self.main.node_object.availableDirections))

            goingBack = self.main.node_object.availableDirections[index] == -self.main.direction

            if goingBack:

                index += 1
                if index >= len(self.main.node_object.availableDirections):
                    index = 0

                self.main.direction.x = self.main.node_object.availableDirections[index][0]
                self.main.direction.y = self.main.node_object.availableDirections[index][1]

        self.main.movement(ghost_speed)

    def CheckSwitchState(self):


        if self.main.player.PowerUp:
            self.SwitchState(self.stateCache.FrightenedState())

        currentTime = pg.time.get_ticks()

        if currentTime - 0 >= self.main.ScatterDuration:
            self.SwitchState(self.stateCache.ChaseState())


    def ExitState(self):
        pass

class ChaseState(BaseState):

    def EnterState(self):
        pass



    def UpdateState(self):

            self.CheckSwitchState()

            direction = pg.math.Vector2()
            minDistance = sys.float_info.max

            #for debugging
            #pg.draw.line(self.main.screen,self.main.color,(self.main.rect.centerx,self.main.rect.centery),(self.main.TargetTile()[0],self.main.TargetTile()[1]),5)

            for directions in self.main.node_object.availableDirections:

                newPosition = pg.math.Vector2(self.main.rect.center + pg.math.Vector2(directions[0], directions[1]))
                distance = (self.main.TargetTile() - newPosition).magnitude_squared()

                if distance < minDistance:
                    direction.x = directions[0]

                    direction.y = directions[1]

                    minDistance = distance

            self.main.setDirection(direction)
            self.main.movement(ghost_speed)


    def CheckSwitchState(self):
        if self.main.player.PowerUp:
            self.SwitchState(self.stateCache.FrightenedState())

    def ExitState(self):
        pass


class FrightenedState(BaseState):

    def EnterState(self):
        pass



    def UpdateState(self):

        self.CheckSwitchState()

        direction = pg.math.Vector2()
        MaxDistance = sys.float_info.min

        for directions in self.main.node_object.availableDirections:

            newPosition = pg.math.Vector2(self.main.rect.center + pg.math.Vector2(directions[0], directions[1]))
            distance = (self.main.gatePos - newPosition).magnitude_squared()

            if distance > MaxDistance:
                direction.x = directions[0]

                direction.y = directions[1]

                MaxDistance = distance

        self.main.setDirection(direction)
        self.main.movement(ghost_speed)

    def CheckSwitchState(self):
        if self.main.player.PowerUp == False:
            self.SwitchState(self.stateCache.ChaseState())


    def ExitState(self):
        pass

class EatenState(BaseState):

    def EnterState(self):
       pass



    def UpdateState(self):

        self.CheckSwitchState()

        direction = pg.math.Vector2()
        minDistance = sys.float_info.max

        for directions in self.main.node_object.availableDirections:

            newPosition = pg.math.Vector2(self.main.rect.center + pg.math.Vector2(directions[0], directions[1]))
            distance = ((self.main.gatePos[0],self.main.gatePos[1]) - newPosition).magnitude_squared()

            if distance < minDistance:

                direction.x = directions[0]
                direction.y = directions[1]

                minDistance = distance

        self.main.setDirection(direction)
        self.main.movement(ghost_EatenSpeed)



    def CheckSwitchState(self):

        if self.main.rect.x == self.main.gatePos[0]:

            self.SwitchState(self.stateCache.ScatterState())


    def ExitState(self):
        pass


class Ghosts(Entity):

    def importSprites(self):
        path = f"Sprites/Ghosts/Body/"

        self.animations = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                           f"{self.name}": [], "Frightened": []
                           }

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)



    def animate(self):
        animation = self.animations[self.name] if self.currentState != self.stateCache.FrightenedState() else self.animations["Frightened"]
        self.frame_index += self.animation_time

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
    def getSpriteDirection(self):
        if self.direction.y == -1:
            self.spriteDirection = "Up"
        elif self.direction.y == 1:
            self.spriteDirection = "Down"
        elif self.direction.x == -1:
            self.spriteDirection = "Left"
        elif self.direction.x == 1:
            self.spriteDirection = "Right"

class Blinky(Ghosts):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.name = "Blinky"

        self.homeDuration = 1000
        self.ScatterDuration = 15000
        self.startingPos = (280,300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.player = player
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object



        self.color = (255,0,0)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def TargetTile(self):
        return self.player.rect.center

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()


class Pinky(Ghosts):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.name = "Pinky"

        self.homeDuration = 5000
        self.ScatterDuration = 16000
        self.startingPos = (300,300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.color = (255, 80, 255)

        self.player = player
        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()


    def TargetTile(self):

        playerDirection = self.player.current_direction
        playerX = self.player.rect.centerx
        playerY = self.player.rect.centery


        if playerDirection == "Up":
            x = playerX
            y = playerY - 80
        elif playerDirection == "Down":
            x = playerX
            y = playerY + 80
        elif playerDirection == "Left":
            x = playerX - 80
            y = playerY
        elif playerDirection == "Right":
            x = playerX + 80
            y = playerY

        return (x,y)

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()


class Inky(Ghosts):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite,blinky):
        super().__init__(group)

        self.name = "Inky"

        self.homeDuration = 9000
        self.ScatterDuration = 17000
        self.startingPos = (280, 320)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.color = (224,255,255)
        self.player = player
        self.blinky = blinky
        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.importSprites()

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def TargetTile(self):

        playerDirection = self.player.current_direction
        playerX = self.player.rect.centerx
        playerY = self.player.rect.centery

        blinkyX = self.blinky.rect.centerx
        blinkyY = self.blinky.rect.centery

        if playerDirection == "Up":
            targetX = playerX
            targetY = (playerY - 40)
        elif playerDirection == "Down":
            targetX = playerX
            targetY = (playerY + 40)
        elif playerDirection == "Left":
            targetX = (playerX - 40)
            targetY = playerY
        elif playerDirection == "Right":
            targetX = (playerX + 40)
            targetY = playerY

        buffX = targetX - blinkyX
        buffY = targetY - blinkyY

        tilex = targetX - buffX
        tiley = targetY - buffY


        targetTileX = (tilex * math.cos(0) - tiley * math.sin(0)) + (buffX * 2)
        targetTileY = (tilex * math.sin(0) + tiley * math.cos(0)) + (buffY * 2)

        return targetTileX,targetTileY

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()


class Clyde(Ghosts):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.name = "Clyde"
        self.homeDuration = 12000
        self.ScatterDuration = 18000
        self.startingPos = (300, 320)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object
        self.player = player


        self.color =(255,190,190)

        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()
        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

        self.allowedDistanceToPacman = 160


    def TargetTile(self):
        x_hometile = 10
        y_hometile = 610

        currentPos = pg.math.Vector2(self.rect.center)
        playerPos = pg.math.Vector2(self.player.rect.center)

        distanceToPlayer = (playerPos - currentPos).magnitude()

        if distanceToPlayer <= self.allowedDistanceToPacman:

            return x_hometile,y_hometile

        else:

            return self.player.rect.center

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()

