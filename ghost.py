import random
import sys
from abc import ABC, abstractmethod
import pygame as pg
from entity import Entity
from enum import Enum
from settings import *


class States(Enum):
    Home = 1
    Scatter = 2
    Chase = 3
    Frightened = 4


class StateCache:
    def __init__(self, main):
        self.main = main

        self.states = {
            "Home" : HomeState(self,self.main),
            "Scatter" : ScatterState(self,self.main),
            "Chase" : ChaseState(self,self.main),
            "Frightened": FrightenedState(self,self.main)
        }

    def HomeState(self):
        return self.states["Home"]
    def ScatterState(self):
        return self.states["Scatter"]
    def ChaseState(self):
        return self.states["Chase"]
    def FrightenedState(self):
        return self.states["Frightened"]

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
        self.main.rect.center = self.main.startingPos
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
            randomDirection = random.randrange(len(self.main.node_object.availableDirections))

            x = self.main.node_object.availableDirections[randomDirection][0]
            y = self.main.node_object.availableDirections[randomDirection][1]

            self.main.direction.x = x
            self.main.direction.y = y

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

            for directions in self.main.node_object.availableDirections:

                newPosition = pg.math.Vector2(self.main.rect.center + pg.math.Vector2(directions[0], directions[1]))
                distance = (self.main.player.rect.center - newPosition).magnitude_squared()

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
            distance = (self.main.player.rect.center - newPosition).magnitude_squared()

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


class Blinky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.homeDuration = 1000
        self.ScatterDuration = 15000
        self.startingPos = (290, 290)
        self.gatePos = (290,250)
        self.portals = portal_sprite
        self.player = player
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object



        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()



    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()


class Pinky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)


        self.homeDuration = 5000
        self.ScatterDuration = 16000
        self.startingPos = (310, 290)
        self.gatePos = (310, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.player = player
        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()


class Inky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.homeDuration = 9000
        self.ScatterDuration = 17000
        self.startingPos = (290, 310)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object
        self.player = player

        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()


class Clyde(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite):
        super().__init__(group)

        self.homeDuration = 12000
        self.ScatterDuration = 18000
        self.startingPos = (310, 310)
        self.gatePos = (310, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object
        self.player = player

        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
