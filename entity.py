import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        self.direction = pg.math.Vector2()




    def movement(self,speed):

        self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.checkCollisions("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkCollisions("Vertical")
        self.rect.center = self.hitbox.center


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
