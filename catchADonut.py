from os import environ
from random import randint
import random
from time import sleep

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

FREE, RETRY = 0, 1
state = FREE

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
        #placement
        self.x = randint(30, WIDTH - 30)
        self.y = y

        #score
        self.points = 0
        self.misses = 0
        #text
        self.font = pg.font.SysFont("Arial", 36)
        self.text_points = self.font.render(f"Score: {self.points}", True, (0,0,0))
        self.text_misses = self.font.render(f"Misses: {self.misses}", True, (0,0,0))

        #random color for fruit
        self.color = random.choice(colorSelection)

        #move params
        self.speed = 5
        self.vel = pg.Vector2(0,0)

        #object
        self.object = pg.Rect(x, y, 30, 30)


    def draw(self, display):
        #fruits
        pg.draw.rect(display, self.color, self.object)
        #text
        screen.blit(self.text_points, (20, 20))
        screen.blit(self.text_misses, (20, 80))

    def update(self, playerobj):
        self.text_points = self.font.render(f"Score: {self.points}", True, (0,0,0))
        self.text_misses = self.font.render(f"Misses: {self.misses}", True, (0,0,0))

        if self.object.colliderect(playerobj):
            self.points += 1
            self.y = 0
            self.x = randint(30, WIDTH - 30)
            self.color = random.choice(colorSelection)
        else:
            if self.y < HEIGHT:
                self.y += self.speed
            else:
                self.misses += 1
                self.y = 0
                self.x = randint(30, WIDTH - 30)
                self.color = random.choice(colorSelection)


        self.object = pg.Rect(int(self.x), int(self.y), 30, 30)
        screen.blit(self.text_points, (20, 20))
        screen.blit(self.text_misses, (20, 80))





#class func config
player = Player(WIDTH/2, HEIGHT - 80)
objects = ObjectSpawn(30, 10)

def game_difficulty(x):
    match x:
        case 1:
            objects.speed = 10
        case 2:
            objects.speed = 5
        case 3:
            objects.speed = 7
        case 4:
            objects.speed = 9
        case 5:
            objects.speed = 12
        case _:
            objects.speed = 3

difficulty = 0

#for dt
prev_time = time.time()

#game loop
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

    #null the score if too much misses
    if objects.misses >= 3:
        objects.points = 0
        objects.misses = 0

    if objects.points % 2 == 0 and objects.points > 0:
        difficulty = difficulty+ 1
        print(difficulty)

    game_difficulty(difficulty)


    #main game func
    screen.fill((222, 197, 124))

    player.draw(screen)
    objects.draw(screen)
    objects.update(player.rect)
    player.move()

    pg.display.flip()
    clock.tick(60)

pg.quit()


