import pygame
import params

class Scene:
    """
    bacon.
    A wrapper class for both animations and levels.
    """

    def load_assets(self):
        """
        Initialize all assets.
        """
        assert False # should never call from Scene


    def __init__(self, screen):
        self.screen = screen
        self.camera_x, self.camera_y = 0, 0 # We assume 1920 x 1080.
        self.ticks = 0

        # Current background index
        self.background_index = 0
        
        # Current soundtrack index
        self.soundtrack_index = 0

        # Show sprites?
        self.show = {"real" : {sprite : 0 for sprite in self.sprites},
                     "dream" : {sprite : 0 for sprite in self.sprites}}
        
        # Blink status default to closed
        self.cur_eye_state = False

        # Last tick on which blink information changed
        self.last_tick_change = 0

        # real or dream?
        self.state = "real"

    def update_music(self, index, volume, fade_time):
        """
        Switch the music from to index and play with given volume
        Fade out the music over fade_time ms.
        """
        pygame.mixer.fadeout(fade_time)
        self.soundtrack_index = index
        pygame.mixer.music.load(self.soundtracks[self.soundtrack_index])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def burst(self) -> None:
        self.screen.blit(self.backgrounds[self.background_index].get_image(), (-self.camera_x, -self.camera_y))
        for sprite in self.sprites:
            if self.show[self.state][sprite]:
                self.screen.blit(sprite.get_image(), sprite.rect.move(-self.camera_x, -self.camera_y))
                
    def update_camera_pos(self) -> None:
        """
        To be overridden.
        Adjust the camera position.
        """
        pass

    def give_blink(self, blink_data) -> None:
        """
        Process new current blink data
        """
        if blink_data != self.cur_eye_state:
            self.last_tick_change = self.ticks
        self.cur_eye_state = blink_data

    def give_gaze(self, screen_gaze) -> None:
        """
        Process new gaze data
        """
        self.screen_gaze = screen_gaze

    def tick(self, blink_data, screen_gaze):
        """
        To be overridden.
        Perform one game tick.
        """
        self.give_blink(blink_data)
        self.give_gaze(screen_gaze)
        self.update_camera_pos()
        self.burst()
        self.ticks += 1

    def is_done(self) -> bool:
        """
        To be overridden.
        Returns if this Scene has completed.
        """
        pass