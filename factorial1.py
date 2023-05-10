from typing import Any
import pygame
from pygame.locals import *
from pygame.sprite import Group
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#variables
tile_size = 25
game_over = 0
main_menu = True
key_found = False
Press = False
complete1 = False
complete2 = False 
key_found1 = False
key_found2 = False
levels = False
world_data = 0
level1 = False
level2 = False
#load images
bg_img = pygame.image.load('img/bg.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')
level1_img = pygame.image.load('img/level1.png')
level2_img = pygame.image.load('img/level2.png')
level3_img = pygame.image.load('img/level3.png')
next_img = pygame.image.load('img/next.png')
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #mouse position
        pos = pygame.mouse.get_pos()

        #chech click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #button
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self,x,y):
        self.reset(x,y)    

    def update(self, game_over):        
        dx=0
        dy=0
        col_thresh = 20

        if game_over == 0:
            #get keyboard
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 10
            if key[pygame.K_RIGHT]:
                dx += 10

            
            #gravity
            self.vel_y += 0.5
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y    
            #check the collision
            self.in_air = True
            for tile in world.tile_list:
                #x collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y ,self.width,self.height):
                    dx = 0

                #y collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                    #below ground
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #above grounf   
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            #check for liquid
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1
            #check for grass
            if pygame.sprite.spritecollide(self, grass_group, False):
                game_over = -1

            #check for collisison with platform
            for platform in platform_group:
                #collision in the x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y ,self.width,self.height):
                    dx = 0
                #collision in the y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
					#check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0



            #update player position
            self.rect.x += dx
            self.rect.y += dy
            player_x = self.rect.x
            player_y = self.rect.y
            if self.rect.bottom >screen_height:
                self.rect.bottom = screen_height
                dy = 0            
        elif game_over == -1:
            self.image = self.dead_image
            self.rect.y -= 5


        #draw player
        screen.blit(self.image, self.rect)
        return game_over
    def reset(self,x,y):
        img = pygame.image.load('img/p1.png')
        self.image = pygame.transform.scale(img, (30,60))
        self.rect = self.image.get_rect()
        self.dead_image = pygame.image.load('img/ghost.png')
        self.rect.x = x 
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

class Player2():
    def __init__(self,x,y):
        self.reset(x,y)    

    def update(self, game_over):        
        dx=0
        dy=0
        col_thresh = 20

        if game_over == 0:
            #get keyboard
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_w] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 10
            if key[pygame.K_d]:
                dx += 10

            
            #gravity
            self.vel_y += 0.5
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y    
            #check the collision
            self.in_air = True
            for tile in world.tile_list:
                #x collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y ,self.width,self.height):
                    dx = 0

                #y collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                    #below ground
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #above grounf   
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            #check for liquid
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            #check for grass
            if pygame.sprite.spritecollide(self, grass_group, False):
                game_over = -1

            #check for collisison with platform
            for platform in platform_group:
                #collision in the x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y ,self.width,self.height):
                    dx = 0
                #collision in the y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
					#check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0



            #update player position
            self.rect.x += dx
            self.rect.y += dy
            player2_x = self.rect.x
            player2_y = self.rect.y
            if self.rect.bottom >screen_height:
                self.rect.bottom = screen_height
                dy = 0            
        elif game_over == -1:
            self.image = self.dead_image
            self.rect.y -= 5


        #draw player
        screen.blit(self.image, self.rect)
        return game_over
    def reset(self,x,y):
        img = pygame.image.load('img/p2.png')
        self.image = pygame.transform.scale(img, (30,60))
        self.rect = self.image.get_rect()
        self.dead_image = pygame.image.load('img/ghost.png')
        self.rect.x = x 
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
	    

