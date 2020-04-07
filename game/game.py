import sys
import pygame
import random

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode( (WITDH,HEIGHT) )
        pygame.display.set_caption(TITLE)

        self.running = True 

        self.clock =pygame.time.Clock()

    def star(self):
        self.new()

    def new(self):
        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform=Platform()
        self.player= Player(100,self.platform.rect.top-200)

        
        self.sprites= pygame.sprite.Group()
        self.walls= pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls()
    
    def generate_walls(self):

        last_position = WITDH + 10

        if not len(self.walls)>0:

            for w in range(0,MAX_WALLS):
                left = random.randrange(last_position+200, last_position+400)
                wall = Wall(left,self.platform.rect.top)
                last_position = wall.rect.right

                self.sprites.add(wall)
                self.walls.add(wall)


    def run (self):
        
        while self.running:
            self.clock.tick(FPS)
            self.event()
            self.draw()
            self.update()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running= False
                pygame.QUIT
                sys.exit()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.player.jump()
    def draw (self):
        self.surface.fill(BLUE)
        
        self.sprites.draw(self.surface)
    def update (self):
        pygame.display.flip()

        self.sprites.update()

        self.player.validate_platform(self.platform)

        wall = self.player.collide_with(self.walls)
        if wall:
            self.stop()
            print('colision')

    def stop(self):
        pass