import pygame
from pygame import Rect


class QuadTree:
    def __init__(self, rects: list, boundingBox=None, squareLocked=False, surface=None, debug=False, maxDepth=7,
                 maxRects=7):
        if debug:
            print(f'creating QuadTree with {rects}')
        if boundingBox:
            self.rect = boundingBox
        else:
            self.rect = Rect(rects[0])
            self.rect.unionall_ip(rects[1:])
            if squareLocked:
                if self.rect.width > self.rect.height:
                    self.rect.height = self.rect.width
                else:
                    self.rect.width = self.rect.height

        self.quadrants = [None] * 4
        quadrantsRect: list = [
            Rect(self.rect.x + ((i % 2) * self.rect.width / 2), self.rect.y + ((i > 1) * self.rect.height / 2),
                 self.rect.width / 2, self.rect.height / 2) for i in range(4)]
        inQuadrants = [[] for _ in range(4)]
        for r in rects:
            for i, q in enumerate(quadrantsRect):
                if q.colliderect(r):
                    inQuadrants[i].append(r)
        for i, e in enumerate(inQuadrants):
            if len(e) > 0:
                if maxDepth == 0 or len(e) <= maxRects:
                    self.quadrants[i] = e
                    # print(self.quadrants[i])
                    continue
                self.quadrants[i] = QuadTree(e, quadrantsRect[i], surface=None, maxDepth=maxDepth - 1,
                                             maxRects=maxRects)
        if surface:
            self.draw(surface)

    def getContainers(self, rect):
        if rect not in self:
            return set()
        containers = set()
        for el in self.quadrants:
            if el:
                if type(el) is QuadTree:
                    containers.update(el.getContainers(rect))
                elif type(el) is list:
                    # for r in el:
                    #     if r == rect:
                    containers.add(self)
        return containers

    def getColliding(self, rect) -> list:
        colliding = []
        for quadTree in self.getContainers(rect):
            for el in quadTree.quadrants:
                if el and type(el) is list:
                    for r in el:
                        if r != rect and rect.colliderect(r):
                            if r not in colliding:
                                colliding.append(r)
        return colliding

    def update(self, rects):
        quadrantsRect: list = [
            Rect(self.rect.x + ((i % 2) * self.rect.width / 2), self.rect.y + ((i > 1) * self.rect.height / 2),
                 self.rect.width / 2, self.rect.height / 2) for i in range(4)]
        for i, el in enumerate(self.quadrants):
            inQuadrant = []
            for rect in rects:
                if quadrantsRect[i].colliderect(rect):
                    inQuadrant.append(rect)
            if type(el) is list:
                self.quadrants[i] = inQuadrant
            elif el:
                el.update(inQuadrant)

    def draw(self, surface):
        for i, el in enumerate(self.quadrants):
            if type(el) is list:
                rect = Rect(self.rect.x + ((i % 2) * self.rect.width / 2),
                            self.rect.y + ((i > 1) * self.rect.height / 2),
                            self.rect.width / 2, self.rect.height / 2)
                pygame.draw.rect(surface, (255, 0, 0), rect, 1, border_radius=1)
            elif el:
                el.draw(surface)

    def __contains__(self, item: Rect):
        return self.rect.colliderect(item)
