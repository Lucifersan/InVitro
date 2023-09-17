import scene
import pygame
import sprites
import params

class S0(scene.Scene):
    """
    CUTSCENE ZERO
    """

    def load_assets(self):
        """
        Initialize all assets.
        """
        # The first sprite in the list is special, and the camera will follow it.

        self.sprites = [sprites.FlippableSprite("s0_{0}".format(i), self, 
                            sprites.frame_load_helper("s0_{0}".format(i), ["real", "dream"], [""], "background"), "real", "")
                                for i in range(10)]
    

        # Get background images
        self.backgrounds = [sprites.FlippableSprite("bush", self,
                            sprites.frame_load_helper("bush", ["real", "dream"], [""], "background"), "real", "")]

        # Get soundtracks
        self.soundtracks = ["music/cutscene0.mp3"]


    def __init__(self, screen):
        self.load_assets()
        self.update_music(0, 1, 100)
        super().__init__(screen)
        self.show = {"real" : {sprite : False for sprite in self.sprites},
                     "dream" : {sprite : False for sprite in self.sprites}}
        
        self.scaling = {"real" : {sprite : 1 for sprite in self.sprites},
                     "dream" : {sprite : 1 for sprite in self.sprites}}
        
        self.show["real"][self.sprites[0]] = True

    def update_camera_pos(self) -> None:
        """
        To be overridden.
        Adjust the camera position.
        """
        pass

    def burst(self) -> None:
        # Example of putting screen effects
        super().burst()
        self.screen_sfx(self.color, self.alpha)

    def screen_sfx(self, color, alpha):
        # Example of putting screen effects
        s = pygame.Surface((params.SCREEN_WIDTH,params.SCREEN_HEIGHT))
        s.set_alpha(alpha)
        s.fill(color)
        self.screen.blit(s, (0,0))


    def tick(self, blink_data, screen_gaze):
        """
        To be overridden.
        Perform one game tick.
        """

        """
        Godawful code for switching frames
        """
        if self.ticks >= 0 and self.ticks < 280:
            self.show["real"][self.sprites[0]] = True
            self.scaling["real"][self.sprites[0]] = 1 + ((280 - self.ticks) / 280) ** 2
        elif self.ticks >= 280 and self.ticks < 400:
            self.show["real"][self.sprites[1]] = True
            self.show["real"][self.sprites[0]] = False
            self.scaling["real"][self.sprites[1]] = 1 + ((400 - self.ticks) / 700) ** 2
        elif self.ticks >= 400 and self.ticks < 525:
            self.show["real"][self.sprites[2]] = True
            self.show["real"][self.sprites[1]] = False
            self.scaling["real"][self.sprites[2]] = 1 + ((500 - self.ticks) / 700) ** 2
        elif self.ticks >= 525 and self.ticks < 650:
            self.show["real"][self.sprites[3]] = True
            self.show["real"][self.sprites[2]] = False
            self.scaling["real"][self.sprites[3]] = 1 + ((700 - self.ticks) / 700) ** 2
        elif self.ticks >= 650 and self.ticks < 720:
            self.show["real"][self.sprites[4]] = True
            self.show["real"][self.sprites[3]] = False
            self.scaling["real"][self.sprites[4]] = 1 + ((750 - self.ticks) / 300) ** 2
        elif self.ticks >= 720 and self.ticks < 777:
            self.show["real"][self.sprites[5]] = True
            self.show["real"][self.sprites[4]] = False
        elif self.ticks >= 777 and self.ticks < 1020:
            self.show["real"][self.sprites[6]] = True
            self.show["real"][self.sprites[5]] = False
        elif self.ticks >= 1020 and self.ticks < 1170:
            self.show["real"][self.sprites[7]] = True
            self.show["real"][self.sprites[6]] = False
        elif self.ticks >= 1170 and self.ticks < 1200:
            self.show["real"][self.sprites[8]] = True
            self.show["real"][self.sprites[7]] = False
            self.scaling["real"][self.sprites[8]] = 1 + ((1250 - self.ticks) / 400) ** 2
        elif self.ticks >= 1200 and self.ticks < 1200:
            self.show["real"][self.sprites[8]] = True
            self.show["real"][self.sprites[7]] = False
            self.scaling["real"][self.sprites[8]] = 1 + ((1250 - self.ticks) / 400) ** 2
        elif self.ticks >= 1200 and self.ticks < 1300:
            self.show["real"][self.sprites[9]] = True
            self.show["real"][self.sprites[8]] = False
            self.scaling["real"][self.sprites[9]] = 1 + ((1250 - self.ticks) / 400) ** 2


        # example fade in effect
        self.color = (255, 255, 255)
        self.alpha = 0
        for transition_tick in [280, 400, 525, 780, 1275]:
            if transition_tick - 30 <= self.ticks and self.ticks < transition_tick:
                self.alpha = (self.ticks - (transition_tick - 30)) * 256 / 30

        super().tick(blink_data, screen_gaze)

    def is_done(self) -> bool:
        """
        To be overridden.
        Returns if this Scene has completed.
        """
        return self.ticks >= 1400
        pass

