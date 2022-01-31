import math
import random
import pygame

pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien.png")
pygame.display.set_icon()

rocket=pygame.image.load("rocket.png")