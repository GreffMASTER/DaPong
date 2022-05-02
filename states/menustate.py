print("Adding Menu State...")

# Imports

import stateman as state
import dapong
import os
from fontman import fonts

pygame = state.pygame       # Get pygame module from state manager

screen = None               # Game's main screen
coinSfx = None              # Coin sound

titlescreen = True          # Determines if title screen should be displayed

def init(scrn,sett=None):   # Initiate state
    global coinSfx
    global screen
    screen = scrn                                                       # Get game's main screen
    state.printMsg("Initiating Menu State...",3)
    print("Initiating Menu State")
    coinSfx = pygame.mixer.Sound(os.path.join("sounds", "score.wav"))   # Load coin sound effect

def draw(screen):
    size = screen.get_size()    # Get window resolution
    if titlescreen:             # Draw title screen
    
        text = fonts["scorefont"].render("DaPong", True, (255,255,255))                     # Create title logo using big font
        text2 = fonts["fpsfont"].render("Insert coin or press Enter.", True, (255,255,255)) # Create subtitle text
        vertext = fonts["fpsfont"].render("v."+dapong.version, True, (255,255,255))         # Create version text

        offset = (text.get_size()[0]/2,text.get_size()[1]/2)    # Get center of the window
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])     # Center the title text
        screen.blit(text,pos)                                   # Draw title text

        offset = (text2.get_size()[0]/2,text2.get_size()[1]/2)  # Get center of the window
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])     # Center the subtitle text
        screen.blit(text2,(pos[0]+10,pos[1]+70))                # Draw subtitle text below the title text
        
        screen.blit(vertext,(5,size[1]-25))                     # Draw version text in the bottom left corner of the window
        
    else:                       # Draw main menu
    
        text = fonts["scorefont"].render("Pick Mode", True, (255,255,255))                  # Create title logo using big font
        info = "Press 1 for Singlepayer - Press 2 for Multiplayer"
        text2 = fonts["fpsfont"].render(info, True, (255,255,255))                          # Create subtitle text
        controls = "P1 - W,S  P2 - UP,DOWN  Show FPS - F1  Screenshot - F10  ESC - Quit"
        contrltext = fonts["fpsfont"].render(controls, True, (255,255,255))                 # Create controls text

        offset = (text.get_size()[0]/2,text.get_size()[1]/2)    # Get center of the window
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])     # Center the title text
        screen.blit(text,pos)                                   # Draw title text

        offset = (text2.get_size()[0]/2,text2.get_size()[1]/2)  # Get center of the window
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])     # Center the subtitle text
        screen.blit(text2,(pos[0],pos[1]+70))                   # Draw subtitle text below the title text
        
        screen.blit(contrltext,(5,size[1]-25))                  # Draw controls text in the bottom left corner of the window
    
    # END OF DRAW

def keypressed(key,mod):
    global titlescreen
    if titlescreen:
        if key == pygame.K_RETURN:
            titlescreen = False
            coinSfx.play()
        if key == pygame.K_ESCAPE:
            pygame.quit()
    else:
        if key == pygame.K_1:
            state.change("game",screen,{"ai":True}) # Change to game state with AI enabled
        if key == pygame.K_2:
            state.change("game",screen)             # Change to game state without AI enabled
        if key == pygame.K_ESCAPE:
            titlescreen = True

# EOF