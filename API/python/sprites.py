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
    
    def distance_squared_to_gaze(self, screen_gaze):
        dx = self.rect.x + self.eye_focus[0] - screen_gaze[0]
        dy = self.rect.y + self.eye_focus[1] - screen_gaze[1]
        return dx * dx + dy * dy
    
    def is_looked_at(self, screen_gaze):
        return screen_gaze is not None and ((self.distance_squared_to_gaze(screen_gaze) < self.distance_threshold) ^ self.reverse)
        
    def __init__(self, name, scene, frames, world_state, obj_state, x = 0, y = 0, tick_delay = 5, animate_on_sight = False, eye_focus = (0,0), distance_threshold = 90000):
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
        self.animate_on_sight = animate_on_sight # Fuck it, you can only set this one manually
        self.reverse = False
        self.eye_focus = eye_focus
        self.distance_threshold = distance_threshold
    
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
        if self.scene.ticks % self.tick_delay == 0 and (not self.animate_on_sight or self.is_looked_at(screen_gaze)):
            animation_frames = len(self.frames[self.world_state][self.obj_state])
            self.frame_pointer = (1 + self.frame_pointer) % animation_frames

class Player(FlippableSprite):
    """
    Player sprite
    """
    def __init__(self, name, scene, frames, world_state, obj_state, x = 0, y = 0, tick_delay = 5):
        self.last_direction = "right"  # Initialize last direction as right
        super().__init__(name, scene, frames, world_state, obj_state, x, y, tick_delay)
        self.x_speed = 0
        self.y_speed = 0
        self.jump_power = -30
        self.jumping = False
        self.jump_start_tick = -100
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
            self.x_speed = -12
            self.last_direction = "left"  # Update last direction to left
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 12
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
            self.y_speed += 2

        # Update position
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.y > params.SCREEN_HEIGHT - self.rect.height:
            self.y_speed = 0
            self.jumping = False
            self.rect.y = min(self.rect.y, params.SCREEN_HEIGHT - self.rect.height)

        if self.jumping and self.scene.ticks - self.jump_start_tick >= 10:
            self.flip_obj_state("jump")
        else:
            if self.x_speed <= 2:
                self.flip_obj_state("still")
            else:
                self.flip_obj_state("walk")

        super().update(flip, blink_data, screen_gaze)


class CollidableSprite(FlippableSprite):
    def __init__(self, name, scene, frames, world_state, obj_state, x, y, tick_delay = 5):
        """
        A flippable sprite that allows for collisions.
        """
        super().__init__(name, scene, frames, world_state, obj_state, x, y, tick_delay)

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
    

class EyeMovableSprite(CollidableSprite):
    def __init__(self, name, scene, frames, world_state, obj_state, x, y, start_coords, finish_coords, eye_focus, ticks_to_complete = 200, distance_threshold = 90000, reverse = False, tick_delay = 5, alt_world=None):
        super().__init__(name, scene, frames, world_state, obj_state, x, y, tick_delay)
        print(self.world_state)
        print(self.frames)
        self.zero_frame_pointer()
        self.start_coords = start_coords
        self.finish_coords = finish_coords
        self.eye_focus = eye_focus
        self.ticks_to_complete = ticks_to_complete
        self.distance_threshold = distance_threshold
        self.counter = 0
        self.reverse = reverse
        self.alt_world = alt_world # if not None, then sprite must be moved in different world

    def update(self, flip, blink_data, screen_gaze, world_state):
        self.flip_world_state(world_state)
        
        if self.alt_world is None:
            if self.is_looked_at(screen_gaze):
                self.counter += 1
            else:
                self.counter -= 4

            self.counter = max(self.counter, 0)
            self.counter = min(self.counter, self.ticks_to_complete)

            self.rect.x = self.start_coords[0] + (self.finish_coords[0] - self.start_coords[0]) * self.counter / self.ticks_to_complete
            self.rect.y = self.start_coords[1] + (self.finish_coords[1] - self.start_coords[1]) * self.counter / self.ticks_to_complete

            print(self.rect.x, self.rect.y)

            super().update(flip, blink_data, screen_gaze)

        elif world_state == self.alt_world:
            self.flip_obj_state("alt") # "stuck" or "alt"; if in alt_world (world it can move in), should switch to "alt"
            if self.is_looked_at(screen_gaze):
                self.counter += 1
            else:
                self.counter -= 4

            self.counter = max(self.counter, 0)
            self.counter = min(self.counter, self.ticks_to_complete)

            self.rect.x = self.start_coords[0] + (self.finish_coords[0] - self.start_coords[0]) * self.counter / self.ticks_to_complete
            self.rect.y = self.start_coords[1] + (self.finish_coords[1] - self.start_coords[1]) * self.counter / self.ticks_to_complete

            print(self.rect.x, self.rect.y)

            super().update(flip, blink_data, screen_gaze)

        else:
            self.flip_obj_state("stuck")