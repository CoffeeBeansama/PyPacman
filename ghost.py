import math
import random
import sys
from abc import ABC, abstractmethod
import pygame as pg
from entity import Entity
from enum import Enum
from settings import *
from support import import_folder
from timer import Timer

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

    def homeState(self):
        return self.states["Home"]
    def scatterState(self):
        return self.states["Scatter"]
    def chaseState(self):
        return self.states["Chase"]
    def frightenedState(self):
        return self.states["Frightened"]
    def eatenState(self):
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
        self.main.VerticalMovement(self.main.direction,-1)


    def CheckSwitchState(self):
        if self.main.level.startLevel:
            if self.main.bounceCount >= self.main.homeDuration:
                if self.main.rect.y == self.main.startingPos[1]:
                    if self.main.hitbox.x < 280:
                        self.main.HorizontalMovement(self.main.direction, 1)
                    else:
                        self.main.HorizontalMovement(self.main.direction, -1)

                if self.main.hitbox.x == 280:
                    self.main.VerticalMovement(self.main.direction, -1)

                if self.main.hitbox.center == self.main.gatePos:
                    self.SwitchState(self.stateCache.scatterState())


    def HomeIdle(self):
        for sprite in self.main.collision_sprite:
            if sprite.rect.colliderect(self.main.rect):
                 if self.main.direction.y < 0:
                     self.main.bounceCount += 1
                     self.main.rect.top = sprite.rect.bottom
                     self.main.VerticalMovement(self.main.direction,1)
                 else:
                     self.main.bounceCount += 1
                     self.main.rect.bottom = sprite.rect.top
                     self.main.VerticalMovement(self.main.direction, -1)


        self.main.rect.center += self.main.direction * ghost_speed
        self.main.hitbox.x += self.main.direction.x * ghost_speed
        self.main.hitbox.y += self.main.direction.y * ghost_speed


    def UpdateState(self):
        self.CheckSwitchState()
        self.HomeIdle()
        self.main.rect.center = self.main.hitbox.center

    def ExitState(self):
        pass

class ScatterState(BaseState):

    def EnterState(self):
        self.main.hitbox.center = self.main.gatePos
        self.main.HorizontalMovement(self.main.direction,self.RandomValue()[1])
        if not self.scatterTimer.activated:
           self.scatterTimer.activate()

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
        if self.main.player.PowerUp and not self.main.eaten:
            self.SwitchState(self.stateCache.frightenedState())

        if self.main.chaseState:
            self.SwitchState(self.stateCache.chaseState())


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
            if self.main.level.showTargetTile:
                pg.draw.line(self.main.screen, self.main.color, (self.main.rect.centerx, self.main.rect.centery),(self.main.TargetTile()[0], self.main.TargetTile()[1]), 3)

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
        if self.main.player.PowerUp and not self.main.eaten:
            self.SwitchState(self.stateCache.frightenedState())

    def ExitState(self):
        self.main.chaseState = False


class FrightenedState(BaseState):

    def EnterState(self):
        self.main.eaten = False

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
            self.SwitchState(self.stateCache.chaseState())


    def ExitState(self):
        pass

class EatenState(BaseState):
    def EnterState(self):
       self.healed = False
       self.main.eaten = True
       pg.mixer.Sound.play(self.main.GhostEatenSound)
       self.main.remove(self.main.level.visible_sprites)

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
        speed = ghost_EatenSpeed if not self.healed else ghost_speed
        self.main.movement(speed)


    def GoingBackHomeEventSequence(self):
        if self.main.rect.center == self.main.gatePos and not self.healed:
            self.main.VerticalMovement(self.main.direction, 1)

        if self.main.hitbox.center == (290, 300):
            self.healed = True
            self.main.add(self.main.level.visible_sprites)
            self.main.VerticalMovement(self.main.direction, -1)

        if self.main.rect.center == self.main.gatePos and self.healed:
            self.SwitchState(self.stateCache.scatterState())

    def CheckSwitchState(self):
        self.GoingBackHomeEventSequence()


    def ExitState(self):
        self.healed = False


