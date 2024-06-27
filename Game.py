import pygame
import random
import numpy as np
import time
pygame.init()
class Roller(pygame.sprite.Sprite):
    def __init__(self, color, width, height, up, down, left, right, speed, w_width, w_height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.color = color
        
        self.width = width
        self.height = height
        
        self.w_width = w_width
        self.w_height = w_height

        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.rect.x -= self.speed
        if keys[self.right]:
            self.rect.x += self.speed
        if keys[self.up]:
            self.rect.y -= self.speed
        if keys[self.down]:
            self.rect.y += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.width > self.w_width:
            self.rect.x = self.w_width - self.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.height > self.w_height:
            self.rect.y = self.w_height - self.height

#screen 
WIDTH = 450
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255,255,255))
pygame.display.set_caption(title = 'ColorIO')
font = pygame.font.SysFont(None, 32)
welcome = font.render("Welcome!", True, (0,0,0))
instruction = font.render("Press SPACE to start!", True, (0,0,0))
screen.blit(welcome, (180, 250))
screen.blit(instruction, (145, 275))


#attributes
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
width = 50
height = 50
normal_speed = 5
fps = 60

#rollers
blue_roller = Roller(blue, width, height, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, normal_speed, WIDTH, HEIGHT)
red_roller = Roller(red, width, height, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, normal_speed, WIDTH, HEIGHT)

#groupping rollers
all_sprites = pygame.sprite.Group()
all_sprites.add(blue_roller, red_roller)

#game configurations
clock = pygame.time.Clock()
stop = False
start = False
superpower = 0
exists = False
point = pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 10, 10)
interval = 5


while not stop: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #start trigger
                start = True
                screen.fill((255,255,255))
                #roller positions                          
                red_roller.rect.x = 400
                red_roller.rect.y = 550
                blue_roller.rect.x = 0
                blue_roller.rect.y = 0
                red_roller.speed = normal_speed
                blue_roller.speed = normal_speed 

                starting_time = time.time() - interval
                last_time = starting_time

    if start:        
        #painting the screen
        for sprite in all_sprites: 
            pygame.draw.rect(screen, sprite.color, (sprite.rect.x, sprite.rect.y, sprite.width, sprite.height))
            sprite.update()              
            
        #timer
        current_time = time.time()       
        if int(current_time - starting_time) == 45:
            start = False
            #counting red and blue pixels
            pixel_array = pygame.surfarray.array3d(screen)

            red_color = np.array([255, 0, 0], dtype=np.uint8)
            # Create a mask for red pixels
            red_mask = np.all(pixel_array == red_color, axis=-1)
            # Count the number of red pixels
            red_pixels = np.sum(red_mask)
            
            blue_color = np.array([0, 0, 255], dtype=np.uint8)
            # Create a mask for red pixels
            blue_mask = np.all(pixel_array == blue_color, axis=-1)
            # Count the number of red pixels
            blue_pixels = np.sum(blue_mask)

            #identifying the winner
            if blue_pixels > red_pixels:
                text = font.render(str("Blue wins!"), True, (0,0,0))
            elif blue_pixels < red_pixels:
                text = font.render(str("Red wins!"), True, (0,0,0))
            else:
                text = font.render(str("Draw!"), True, (0,0,0))
            screen.blit(text, (180, 250))

        #implementing super powers
        if int(current_time - last_time) == interval: #displaying the first or new point with interval
            last_time = current_time #updating the time
            superpower = abs(superpower - 1)
            point.x = random.randint(50, WIDTH - 50)
            point.y = random.randint(50, HEIGHT - 50)
            pygame.draw.rect(screen, (0,0,0), point)
            for sprite in all_sprites:
                sprite.width = width
                sprite.height = height
                sprite.speed = normal_speed
            exists = True
        for sprite in all_sprites:
            if exists:
                if sprite.rect.colliderect(point):
                    if superpower:
                        sprite.width *= 2
                        sprite.height *= 2
                    else:
                        sprite.speed *= 2
                    pygame.draw.rect(screen, sprite.color, point)
                    exists = False
        
    pygame.display.flip()
    clock.tick(fps)


    


    