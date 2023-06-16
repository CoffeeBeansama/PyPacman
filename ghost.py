from abc import ABC, abstractmethod
import pygame as pg
from enum import Enum


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
        self.main.rect.center = self.main.gatePos

    def UpdateState(self):
        self.CheckSwitchState()

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


class Blinky(pg.sprite.Sprite):

    def __init__(self, image, pos, group, object_type):
        super().__init__(group)

        self.homeDuration = 1000
        self.startingPos = (290, 290)
        self.gatePos = (290,250)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()



    def update(self):
        self.currentState.UpdateState()


class Pinky(pg.sprite.Sprite):

    def __init__(self, image, pos, group, object_type):
        super().__init__(group)


        self.homeDuration = 3000
        self.startingPos = (310, 290)
        self.gatePos = (310, 250)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()


class Inky(pg.sprite.Sprite):

    def __init__(self, image, pos, group, object_type):
        super().__init__(group)

        self.homeDuration = 5000
        self.startingPos = (290, 310)
        self.gatePos = (290, 250)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()


class Clyde(pg.sprite.Sprite):

    def __init__(self, image, pos, group, object_type):
        super().__init__(group)

        self.homeDuration = 7000
        self.startingPos = (310, 310)
        self.gatePos = (310, 250)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.HomeState()
        self.currentState.EnterState()

    def update(self):
        self.currentState.UpdateState()
