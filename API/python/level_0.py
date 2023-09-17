import scene
import pygame
import sprites
import params

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
                            sprites.frame_load_helper("eyemovable", ["real", "dream"], [""]), "real", "", x = 1600, y = params.SCREEN_HEIGHT - 600, 
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
                        sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""]), "real", "", x=0, y = params.SCREEN_HEIGHT - 100),
                        #sprites.FlippableSprite("clouds", self,
                        #    sprites.frame_load_helper("clouds", ["real", "dream"], [""]), "real", "", x = 800, y = 0)
                        ]

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
        s = pygame.Surface((params.SCREEN_WIDTH,params.SCREEN_HEIGHT))
        if self.ticks - self.last_tick_change > params.BACKGROUND_TRANSITION_TIME:
            return
        s.set_alpha(256 * (self.ticks - self.last_tick_change) * (self.blink_data == False) / params.BACKGROUND_TRANSITION_TIME)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0,0)) 


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
        self.backgrounds[self.background_index].update(self.state, blink_data, screen_gaze)
        super().tick(blink_data, screen_gaze)

    def is_done(self) -> bool:
        """
        To be overridden.
        Returns if this Scene has completed.
        """
        pass

