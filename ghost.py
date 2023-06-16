import random
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

    def SetRandomDirection(self,main):
        if main.NodeCollided():
            main.savePreviousDirection(main.direction)
            if self.RandomValue()[0] == "Horizontal":

                main.HorizontalMovement(main.direction,self.RandomValue()[1])
            elif self.RandomValue()[0] == "Vertical":
                main.VerticalMovement(main.direction,self.RandomValue()[1])


    def UpdateState(self):
        self.CheckSwitchState()
        self.SetRandomDirection(self.main)
        self.main.movement(ghost_speed)

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass

class ChaseState(BaseState):

    def EnterState(self):
        pass

    def UpdateState(self):
        self.CheckSwitchState()

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class FrightenedState(BaseState):

    def EnterState(self):
        pass

    def UpdateState(self):
        self.CheckSwitchState()

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class Blinky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,object_type):
        super().__init__(group)

        self.homeDuration = 1000
        self.startingPos = (290, 290)
        self.gatePos = (290,250)

        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
    

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()



    def update(self):
        self.currentState.UpdateState()


class Pinky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,object_type):
        super().__init__(group)


        self.homeDuration = 5000
        self.startingPos = (310, 290)
        self.gatePos = (310, 250)

        self.collision_sprite = collidableSprite
        self.nodes = node_sprite

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()


class Inky(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,object_type):
        super().__init__(group)

        self.homeDuration = 9000
        self.startingPos = (290, 310)
        self.gatePos = (290, 250)

        self.collision_sprite = collidableSprite
        self.nodes = node_sprite

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()


class Clyde(Entity):

    def __init__(self, image, pos, group,collidableSprite,node_sprite,object_type):
        super().__init__(group)

        self.homeDuration = 12000
        self.startingPos = (310, 310)
        self.gatePos = (310, 250)

        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.direction = pg.math.Vector2()
        self.previous_direction = pg.math.Vector2()

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()
