#!/usr/bin/python3
# DaPong Project - A simple pong game made in Python
# Started 26.04.2022
# Luke Lasok 2022

import pygame, sys, os      # Import important stuff
import stateman as state    # Import the state manager  
from fontman import fonts   # Import font list

version = "dev_02.05.22"    # Version of the program

# Additional functions

def readArgs(argc, argv):   # Read arguments and change settings (currently unused)
    pass

def initPyGame(res,title):  # Initialize PyGame and setup game window
    pygame.init()                                                       # Initiate PyGame
    iconimg = pygame.image.load(os.path.join("graphics", "icon.png"))   # Load icon graphic
    scrn = pygame.display.set_mode(res)                                 # Set window resolution
    pygame.display.set_caption(title)                                   # Set window title
    pygame.display.set_icon(iconimg)                                    # Set window icon
    return scrn, True                                                   # Return screen and True allowing loop to run
    
# MAIN FUNCTION

def main(argc, argv):
    print("DaPong v."+version)
    readArgs(argc, argv)                                    # Currently unused
    screen, running = initPyGame((720,420),"DaPong")        # Initiate PyGame, returns screen and True if it was successfull
    clock = pygame.time.Clock()
    # Add fonts to the font manager
    fonts["fpsfont"] = pygame.font.Font(os.path.join("fonts", 'FFFFORWA.TTF'), 16)
    fonts["scorefont"] = pygame.font.Font(os.path.join("fonts", 'FFFFORWA.TTF'), 100)
    fonts["infofont"] = pygame.font.SysFont("Arial",16)
    # Setup stateman
    state.change("menu",screen)                             # Change state to "menu"
    # Prepare for loop
    dt = 0.0
    last = 0.0
    # MAIN LOOP
    while running:
        # Get time
        t = pygame.time.get_ticks()

        # Logic updates
        state.update(dt,clock)  # Update state logic
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               # Quit event 
                state.quit()
                running = False
            elif event.type == pygame.KEYDOWN:                          # Key pressed once event
                state.keypressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:                            # Key released event
                state.keyreleased(event.key, event.mod)
            elif event.type == pygame.MOUSEMOTION:                      # Mouse moved event
                state.mousemoved(event.pos, event.rel, event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:                    # Mouse button released event
                state.mbuttonreleased(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:                  # Mouse button pressed once event
                state.mbuttonpressed(event.pos, event.button)

        # Key input
        keys = pygame.key.get_pressed()                                 # Key held down
        if keys:
            state.keydown(keys)
        
        # Draw
        screen.fill((0, 0, 0))      # Reset screen to prevent smearing effect
        state.draw(screen)          # Draw state
        pygame.display.flip()       # Update screen
        # Timer stuff
        clock.tick()                # Update timer
        dt = (t - last) / 1000.0    # Get Delta Time
        last = t                    # Update last timer
        
        
# END OF MAIN

if __name__=="__main__":
    main(len(sys.argv),sys.argv)

# EOF