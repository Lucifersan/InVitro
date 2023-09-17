import scene
import pygame
import sprites
import params
import math

class L0(scene.Scene):
    """
    bacon.
    A wrapper class for both animations and levels.
    """

    def load_assets(self):
        """
        Initialize all assets.
        """
        # The first sprite in the list is special, and the camera will follow it.

        self.sprites = [sprites.Player("player", self, 
                            sprites.frame_load_helper("player", ["real", "dream"], ["still", "walk", "jump"]), "real", "still"),
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 900, y = params.SCREEN_HEIGHT - 150),
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 600, y = params.SCREEN_HEIGHT - 100),
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 300, y = params.SCREEN_HEIGHT - 50), 
                        sprites.EyeMovableSprite("eyemovable", self,
                            sprites.frame_load_helper("eyemovable", ["real", "dream"], [""]), "real", "", x = 1800, y = params.SCREEN_HEIGHT - 600, 
                                start_coords=(1800, params.SCREEN_HEIGHT - 600), finish_coords=(1800, params.SCREEN_HEIGHT - 0), eye_focus=(150, 150)),
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 2500, y = params.SCREEN_HEIGHT - 100), 
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 2900, y = params.SCREEN_HEIGHT - 200), 
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 3300, y = params.SCREEN_HEIGHT - 300), 
                        sprites.EyeMovableSprite("eyemovable", self,    
                            sprites.frame_load_helper("eyemovable", ["real", "dream"], [""]), "real", "", x = 3700, y = params.SCREEN_HEIGHT - 200, 
                                start_coords=(3700, params.SCREEN_HEIGHT - 50), finish_coords=(3700, params.SCREEN_HEIGHT - 450), reverse=True, eye_focus=(150, 150)),
                        sprites.CollidableSprite("stationary", self,
                            sprites.frame_load_helper("stationary", ["real", "dream"], [""]), "real", "", x = 4100, y = params.SCREEN_HEIGHT - 500),
                        sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""], scaling = 4), "real", "", x=0, y = params.SCREEN_HEIGHT - 100, animate_on_sight = True),
                        sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""], scaling = 6), "real", "", x=200, y = params.SCREEN_HEIGHT - 150, animate_on_sight = True),
                        sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""], scaling = 4), "real", "", x=1200, y = params.SCREEN_HEIGHT - 100, animate_on_sight = True),
                        sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""], scaling = 3), "real", "", x=1400, y = params.SCREEN_HEIGHT - 75, animate_on_sight = True), 
                        sprites.FlippableSprite("floor", self,
                            sprites.frame_load_helper("floor", ["real", "dream"], [""]), "real", "", x=0, y=params.SCREEN_HEIGHT - 8),
                        sprites.FlippableSprite("floor", self,
                            sprites.frame_load_helper("floor", ["real", "dream"], [""]), "real", "", x=1920, y=params.SCREEN_HEIGHT - 8),
                        sprites.FlippableSprite("floor", self,
                            sprites.frame_load_helper("floor", ["real", "dream"], [""]), "real", "", x=-1920, y=params.SCREEN_HEIGHT - 8),
                        sprites.FlippableSprite("floor", self,
                            sprites.frame_load_helper("floor", ["real", "dream"], [""]), "real", "", x=3840, y=params.SCREEN_HEIGHT - 8),
                        sprites.FlippableSprite("floor", self,
                            sprites.frame_load_helper("floor", ["real", "dream"], [""]), "real", "", x=5760, y=params.SCREEN_HEIGHT - 8),
                        sprites.FlippableSprite("paintbrush", self,
                            sprites.frame_load_helper("paintbrush", ["real", "dream"], [""]), "real", "", x=4200, y = params.SCREEN_HEIGHT - 600), 
                        sprites.FlippableSprite("clouds", self,
                            sprites.frame_load_helper("clouds", ["real", "dream"], [""], scaling=6), "real", "", x = 800, y = 0)
                        ]
        
        self.eye_open = pygame.image.load("images/seen.png")
        self.eye_open = pygame.transform.scale(self.eye_open, (self.eye_open.get_width() * 4, self.eye_open.get_height() * 4))
        self.eye_closed = pygame.image.load("images/unseen.png")
        self.eye_closed = pygame.transform.scale(self.eye_closed, (self.eye_closed.get_width() * 4, self.eye_closed.get_height() * 4))

        # Get background images
        self.backgrounds = [sprites.FlippableSprite("background_level1", self, 
                            sprites.frame_load_helper("background_level1", ["real", "dream"], [""], "background"), "real", "")]

        print(self.sprites[0].frames)
        print(self.backgrounds[0].frames)

        # Get soundtracks
        self.soundtracks = []


    def __init__(self, screen):
        self.load_assets()
        super().__init__(screen)
        self.show = {"real" : {sprite : True for sprite in self.sprites},
                     "dream" : {sprite : True for sprite in self.sprites}}
        
        self.parallax[self.sprites[-1]] = 0.1

        self.state = "dream"
        

    def update_camera_pos(self) -> None:
        """
        To be overridden.
        Adjust the camera position.
        """
        camera_tx = self.sprites[0].rect.centerx - params.CENTER_WIDTH
        camera_ty = self.sprites[0].rect.centery - params.CENTER_HEIGHT
        self.camera_x = 0.9 * self.camera_x + 0.1 * camera_tx
        self.camera_y = min(0.1 * params.SCREEN_HEIGHT, 0.9 * self.camera_y + 0.1 * camera_ty)

    def burst(self):
        super().burst()
        for sprite in self.sprites:
            if isinstance(sprite, sprites.EyeMovableSprite):
                print("Drawing at",sprite.rect.x + sprite.eye_focus[0] - self.eye_open.get_width() / 2,
                      sprite.rect.y + sprite.eye_focus[1] - self.eye_open.get_height() / 2)
                if sprite.is_looked_at(self.screen_gaze):
                    self.screen.blit(self.eye_open, (sprite.rect.x + sprite.eye_focus[0] - self.eye_open.get_width() / 2 - self.camera_x,
                                                    sprite.rect.y + sprite.eye_focus[1] - self.eye_open.get_height() / 2 - self.camera_y))
                else:
                    self.screen.blit(self.eye_closed, (sprite.rect.x + sprite.eye_focus[0] - self.eye_closed.get_width() / 2 - self.camera_x,
                                                        sprite.rect.y + sprite.eye_focus[1] - self.eye_closed.get_height() / 2 - self.camera_y))

        #s = pygame.Surface((params.SCREEN_WIDTH,params.SCREEN_HEIGHT))
        #if self.ticks - self.last_tick_change > params.BACKGROUND_TRANSITION_TIME:
        #    return
        #s.set_alpha(256 * (self.ticks - self.last_tick_change) * (self.blink_data == False) / params.BACKGROUND_TRANSITION_TIME)
        #s.fill((0, 0, 0))
        #self.screen.blit(s, (0,0)) 


    def tick(self, blink_data, screen_gaze):
        """
        To be overridden.
        Perform one game tick.
        """
        print(self.ticks, self.last_tick_change, blink_data, screen_gaze)
        self.blink_data = blink_data
        flip = False and (self.ticks - self.last_tick_change == params.BACKGROUND_TRANSITION_TIME) and blink_data == False
        if flip:
            if self.state == "real":
                self.state = "dream"
            else:
                self.state = "real"
        for sprite in self.sprites:
            sprite.update(self.state, blink_data, screen_gaze)
            if isinstance(sprite, sprites.CollidableSprite):
                sprite.push(self.sprites[0])
        # pulse the paintbrush
        self.sprites[-2].rect.y = params.SCREEN_HEIGHT - 700 + 30 * math.sin(self.ticks / 40)
        self.backgrounds[self.background_index].update(self.state, blink_data, screen_gaze)
        super().tick(blink_data, screen_gaze)

    def is_done(self) -> bool:
        """
        To be overridden.
        Returns if this Scene has completed.
        """
        return self.sprites[0].rect.x >= 4150

