import pygame
import os

import params

class Platform(pygame.sprite.Sprite):
    def __init__(self, name, position, length=1):
        super().__init__()
        self.length = length
        raw_image = pygame.image.load(os.path.join('images', f"{name}.png"))  # Load animation frames
        self.image = pygame.transform.scale(raw_image, (raw_image.get_width() * .5, raw_image.get_height() * .5))  # Enlarge by 4 times
        
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.frame_index = 0
    

class EyeSensObject(pygame.sprite.Sprite):
    def __init__(self, name, frames, position):
        super().__init__()
        self.images = []  # List to store animation frames
        for i in range(frames):  
            image = pygame.image.load(
                os.path.join('images', f"{name}{i + 1}.png"))  # Load animation frames
            image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))  # Enlarge by 4 times
            self.images.append(image)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.frame_index = 0
        self.animation_speed = 300  # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]


class Player(pygame.sprite.Sprite):
    def __init__(self, name, frames):
        super().__init__()
        self.images = []  # List to store animation frames
        for i in range(frames):  
            image = pygame.image.load(
                os.path.join('images', f"{name}{i + 1}.png"))  # Load animation frames
            image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))  # Enlarge by 4 times
            self.images.append(image)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (params.SCREEN_WIDTH // 2, params.SCREEN_HEIGHT - self.rect.height)
        self.frame_index = 0
        self.animation_speed = 300  # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()
        self.x_speed = 0
        self.y_speed = 0
        self.jump_power = -90
        self.jumping = False
        self.last_direction = "right"  # Initialize last direction as right

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -42
            self.last_direction = "left"  # Update last direction to left
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 42
            self.last_direction = "right"  # Update last direction to right
        else:
            self.x_speed = 0

        # Flip image based on last direction
        if self.last_direction == "left":
            self.image = pygame.transform.flip(self.images[self.frame_index], True, False)
        else:
            self.image = self.images[self.frame_index]

        # Handle jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.y_speed = self.jump_power
            self.jumping = True

        # Update position
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Apply gravity
        if self.rect.y < params.SCREEN_HEIGHT - self.rect.height:
            self.y_speed += 13
        else:
            self.y_speed = 0
            self.jumping = False
            self.rect.y = params.SCREEN_HEIGHT - self.rect.height