import pygame

from .config import *

class Player (pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface( (40,40) )
        self.image.fill(ORANGE)

        self.rect = self.image.get_rect()
        self.rect.x= 100
        self.rect.y=100

