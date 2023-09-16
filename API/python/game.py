import argparse
import os
import sys
import time
import pygame
import multiprocessing as mp

# global parameters
import params

# For getting eye data
import eye

# sprites
import sprites

def test_loop():
    # Initialize Pygame
    pygame.init()

    screen_info = pygame.display.Info()
    params.SCREEN_WIDTH = screen_info.current_w
    params.SCREEN_HEIGHT = screen_info.current_h

    # Create the screen
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))

    # screen = pygame.display.set_mode((1300, 750))
    pygame.display.set_caption("InVitro")

    # Load background image
    background_image = pygame.image.load("images/night_bg.png")  # Replace with the path to your background image
    background_image = pygame.transform.scale(background_image, (params.SCREEN_WIDTH, params.SCREEN_HEIGHT))  # Resize image

    invitro_img = pygame.image.load("images/invitro_no_bg.jpg")  # Replace with the path to your background image
    invitro_img = pygame.transform.scale(invitro_img, (params.SCREEN_WIDTH, params.SCREEN_HEIGHT))  # Resize image

    bg_img_list = [background_image, invitro_img]
    #music_list = ["audio/Wondering(chosic.com).mp3",
    #            "audio/Embrace(chosic.com).mp3"]
    music_list = []

    # Clock for controlling FPS
    clock = pygame.time.Clock()

    # Initialize the Pygame font module
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    sprite = sprites.EyeSensObject('real', 2, (10, 10))
    player = sprites.Player('dream', 2)

    # Main game loop
    running = True
    init_close_eyes = 1
    scene_index = 0
    scene_changed = True

    # game music
    pygame.mixer.init()
    #pygame.mixer.music.load(music_list[scene_index])
    #pygame.mixer.music.set_volume(0.4)
    #pygame.mixer.music.play()
    
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    # q_in.put('STOP')
                    sys.exit()

        # Clear the screen with the background image
        screen.blit(bg_img_list[scene_index], (0, 0))

        screen_gaze = eye.pull_gaze_info()

        # eye tracking 
        if screen_gaze is not None:
            eye_pos = font.render('Eye coords: ({:.2f}, {:.2f})'.format(screen_gaze.x, screen_gaze.y), False, (255, 0, 0))
            # pygame.draw.circle(screen, (255, 0, 0), (screen_gaze.x, screen_gaze.y), 150)
            screen.blit(eye_pos, (0, 0))

            if abs(screen_gaze.x - sprite.rect.x) < 150 and abs(screen_gaze.y - sprite.rect.y) < 150:
                sprite.update()


        screen.blit(sprite.image, sprite.rect)
        # # Update player
        player.update()

        # # Draw player
        screen.blit(player.image, player.rect)

        eye_open = eye.pull_blink_state()
        # process blink data 
        eye_state_text = font.render('Eyes open?: ' + str(eye_open), False, (255, 0, 0))
        if not eye_open: # eyes are CLOSED
            if init_close_eyes: # eyes just started closing
                closed_start = time.time()
                scene_changed = False
                init_close_eyes = 0

            time_closed = time.time() - closed_start
                
            if time_closed > 5 and not scene_changed: 
                scene_index = (scene_index + 1) % 2
                screen.blit(bg_img_list[scene_index], (0, 0))
                #pygame.mixer.music.load(music_list[scene_index])
                #pygame.mixer.music.set_volume(0.4)
                #pygame.mixer.music.play()
                scene_changed = True

            time_closed_text = font.render(f'Closed for {int(time_closed)}', False, (255, 0, 0))
            screen.blit(time_closed_text, (0, 200))
        else: # eyes open
            init_close_eyes = 1
        
        screen.blit(eye_state_text, (0, 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
    eye.init(vars(ap.parse_args()))
    eye.start_blink_loop()
    test_loop()