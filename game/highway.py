import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(lane_size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = distance+150,y
        self.distance = distance

    def update(self, camera):
        if self.rect.right < 0:
            self.distance += 1150
        self.rect.centerx = self.distance-camera+450

class Line(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(IMAGE_DIR,START_LINE_IMAGE[0])).convert()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = 60,100
        self.distance = 60
        self.end_distance = finish_line

    def update(self, *args):
        if self.rect.right < 0:
            self.distance = self.end_distance
            self.image = pygame.image.load(path.join(IMAGE_DIR, START_LINE_IMAGE[1]))
        else:
            pass
