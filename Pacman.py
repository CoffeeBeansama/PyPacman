import pygame as pg
from entity import Entity
from support import import_folder
from settings import *

class Pacman(Entity):
    def __init__(self,image,pos,sprite_group,collidable_sprite,node_sprite,portal_sprite,level):
        super().__init__(sprite_group)

        self.image = pg.image.load(image).convert_alpha()

        self.image = pg.transform.scale(self.image,(20,20))

        self.eaten = False
        self.level = level
        self.rect = self.image.get_rect(topleft=pos)
        self.nodes = node_sprite
        self.hitbox = self.rect.inflate(0,0)
        self.collision_sprite = collidable_sprite

        self.importSprites()

        self.PowerUp = False
        self.portals = portal_sprite

        self.state = "Left"
        self.current_direction = "Left"
        self.next_direction.x = -1
        self.next_direction.y = 0

        self.HorizontalMovement(self.direction, -1)

    def importSprites(self):
        player_path = "Sprites/Pacman/"

        self.animations_States = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                                  "Death": []
                           }

        for animation in self.animations_States.keys():
            full_path = player_path + animation
            self.animations_States[animation] = import_folder(full_path)

    def animate(self):
        # increments the frame index when receiving input
        # when frame index reaches to maximum it loops over again to repeat the animation cycle

        animation = self.animations_States[self.state]
        self.frame_index += self.animation_time


        if self.frame_index >= len(animation):
            if self.state == "Death":
                self.level.startLevel = False

            else:
                self.frame_index = 0


        self.image = animation[int(self.frame_index)] if self.level.startLevel else pg.image.load(Sprites["Blank"]).convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def setDirection(self,direction):

        if self.current_direction == "Up":
            self.savePreviousDirection(direction)

            if self.previous_direction.y == 1:
                direction.y = direction.y * -1
            else:
                if self.NodeCollided():
                    self.VerticalMovement(direction, -1)


        elif self.current_direction == "Down":
            self.savePreviousDirection(direction)
            if self.previous_direction.y == -1:
                direction.y = direction.y * -1
            else:
                if self.NodeCollided():
                    self.VerticalMovement(direction, 1)

        elif self.current_direction == "Left":
            self.savePreviousDirection(direction)
            if self.previous_direction.x == 1:
                direction.x = direction.x * -1
            else:

                if self.NodeCollided():
                    self.HorizontalMovement(direction, -1)


        elif self.current_direction == "Right":

            self.savePreviousDirection(direction)
            if self.previous_direction.x == -1:
                direction.x = direction.x * -1
            else:
                if self.NodeCollided():
                    self.HorizontalMovement(direction, 1)

    def getSpriteDirection(self):
        if not self.eaten:
            if self.direction.y == -1:
                self.state = "Up"
            elif self.direction.y == 1:
                self.state = "Down"
            elif self.direction.x == -1:
                self.state = "Left"
            elif self.direction.x == 1:
                self.state = "Right"
        else:
            self.state = "Death"






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
        self.getSpriteDirection()
        self.animate()
        self.movement(pacman_Speed)


