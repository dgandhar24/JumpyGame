# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.l = 0
        self.r = 0
        self.flag_l = 0
        self.flag_r = 0
        self.cframe_l = 0
        self.cframe_r = 0
        
        self.image = pg.Surface((48, 64))
        #self.image.fill(YELLOW)
        self.image = pg.image.load("jumpy.png").convert()
        self.stand = pg.image.load("jumpy.png").convert()
        self.walk1_r = pg.image.load("walk1_r.png").convert()
        self.walk2_r = pg.image.load("walk2_r.png").convert()
        self.walk1_l = pg.image.load("walk1_l.png").convert()
        self.walk2_l = pg.image.load("walk2_l.png").convert()
        self.jumpy = pg.image.load("jump.png").convert()
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
        

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.l += 1
            self.flag_l = 1
            if self.cframe_l == 0 and self.l > 5:
                self.l = 0
                self.image = self.walk2_l
                self.cframe_l = (self.cframe_l + 1) % 2
            elif self.cframe_l == 1 and self.l > 5:
                self.l = 0
                self.image = self.walk1_l
                self.cframe_l = (self.cframe_l + 1) % 2


        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.r += 1
            self.flag_r = 1
            if self.cframe_r == 0 and self.r > 5:
                self.r = 0
                self.image = self.walk2_r
                self.cframe_r = (self.cframe_r + 1) % 2
            elif self.cframe_r == 1 and self.r > 5:
                self.r = 0
                self.image = self.walk1_r
                self.cframe_r = (self.cframe_r + 1) % 2

        if not(keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
                self.r = 0
                self.l = 0
                self.image = self.stand

        if self.vel.y < 0:
            self.image = self.jumpy

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
