import pygame

from pygame.locals import *
from sense_hat import SenseHat

pygame.init()
pygame.display.set_mode((640, 480))

sense = SenseHat()
sense.clear()

running = True

x = 0
y = 0
sense.set_pixel(x, y, 255, 255, 255)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            sense.set_pixel(x, y, 0, 0, 0)  # Black 0,0,0 means OFF

            if event.key == K_DOWN and y < 7:
                y = y + 1
            elif event.key == K_UP and y > 0:
                y = y - 1
            elif event.key == K_RIGHT and x < 7:
                x = x + 1
            elif event.key == K_LEFT and x > 0:
                x = x - 1

        sense.set_pixel(x, y, 255, 255, 255)
        if event.type == QUIT:
            running = False
            print("BYE")
