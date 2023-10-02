import pygame as pg
from entity import Entity
from support import import_folder
from settings import *
from Sounds import *

class Pacman(Entity):
    def __init__(self,image,sprite_group,collidable_sprite,node_sprite,portal_sprite,level):
        super().__init__(sprite_group)

        self.PowerUp = False
        self.eaten = False

        self.image = pg.image.load(image).convert_alpha()

        self.image = pg.transform.scale(self.image,(20,20))

        self.start_pos = (300, 360)

        self.level = level
        self.rect = self.image.get_rect(topleft=self.start_pos)
        self.nodes = node_sprite
        self.hitbox = self.rect.inflate(0,0)
        self.collision_sprite = collidable_sprite

        self.importSprites()


        self.portals = portal_sprite
        self.directionFacing = "Left"
        self.spriteState = self.directionFacing

        self.HorizontalMovement(self.direction, -1)

    def ResetState(self):
        self.eaten = False
        self.directionFacing = "Left"
        self.spriteState = self.directionFacing
        self.hitbox.x = self.start_pos[0]
        self.hitbox.y = self.start_pos[1]
        self.rect.center = self.hitbox.center
        self.HorizontalMovement(self.direction,-1)

    def GhostCollide(self,ghost):
        if self.PowerUp:
            if not ghost.eaten:
                ghost.Eaten()
                self.level.score += 100

        else:
            if not self.eaten:
                self.eaten = True
                PlaySound("PacmanDying")

    def importSprites(self):
        player_path = "Sprites/Pacman/"

        self.animations_States = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                                  "Death": [] }

        for animation in self.animations_States.keys():
            full_path = player_path + animation
            self.animations_States[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations_States[self.spriteState]
        self.frame_index += self.animation_time
        if self.frame_index >= len(animation):
            if self.directionFacing == "Death":
                self.level.pacmanEaten = True
                self.level.startLevel = False

            else:
                self.frame_index = 0

        self.image = animation[int(self.frame_index)].convert_alpha() if self.level.startLevel else pg.image.load(Sprites["Blank"]).convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def setDirection(self,direction):
        match self.directionFacing:
            case "Up":
                    self.VerticalDirection(direction,self.VerticalMovement,-1,"Up")
            case "Down":
                    self.VerticalDirection(direction,self.VerticalMovement,1,"Down")
            case "Left":
                    self.HorizontalDirection(direction,self.HorizontalMovement,-1,"Left")
            case "Right":
                    self.HorizontalDirection(direction,self.HorizontalMovement,1,"Right")


    def checkifAlive(self):
        if self.eaten:
            self.directionFacing = "Death"
            self.spriteState = self.directionFacing

    def VerticalDirection(self,direction,function,value,spriteDirection):
        self.savePreviousDirection(direction)
        if self.previous_direction.y == value * -1:
            direction.y = direction.y * -1
            self.spriteState = spriteDirection
        else:
            if self.NodeCollided():
                function(direction, value)
                self.spriteState = spriteDirection

    def HorizontalDirection(self,direction,function,value,spriteDirection):
        self.savePreviousDirection(direction)
        if self.previous_direction.x == value * -1:
            direction.x = direction.x * -1
            self.spriteState = spriteDirection
        else:
            if self.NodeCollided():
                function(direction, value)
                self.spriteState = spriteDirection


    def get_inputs(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]: # Up
            self.directionFacing = "Up"

        elif keys[pg.K_s]: # Down
            self.directionFacing = "Down"

        if keys[pg.K_a]: # Left
            self.directionFacing = "Left"

        elif keys[pg.K_d]: # Right
            self.directionFacing = "Right"

    def update(self):

        self.CheckPortalCollision()
        self.checkifAlive()

        if not self.eaten:
            self.get_inputs()
            self.movement(pacman_Speed)
            self.setDirection(self.direction)

        self.animate()


