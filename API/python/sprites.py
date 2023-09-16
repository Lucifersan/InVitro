import pygame
import os
import params

def frame_load_helper(name, world_states, obj_states, scaling = 4):
    """
    Returns a frame mapping given a list of world states and object states.
    """
    ret = dict()
    for world_state in world_states:
        ret[world_state] = dict()
        for obj_state in obj_states:
            ret[world_state][obj_state] = []
            filename = name + "_" + world_state + "_" + obj_state + "_{0}.png"
            index = 0
            while True:
                path = os.path.join("images", filename.format(index))
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    if scaling == "background":
                        image = pygame.transform.scale(image, (params.SCREEN_WIDTH, params.SCREEN_HEIGHT))
                    else:
                        image = pygame.transform.scale(image, (image.get_width() * scaling, image.get_height() * scaling))
                    ret[world_state][obj_state].append(image)
                else:
                    break
                index += 1
    return ret

class FlippableSprite(pygame.sprite.Sprite):
    """
    A sprite that changes between the two worlds.
    """
    def __init__(self, name, scene, frames, world_state, obj_state, tick_delay = 5, x = 0, y = 0):
        """
        Frames is a mapping from "real" to a list of frames
        and "dream" to a list of frames

        each value itself is a map from states to frame pointers
        """
        self.exists = {"real" : True, "dream" : True} # When to render this
        super().__init__()
        self.scene = scene
        self.name = name
        self.frames = frames
        self.tick_delay = tick_delay
        self.world_state = world_state
        self.obj_state = obj_state
        self.zero_frame_pointer()
        print(self, self.frames)
        self.rect = self.get_image().get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def get_image(self):
        """
        Inputs a state, real or dream, and outputs the current image
        """
        assert self.exists[self.world_state]
        return self.frames[self.world_state][self.obj_state][self.frame_pointer]
    
    def zero_frame_pointer(self):
        self.frame_pointer = 0

    def flip_world_state(self, world_state):
        """
        flip world state and zero animation pointer
        """
        if world_state != self.world_state:
            self.zero_frame_pointer()
            self.world_state = world_state

    def flip_obj_state(self, obj_state):
        """
        flip object state and zero animation pointer
        """
        if obj_state != self.obj_state:
            self.zero_frame_pointer()
            self.obj_state = obj_state
    
    def update(self, world_state, blink_data, screen_gaze):
        """
        Update the sprite
        """
        self.flip_world_state(world_state)
        if self.scene.ticks % self.tick_delay == 0:
            animation_frames = len(self.frames[self.world_state][self.obj_state])
            self.frame_pointer = (1 + self.frame_pointer) % animation_frames

class Player(FlippableSprite):
    """
    Player sprite
    """
    def __init__(self, name, scene, frames, world_state, obj_state, tick_delay = 5, x = 0, y = 0):
        self.last_direction = "right"  # Initialize last direction as right
        super().__init__(name, scene, frames, world_state, obj_state, tick_delay, x, y)
        self.x_speed = 0
        self.y_speed = 0
        self.jump_power = -20
        self.jumping = False
        print("Made a player", self.last_direction)
    
    def get_image(self):
        """
        Inputs a state, real or dream, and outputs the current image
        """
        image = super().get_image()
        # Flip image based on last direction
        if self.last_direction == "left":
            return pygame.transform.flip(image, True, False)
        else:
            return image
        
    def update(self, flip, blink_data, screen_gaze):

        if self.y_speed != 0:
            self.jumping = True

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -5
            self.last_direction = "left"  # Update last direction to left
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 5
            self.last_direction = "right"  # Update last direction to right
        else:
            self.x_speed = 0

        # Handle jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.y_speed = self.jump_power
            self.jumping = True
            self.jump_start_tick = self.scene.ticks

        # Apply gravity
        if not (keys[pygame.K_SPACE] and self.jumping and self.scene.ticks - self.jump_start_tick < 10):
            self.y_speed += 1

        # Update position
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.y > params.SCREEN_HEIGHT - self.rect.height:
            self.y_speed = 0
            self.jumping = False
            self.rect.y = min(self.rect.y, params.SCREEN_HEIGHT - self.rect.height)

        print(self.rect.y, self.jumping, self.y_speed)
        if self.jumping:
            self.flip_obj_state("jump")
        else:
            if self.x_speed == 0 and self.y_speed == 0:
                self.flip_obj_state("still")
            else:
                self.flip_obj_state("walk")

        super().update(flip, blink_data, screen_gaze)


class CollidableSprite(FlippableSprite):
    def __init__(self, name, scene, frames, world_state, obj_state, width, height, x, y, tick_delay = 5):
        """
        A flippable sprite that allows for collisions.
        """
        super().__init__(name, scene, frames, world_state, obj_state, tick_delay, x, y)

    def rectify_x(self, sprite):
        # Fix x
        if self.rect.colliderect(sprite.rect):
            sprite.rect.move_ip(-sprite.x_speed, 0)
            if sprite.rect.centerx < self.rect.centerx:
                sprite.rect.x = self.rect.left - sprite.rect.width
            else:
                sprite.rect.x = self.rect.right
            sprite.x_speed = 0

    def rectify_y(self, sprite):
        # Fix y
        if self.rect.colliderect(sprite.rect):
            sprite.rect.move_ip(0, -sprite.y_speed)
            if sprite.rect.centery < self.rect.centery:
                sprite.rect.y = self.rect.top - sprite.rect.height
                sprite.jumping = False
            else:
                sprite.rect.y = self.rect.bottom
            sprite.y_speed = 0

    def push(self, sprite):
        """
        Push sprite away. Sprite should be a player
        """
        assert isinstance(sprite, Player)
        
        if not self.rect.colliderect(sprite.rect):
            return
        
        # midtop, midleft, midbottom, midright 
        if self.rect.collidepoint(sprite.rect.midtop) or self.rect.collidepoint(sprite.rect.midbottom):
            # TOO HIGH
            # FUCK     
            self.rectify_y(sprite)
            self.rectify_x(sprite)

        elif self.rect.collidepoint(sprite.rect.midleft) or self.rect.collidepoint(sprite.rect.midright):
            # NO
            self.rectify_x(sprite)
            self.rectify_y(sprite)

        else:
            for point in [sprite.rect.topleft, sprite.rect.topright, sprite.rect.bottomleft, sprite.rect.bottomright]:
                if self.rect.collidepoint(point):
                    dx = point[0] - self.rect.centerx
                    dy = point[1] - self.rect.centery
                    sx = abs(dx) * self.rect.height
                    sy = abs(dy) * self.rect.width
                    if sx >= sy:
                        self.rectify_x(sprite)
                        self.rectify_y(sprite)
                    else:
                        self.rectify_y(sprite)
                        self.rectify_x(sprite)


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