class World():
    def __init__(self, data):
            self.tile_list = []
            dirt_img = pygame.image.load('img/stoneWall.png')
            ground_img = pygame.image.load('img/castle.png')

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile =(img, img_rect)
                        self.tile_list.append(tile)                
                    if tile == 2:
                        img = pygame.transform.scale(ground_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile =(img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        key2 = Key2(col_count * tile_size + (tile_size//2), row_count * tile_size + (tile_size // 2))
                        key2_group.add(key2)
                    if tile == 4:
                        platform = Platform(col_count * tile_size, row_count * tile_size)
                        platform_group.add(platform)
                    if tile == 5:
                        knopka = Knopka(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        knopka_group.add(knopka)
                    if tile == 6:
                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lava_group.add(lava)
                    if tile == 7:
                        key = Key(col_count * tile_size + (tile_size//2), row_count * tile_size + (tile_size // 2))
                        key_group.add(key)
                    if tile == 8:
                        exit = Exit(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        exit_group.add(exit)
                    if tile == 9:
                        exit2 = Exit2(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        exit2_group.add(exit2)
                    if tile == 10:
                        water = Water(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        water_group.add(water)
                    if tile == 11:
                        grass = Grass(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        grass_group.add(grass)
                    
                    
                    col_count += 1
                row_count += 1 
    def draw(self):
         for tile in self.tile_list:
              screen.blit(tile[0], tile[1])              

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
    
    def update(self):  
            if Press == True and self.move_counter<50:
                self.rect.y += (self.move_direction + 2) 
                self.move_counter += 1
            elif Press == False and self.move_counter>0:
                self.rect.y -= (self.move_direction + 2)
                self.move_counter -= 1

class Grass(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/grass.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
class Water(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/water.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size * 2, int(tile_size * 3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
class Exit2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door2.png')
        self.image = pygame.transform.scale(img, (tile_size * 2, int(tile_size * 3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
class Key(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/key.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
class Key2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/key2.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
class Knopka(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/button.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


knopka_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
grass_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
exit2_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
key2_group = pygame.sprite.Group()
platform2_group = pygame.sprite.Group()

world_data1 = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,8,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,4,4,4,4,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,11,11,11,11,1,1,1,1,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,10,10,10,10,1,1,1,1,6,6,6,6,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

world_data2 = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,7,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,3,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,5,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,8,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,0,0,1,1,1,11,11,11,11,11,11,11,11,11,11,11,11,11,11,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
[1,4,4,4,4,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],


]
player = Player(100,screen_height - 130)
player_two = Player2(100,screen_height - 30)
#create button
restart_button = Button(screen_width // 2-50, screen_height//2, restart_img)
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
level1_img = Button(screen_width // 2 - 250, screen_height // 2, level1_img)
level2_img = Button(screen_width // 2 , screen_height // 2, level2_img)
level3_img = Button(screen_width // 2 + 250, screen_height // 2, level3_img)
next_img = Button(screen_width // 2-150, screen_height//2, next_img)


run = True
while run:

    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            levels = True
            main_menu = False
    else:          
        if levels ==True:
            if level1_img.draw():
                world = World(world_data1)
                level1 = True
                levels = False

        else:
            world.draw()
            if game_over == 0:
                platform_group.update()
                if pygame.sprite.spritecollide(player, exit_group, False) and key_found1 == True:
                        complete1 = True 
                else: complete1 = False 
                if pygame.sprite.spritecollide(player_two, exit2_group, False) and key_found2 == True:
                        complete2 = True 
                else: complete2 = False              
                if pygame.sprite.spritecollide(player,knopka_group, False) or pygame.sprite.spritecollide(player_two,knopka_group, False):
                    Press = True
                else:
                    Press = False
                if pygame.sprite.spritecollide(player,key_group, True):
                    key_found1 = True
                if pygame.sprite.spritecollide(player_two,key2_group, True):
                    key_found2 = True
                if complete1 == True and complete2 == True and key_found1 == True and key_found2 == True:
                    game_over = 1
                platform_group.draw(screen)
                knopka_group.draw(screen)
                grass_group.draw(screen)
                lava_group.draw(screen)
                water_group.draw(screen)
                exit_group.draw(screen)
                exit2_group.draw(screen)
                key_group.draw(screen)
                key2_group.draw(screen)
                game_over = player.update(game_over)
                game_over = player_two.update(game_over)  
                
            #died
            if game_over == -1:
                if restart_button.draw():
                    player.reset(100,screen_height - 130)
                    player_two.reset(100,screen_height - 30)
                    game_over = 0
            if game_over == 1:
                if restart_button.draw():
                    player.reset(100,screen_height - 130)
                    player_two.reset(100,screen_height - 30)
                    game_over = 0
                    key_found = False
                    Press = False
                    knopka_group.draw(screen)
                    platform_group.draw(screen)
                    lava_group.draw(screen)
                    exit_group.draw(screen)
                    key_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()