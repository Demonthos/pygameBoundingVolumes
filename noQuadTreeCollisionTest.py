import pygame
from pygame import Rect
from Particle import Particle
import random
import sys

width, height = 600, 600

walls = Rect(0, 0, width, height)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("particle life")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


r = 5
particles = [Particle(random.randint(1, width - r*2 - 1), random.randint(1, height - r*2 - 1), r) for _ in range(450)]
for p in particles:
    p.velocity = [random.random() * 2 - 1, random.random() * 2 - 1]
    p.color = [random.randint(0, 255) for _ in range(3)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    clock.tick(60)
    for p in particles:
        p.move(walls)
    for p in particles:
        colliding = []
        for otherP in particles:
            if p != otherP and p.rect.colliderect(otherP.rect):
                colliding.append(otherP)
        if colliding:
            p.color[0] = 255
            for r in colliding:
                clipped = p.rect.clip(r)
                adjustment = clipped.width/2, clipped.height/2
                minIndex = adjustment[0] > adjustment[1]
                newPos = list(p.pos)
                newPos[minIndex] -= adjustment[minIndex]*(1 - 2*(p.pos[minIndex] > (r.y if minIndex else r.x)))
                p.updatePos(*newPos)
                p.velocity[minIndex] *= -1
                # p.move(walls)
        else:
            p.color[0] = 0
        p.draw(screen)
    screen.blit(update_fps(), (10, 0))
    pygame.display.flip()
