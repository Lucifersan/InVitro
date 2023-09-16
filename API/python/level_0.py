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
                        sprites.CollidableSprite("collidable", self,
                            sprites.frame_load_helper("collidable", ["real", "dream"], [""]), "real", "", width=160, height=160, x = 500, y = params.SCREEN_HEIGHT - 400)]
        
        # Get background images
        self.backgrounds = [sprites.FlippableSprite("background", self, 
                            sprites.frame_load_helper("background", ["real", "dream"], [""], "background"), "real", "")]
        
        print(self.sprites[0].frames)
        print(self.backgrounds[0].frames)

        # Get soundtracks
        self.soundtracks = []


    def __init__(self, screen):
        self.load_assets()
        super().__init__(screen)
        self.show = {"real" : {sprite : True for sprite in self.sprites},
                     "dream" : {sprite : True for sprite in self.sprites}}

    def update_camera_pos(self) -> None:
        """
        To be overridden.
        Adjust the camera position.
        """
        camera_tx = self.sprites[0].rect.centerx - params.CENTER_WIDTH
        camera_ty = self.sprites[0].rect.centery - params.CENTER_HEIGHT
        self.camera_x = 0.9 * self.camera_x + 0.1 * camera_tx
        self.camera_y = min(0.1 * params.SCREEN_HEIGHT, 0.9 * self.camera_y + 0.1 * camera_ty)

    def tick(self, blink_data, screen_gaze):
        """
        To be overridden.
        Perform one game tick.
        """
        print(self.ticks, self.last_tick_change, blink_data, screen_gaze)
        flip = (self.ticks - self.last_tick_change == params.BLINK_FRAME_THRESHOLD) and blink_data == False
        if flip:
            if self.state == "real":
                self.state = "dream"
            else:
                self.state = "real"
        for sprite in self.sprites:
            sprite.update(self.state, blink_data, screen_gaze)
            if isinstance(sprite, sprites.CollidableSprite):
                sprite.push(self.sprites[0])
        super().tick(blink_data, screen_gaze)

    def is_done(self) -> bool:
        """
        To be overridden.
        Returns if this Scene has completed.
        """
        pass

