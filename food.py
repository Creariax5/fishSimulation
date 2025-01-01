import pygame
import random


class Food:
    def __init__(self, map):
        self.pos = pygame.Vector2(random.randint(0, map.width), random.randint(0, map.height))
        self.size = 4

    def draw(self, screen):
        pygame.draw.circle(screen, "green", self.pos, self.size)
