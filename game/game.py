import sys
import pygame

from .config import *
from .platform import Platform
from .player import Player

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode( (WITDH,HEIGHT) )
        pygame.display.set_caption(TITLE)

        self.running = True 

    def star(self):
        self.new()

    def new(self):
        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform=Platform()
        self.player= Player(100,self.platform.rect.top-200)

        self.sprites= pygame.sprite.Group()
        self.sprites.add(self.platform)
        self.sprites.add(self.player)


    def run (self):
        
        while self.running:
            self.event()
            self.draw()
            self.update()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running= False
                pygame.QUIT
                sys.exit()
    def draw (self):
        self.surface.fill(BLUE)
        
        self.sprites.draw(self.surface)
    def update (self):
        pygame.display.flip()

        self.sprites.update()

        self.player.validate_platform(self.platform)

    def stop(self):
        pass