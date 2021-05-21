import pygame
import math
from pygame import Rect


class Particle:
    def __init__(self, x, y, r, color=(255, 255, 255), circle=False):
        self.pos: pygame.Vector2 = pygame.Vector2(x, y)
        self.r = r
        self.color = color
        self.rect = Rect(self.x, self.y, (self.r * 2) + 1, (self.r * 2) + 1)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.circle = circle

    def draw(self, screen):
        if self.circle:
            pygame.draw.circle(screen, self.color, (self.x + self.r, self.y + self.r), self.r)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        pygame.display.update(self.rect)

    def move(self, wallBox: Rect = None, loop=False):
        if wallBox:
            self.updateRect(self.velocity[0], 0)
            if not wallBox.contains(self.rect):
                if loop:
                    self.pos[0] = (wallBox.right - self.r - 10) if (self.pos[0] <= self.r) else self.r + 10
                    self.rect.x = self.pos[0]
                    # print(self.pos[0])
                else:
                    self.velocity[0] *= -1
                    self.pos[0] = max(0, min(self.pos[0], wallBox.right - self.r*2))
            self.updateRect(0, self.velocity[1])
            if not wallBox.contains(self.rect):
                if loop:
                    self.pos[1] = (wallBox.bottom - self.r - 10) if (self.pos[1] <= self.r) else self.r + 10
                    # print(self.pos[1])
                else:
                    self.velocity[1] *= -1
                    self.pos[1] = max(0, min(self.pos[1], wallBox.bottom - self.r*2))
        self.updatePos(*(self.pos + self.velocity))

    def updatePos(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.updateRect()

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def updateRect(self, x=0, y=0):
        self.rect.x, self.rect.y = self.x+x, self.y+y

    def checkCollision(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
