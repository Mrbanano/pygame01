import sys
import pygame

from .config import *

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode( (WITDH,HEIGHT) )
        pygame.display.set_caption(TITLE)

        self.running = True 

    def star(self):
        self.new()

    def new(self):
        self.run()

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
        self.surface.fill(BLACK)
    def update (self):
        pygame.display.flip()
    def stop(self):
        pass