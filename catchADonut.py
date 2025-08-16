from os import environ
from random import randint
import random

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg
import time

#screen size
WIDTH = 550
HEIGHT = 960

#window config
pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        #player rect + colors
        self.basketColor = (64, 45, 1)
        self.playerColor = (136, 29, 242)
        self.player = pg.Rect(x, y, 70, 70)

        #basket sprite var
        self.image = pg.Surface((70, 10))
        self.image.fill(self.basketColor)
        self.rect = self.image.get_rect()

        #location
        self.rect.x = x
        self.rect.y = y

        # movement variables
        self.vel = pg.Vector2(0, 0)
        self.left_pressed = False
        self.right_pressed = False
        self.speed = 8
        self.points = 0
        self.font = pg.font.SysFont("Arial", 36)
        self.text = self.font.render(f"Score: {self.points}", True, (0,0,0))

    def draw(self, display):
        pg.draw.rect(display, self.playerColor, self.player)
        screen.blit(self.image, (self.rect.x, self.rect.y - 30))


    def move(self):
        self.vel = pg.Vector2(0,0)

        if self.left_pressed and not self.right_pressed:
            self.vel[0] = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel[0] = self.speed

        if self.vel != (0,0):
            self.vel.normalize_ip()

        self.rect.x += self.vel[0] * self.speed

        self.player = pg.Rect(int(self.rect.x), int(self.rect.y), 70, 70)
        self.image = pg.Surface((70, 10))
        self.image.fill(self.basketColor)


colorSelection = [
    (79, 235, 40),
    (245, 255, 61),
    (245, 37, 78),
    (255, 33, 13),
    (252, 40, 224)
]



class Fruits(pg.sprite.Sprite):
    def __init__(self, col, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, x, y):
        self.rect.move_ip(0, 5)

        if pg.sprite.collide_rect(self, player):
            self.kill()
            add = 1
            self.rect.center = (x, y)
            fruit_group.add(fruits)
        else:
            if self.rect.top > HEIGHT:
                self.kill()
                add = 0
                self.rect.center = (x, y)
                fruit_group.add(fruits)


#class func config
player = Player(WIDTH/2, HEIGHT - 80)
players = pg.sprite.Group()
fruits = Fruits(random.choice(colorSelection), randint(30, WIDTH - 30), 55)

#for dt
prev_time = time.time()

#sprite group
fruit_group = pg.sprite.Group()
fruit_group.add(fruits)

while running:
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.left_pressed = True
            if event.key == pg.K_RIGHT:
                player.right_pressed = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player.left_pressed = False
            if event.key == pg.K_RIGHT:
                player.right_pressed = False

    screen.fill((222, 197, 124))

    fruits = Fruits(random.choice(colorSelection), randint(30, WIDTH - 30), 55)
    player.draw(screen)
    fruit_group.draw(screen)

    player.move()
    fruit_group.update(randint(30, WIDTH - 30), 55)

    pg.display.flip()
    clock.tick(60)

pg.quit()


