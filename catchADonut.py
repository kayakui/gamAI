from os import environ
from random import randint

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg
import time

WIDTH = 550
HEIGHT = 960

pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True


class Player:
    def __init__(self, x, y):
        self.player = pg.Rect(x, y, 70, 70)
        self.basket = pg.Rect(x - 50, y + 30, 70, 10)
        self.playerColor = (136, 29, 242)
        self.basketColor = (64, 45, 1)
        self.x = x
        self.y = y
        self.vel = pg.Vector2(0, 0)
        self.left_pressed = False
        self.right_pressed = False
        self.speed = 8

    def draw(self, display):
        pg.draw.rect(display, self.playerColor, self.player)
        pg.draw.rect(display, self.basketColor, self.basket)

    def update(self):
        self.vel = pg.Vector2(0,0)

        if self.left_pressed and not self.right_pressed:
            self.vel[0] = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel[0] = self.speed

        if self.vel != (0,0):
            self.vel.normalize_ip()

        self.x += self.vel[0] * self.speed

        self.player = pg.Rect(int(self.x), int(self.y), 70, 70)
        self.basket = pg.Rect(int(self.x), int(self.y - 30), 70, 10)

colorSelection = [
    (79, 235, 40),
    (245, 255, 61),
    (245, 37, 78),
    (255, 33, 13),
    (252, 40, 224)
]

color = colorSelection[randint(0, 4)]

class ObjectSpawn:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.points = 0
        self.font = pg.font.SysFont("Arial", 36)
        self.text = self.font.render(f"Score: {self.points}", True, (0,0,0))
        self.speed = 200
        self.vel = pg.Vector2(0,0)
        self.score = 0
        self.object = pg.Rect(x, y, 30, 30)
        self.colorSelection = [
            (79, 235, 40),
            (245, 255, 61),
            (245, 37, 78),
            (255, 33, 13),
            (252, 40, 224)
        ]

    def draw(self, display):
        pg.draw.rect(display, color, self.object)
        screen.blit(self.text, (20, 20))

    def update(self, delta, playerobj):
        self.text = self.font.render(f"Score: {self.points}", True, (0,0,0))

        if self.object.colliderect(playerobj):
            self.points += 1
            self.y = 0
        else:
            if self.y > (HEIGHT * -1):
                self.y += self.speed * delta

        self.object = pg.Rect(int(self.x), int(self.y), 30, 30)
        screen.blit(self.text, (20, 20))

player = Player(WIDTH/2, HEIGHT - 80)
objects = ObjectSpawn(WIDTH/2, 10)
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

    pg.display.flip()
    clock.tick(60)
    screen.fill((222, 197, 124))

    player.draw(screen)
    objects.draw(screen)

    player.update()
    objects.update(dt, player.basket)

pg.quit()


