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

def play(level):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    # q_in.put('STOP')
                    sys.exit()
        level.screen.fill((255,255,255))
        level.tick(eye.pull_blink_state(), eye.pull_gaze_info())
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
    eye.init(vars(ap.parse_args()))
    eye.start_blink_loop()

    # Initialize Pygame
    pygame.init()

    screen_info = pygame.display.Info()
    # Create the screen
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))

    # screen = pygame.display.set_mode((1300, 750))
    pygame.display.set_caption("InVitro")

    # Clock for controlling FPS
    clock = pygame.time.Clock()

    # Initialize the Pygame font module
    font = pygame.font.Font(None, 36)

    import level_0
    play(level_0.L0(screen))
    pygame.quit()
    sys.exit()