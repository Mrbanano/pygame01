import os
import sys
import pygame
import random

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall
from .coin import Coin

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode( (WITDH,HEIGHT) )
        pygame.display.set_caption(TITLE)

        self.running = True 
        

        self.clock =pygame.time.Clock()

        self.font=pygame.font.match_font(FONT)

        self.dir =os.path.dirname(__file__)
        self.dir_sound= os.path.join(self.dir,'source/sounds')
        self.dir_img= os.path.join(self.dir,'source/sprites')

    def star(self):
        self.new()

    def new(self):
        self.score= 0
        self.level=0
        self.playing= True

        self.background = pygame.image.load(os.path.join(self.dir_img,'bg.png'))
        self.platform_bg = pygame.image.load(os.path.join(self.dir_img,'platform.jpg'))
        
        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform=Platform()

        self.player= Player(100,self.platform.rect.top-200,self.dir_img)

        
        self.sprites= pygame.sprite.Group()
        self.walls= pygame.sprite.Group()
        self.coins= pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls()
        
    def generate_walls(self):

        last_position = WITDH + 100

        if not len(self.walls)>0:

            for w in range(0,MAX_WALLS):
                left = random.randrange(last_position+200, last_position+400)
                wall = Wall(left,self.platform.rect.top,self.dir_img)
                last_position = wall.rect.right

                self.sprites.add(wall)
                self.walls.add(wall)

            self.level += 1
            self.generate_coins()

    def generate_coins(self):
        last_position = WITDH + 100

        for c in range (0,MAX_COINS):
             pos_x= random.randrange(last_position+130, last_position+300)
             coin=Coin(pos_x,150,self.dir_img)

             last_position= coin.rect.right

             self.sprites.add(coin)
             self.coins.add(coin)

    def run (self):
        
        while self.running:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()
            
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running= False
                pygame.QUIT
                sys.exit()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]:
            self.player.jump()
        if key[pygame.K_r] and not self.playing:
            self.new()
            
    def draw (self):
        self.surface.blit(self.background,(0,0))
        self.platform.image.blit(self.platform_bg,(0,0))
        self.draw_text()

        self.sprites.draw(self.surface)

        pygame.display.flip()
    
    def update (self):
        if self.playing:

            wall = self.player.collide_with(self.walls)
            if wall:
                if self.player.collide_bottom(wall):
                    self.player.skid(wall)
                else:
                    sound = pygame.mixer.Sound(os.path.join(self.dir_sound,'lose.wav'))
                    sound.play()
                    self.stop()

            coin = self.player.collide_with(self.coins)
            if coin:
                self.score +=1
                coin.kill()

                sound = pygame.mixer.Sound(os.path.join(self.dir_sound,'coins.wav'))
                sound.play()

            self.sprites.update()

            self.player.validate_platform(self.platform)

            self.update_elements(self.walls)
            self.update_elements(self.coins)

            self.generate_walls()
         
    def update_elements(self,elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def stop(self):
         self.stop_elements(self.walls)
         self.player.stop()
         
         self.playing= False
    
    def stop_elements(self,elements):
        for element in elements:
            element.stop()

    def score_format(self):
        return '{}'.format(self.score)

    def level_format(self):
        return '{}'.format(self.level)
    
    def draw_text (self):
        self.display_text(self.score_format(),30, CUSTOM2, 600,38)
        self.display_text(self.level_format(),30, CUSTOM1, 200,38)

        if not self.playing:
            self.display_text('Game Over ',60, RED, WITDH//2,HEIGHT//2)
            self.display_text('R to Restar ',30, RED, WITDH//2,HEIGHT//2+40)
            
    def display_text(self,text,size,color,pos_x,pos_y):
        font = pygame.font.Font(self.font,size)
        text= font.render(text,True, color )
        rect = text.get_rect()
        rect.midtop= (pos_x, pos_y)
        
        self.surface.blit(text,rect)
