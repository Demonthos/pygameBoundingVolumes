import pygame
from pygame import Rect
from Particle import Particle
from KDTree import KDTree
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


r = 1
particles = [Particle(random.randint(1, width/2 - r*2 - 1), random.randint(1, height/2 - r*2 - 1), r) for _ in range(2000)]
for p in particles:
    p.velocity = [random.random() * 2 - 1, random.random() * 2 - 1]
    p.velocity = [e*2 for e in p.velocity]
    p.color = [random.randint(0, 255) for _ in range(3)]
kDTree = KDTree([p.rect for p in particles], boundingBox=walls)
updateCounter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    clock.tick(60)
    for p in particles:
        p.move(walls)
    updateCounter += 1
    if updateCounter > 5:
        updateCounter = 0
        kDTree = KDTree([p.rect for p in particles], boundingBox=walls)
    else:
        kDTree.update([p.rect for p in particles])
    kDTree.draw(screen)
    for p in particles:
        colliding = kDTree.getColliding(p.rect)
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
