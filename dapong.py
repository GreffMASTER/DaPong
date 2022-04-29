#!/usr/bin/python3
# DaPong Project - A simple pong game made in Python
# Started 26.04.2022
# Luke Lasok 2022

import pygame, sys, os      # Import important stuff
import stateman as state    # Import the state manager  
from fontman import fonts   # Import font list

FPS = 60
version = "devtest1"

def readArgs(argc, argv):   # Read arguments and change settings (currently unused)
    pass

def initPyGame(res,title):   # Initialize PyGame and setup game window
    global screen
    pygame.init()
    iconimg = pygame.image.load(os.path.join("graphics", "icon.png"))
    scrn = pygame.display.set_mode(res)
    screen = scrn
    pygame.display.set_caption(title)
    pygame.display.set_icon(iconimg)
    return scrn, True

def main(argc, argv):                   # The main function
    readArgs(argc, argv)                # Currently unused
    screen, running = initPyGame((720,420),"DaPong")      # Initiate PyGame, returns screen and True if it was successfull
    clock = pygame.time.Clock()
    # Add fonts to the font manager
    fonts["fpsfont"] = pygame.font.Font(os.path.join("fonts", 'FFFFORWA.TTF'), 16)
    fonts["scorefont"] = pygame.font.Font(os.path.join("fonts", 'FFFFORWA.TTF'), 100)
    fonts["infofont"] = pygame.font.SysFont("Arial",16)
    # Setup stateman
    state.change("menu",screen)
    # Prepare for loop
    dt = 0.0
    last = 0.0
    while running:              # Main loop
        # Timer stuff
        t = pygame.time.get_ticks()

        # Logic updates
        state.update(dt,clock)  # Update state
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.quit()
                running = False
            elif event.type == pygame.KEYDOWN:
                state.keypressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:
                state.keyreleased(event.key, event.mod)
            elif event.type == pygame.MOUSEMOTION:
                state.mousemoved(event.pos, event.rel, event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                state.mbuttonreleased(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                state.mbuttonpressed(event.pos, event.button)

        # Key input
        keys = pygame.key.get_pressed()
        if keys:
            state.keydown(keys)
        
        # Draw
        screen.fill((0, 0, 0))  # Reset screen to prevent smearing effect
        state.draw(screen)      # Draw state
        pygame.display.flip()   # Update screen
        # Timer stuff
        clock.tick()                # Update timer
        dt = (t - last) / 1000.0    # Get Delta Time
        last = t                    # Update last timer
        
        
# END OF MAIN

if __name__=="__main__":
    main(len(sys.argv),sys.argv)

# EOF
