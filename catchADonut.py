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

        #color
        self.basketColor = (64, 45, 1)

        #basket sprite var
        self.image = pg.Surface((70, 70))
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

    def draw(self, display):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.vel = pg.Vector2(0,0)

        if self.left_pressed and not self.right_pressed:
            self.vel[0] = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel[0] = self.speed

        if self.vel != (0,0):
            self.vel.normalize_ip()

        self.rect.x += self.vel[0] * self.speed

        self.image = pg.Surface((70, 10))
        self.image.fill(self.basketColor)

colorSelection = [
    (79, 235, 40),
    (245, 255, 61),
    (245, 37, 78),
    (255, 33, 13),
    (252, 40, 224)
]

class ObjectSpawn:
    def __init__(self, x ,y):
        self.x = randint(30, WIDTH - 30)
        self.y = y
        self.points = 0
        self.font = pg.font.SysFont("Arial", 36)
        self.text = self.font.render(f"Score: {self.points}", True, (0,0,0))
        self.color = random.choice(colorSelection)
        self.speed = 5
        self.vel = pg.Vector2(0,0)
        self.score = 0
        self.object = pg.Rect(x, y, 30, 30)

    def draw(self, display):
        pg.draw.rect(display, self.color, self.object)
        screen.blit(self.text, (20, 20))

    def update(self, playerobj):
        self.text = self.font.render(f"Score: {self.points}", True, (0,0,0))

        if self.object.colliderect(playerobj):
            self.points += 1
            self.y = 0
            self.x = randint(30, WIDTH - 30)
            self.color = random.choice(colorSelection)
        else:
            if self.y < HEIGHT:
                self.y += self.speed
            else:
                self.points -= 1
                self.y = 0
                self.x = randint(30, WIDTH - 30)
                self.color = random.choice(colorSelection)


        self.object = pg.Rect(int(self.x), int(self.y), 30, 30)
        screen.blit(self.text, (20, 20))





#class func config
player = Player(WIDTH/2, HEIGHT - 80)
objects = ObjectSpawn(30, 10)

#for dt
prev_time = time.time()


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

    player.draw(screen)
    objects.draw(screen)
    objects.update(player.rect)


    player.move()

    pg.display.flip()
    clock.tick(60)

pg.quit()