class Ghosts(Entity):

    def __init__(self,group):
        super().__init__(group)
        self.chaseState = False
        self.eaten = False
        self.GhostEatenSound = mixer.Sound(Sounds["GhostEaten"])
        self.scatterTimer = Timer(self.ScatterDuration,self.switchToChaseState)

    def importSprites(self):
        path = f"Sprites/Ghosts/Body/"

        self.animations = {f"{self.name}": [], "Frightened": [],
                           "Up": [], "Down": [], "Left": [], "Right": []
                           }

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animateEyes(self):
        eye = self.animations[self.spriteDirection][0].convert_alpha()
        return self.screen.blit(eye, (self.rect.x, self.rect.y))
    
    def switchToChaseState(self):
        self.currentState.SwitchState(self.stateCache.chaseState())

    def Eaten(self):
        if self.currentState != self.stateCache.eatenState():
            self.currentState.SwitchState(self.stateCache.eatenState())


    def animate(self):
        animation = self.animations[self.name] if self.currentState != self.stateCache.frightenedState() else self.animations["Frightened"]

        self.frame_index += self.animation_time
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.currentState != self.stateCache.frightenedState():
            self.animateEyes()


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

    def __init__(self, image,group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite,level):
        super().__init__(group)

        self.name = "Blinky"
        self.bounceCount = 0
        self.homeDuration = 0
        self.ScatterDuration = 15000
        self.startingPos = (280,300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.player = player
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.level = level
        self.color = (255,0,0)

        self.eye = pg.image.load("Sprites/Ghosts/Body/Up/1.png")

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()


        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.scatterState()
        self.currentState.EnterState()

    def TargetTile(self):
        return self.player.rect.center

    def ResetState(self):
        self.currentState = self.stateCache.scatterState()
        self.currentState.EnterState()
        self.chaseState = False

    def update(self):

        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()



class Pinky(Ghosts):

    def __init__(self, image,group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite,level):
        super().__init__(group)

        self.name = "Pinky"

        self.homeDuration = 2
        self.bounceCount = 0
        self.ScatterDuration = 16000
        self.startingPos = (290, 300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.level = level

        self.color = (255, 80, 255)

        self.player = player
        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.homeState()
        self.currentState.EnterState()


    def TargetTile(self):

        playerDirection = self.player.directionFacing
        playerX = self.player.rect.centerx
        playerY = self.player.rect.centery

        match playerDirection:
            case "Up":
                x = playerX
                y = playerY - 80
            case "Down":
                x = playerX
                y = playerY + 80
            case "Left":
                x = playerX - 80
                y = playerY
            case "Right":
                x = playerX + 80
                y = playerY
            case _:
                x = self.rect.centerx
                y = self.rect.centery

        return (x,y)

    def ResetState(self):
        self.bounceCount = 0
        self.currentState = self.stateCache.homeState()
        self.currentState.EnterState()
        self.chaseState = False


    def update(self):
        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()


class Inky(Ghosts):

    def __init__(self, image, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite,blinky,level):
        super().__init__(group)

        self.name = "Inky"

        self.homeDuration = 5
        self.bounceCount = 0
        self.ScatterDuration = 17000
        self.startingPos = (270, 300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object

        self.level = level

        self.color = (224,255,255)
        self.player = player
        self.blinky = blinky
        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type

        self.importSprites()

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.homeState()
        self.currentState.EnterState()

    def TargetTile(self):

        playerDirection = self.player.direction
        playerX = self.player.rect.centerx
        playerY = self.player.rect.centery

        blinkyX = self.blinky.rect.centerx
        blinkyY = self.blinky.rect.centery


        if playerDirection.y < 0:
            targetX = playerX
            targetY = (playerY - 40)
        elif playerDirection.y > 0:
            targetX = playerX
            targetY = (playerY + 40)
        elif playerDirection.x < 0:
            targetX = (playerX - 40)
            targetY = playerY
        elif playerDirection.x > 0:
            targetX = (playerX + 40)
            targetY = playerY

        buffX = targetX - blinkyX
        buffY = targetY - blinkyY

        tilex = targetX - buffX
        tiley = targetY - buffY

        targetTileX = (tilex * math.cos(0) - tiley * math.sin(0)) + (buffX * 2)
        targetTileY = (tilex * math.sin(0) + tiley * math.cos(0)) + (buffY * 2)



        return targetTileX,targetTileY

    def ResetState(self):
        self.bounceCount = 0
        self.currentState = self.stateCache.homeState()
        self.currentState.EnterState()
        self.chaseState = False
    def update(self):

        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()


class Clyde(Ghosts):

    def __init__(self, image, group,collidableSprite,node_sprite,node_object,object_type,player,portal_sprite,level):
        super().__init__(group)

        self.name = "Clyde"
        self.homeDuration = 7
        self.bounceCount = 0
        self.ScatterDuration = 18000
        self.startingPos = (310, 300)
        self.gatePos = (290, 250)
        self.portals = portal_sprite
        self.collision_sprite = collidableSprite
        self.nodes = node_sprite
        self.node_object = node_object
        self.player = player

        self.level = level
        self.color =(255,190,190)

        self.currentDirection = "Horizontal"

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)

        self.object_type = object_type

        self.importSprites()
        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.homeState()
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

    def ResetState(self):
        self.bounceCount = 0
        self.currentState = self.stateCache.homeState()
        self.currentState.EnterState()
        self.chaseState = False

    def update(self):

        self.CheckPortalCollision()
        self.currentState.UpdateState()
        self.getSpriteDirection()
        self.animate()

