print("Adding Menu State...")

# Imports

import stateman as state
import dapong
import os, sys
from fontman import fonts

pygame = state.pygame       # Get pygame module from state manager

screen = None               # Game's main screen
controlscreen = False
titlescreen = True          # Determines if title screen should be displayed

buttons = [["VS PLAYER",200,200,120,60],["VS CPU",400,200,120,60],["CONTROLS",200,300,120,60],["QUIT",400,300,120,60]]

def drawRectOutline(scrn,x,y,w,h,bgc,olc):
    ol = pygame.Rect(x-4,y-4,w+8,h+8)
    bg = pygame.Rect(x,y,w,h)
    pygame.draw.rect(scrn,olc,ol)
    pygame.draw.rect(scrn,bgc,bg)

def init(scrn,sett=None):   # Initiate state
    global coinSfx
    global screen
    global selected
    global delta
    global clickSfx
    selected = -1
    screen = scrn                                                       # Get game's main screen
    state.printMsg("Initiating Menu State...",3)
    print("Initiating Menu State")
    coinSfx = pygame.mixer.Sound(os.path.join("sounds", "score.wav"))   # Load coin sound effect
    clickSfx = pygame.mixer.Sound(os.path.join("sounds", "click.wav"))  # Load click sound effect

def update(dt,clck):
    delta = dt

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
        if controlscreen:
            text = fonts["scorefont"].render("Controls", True, (255,255,255))
            controls = [None,None,None,None,None]
            controls[0] = "PLAYER 1              PLAYER 2"
            controls[1] = "W                           UP"
            controls[2] = "S                            DOWN"
            controls[3] = ""
            controls[4] = "Show FPS - F1  Screenshot - F10  ESC - Quit"

            offset = (text.get_size()[0]/2,text.get_size()[1]/2)                                # Get center of the window
            pos = ((size[0]/2)-offset[0],(size[1]/4)-offset[1])                                 # Center the title text
            screen.blit(text,pos)
            for i in range(5):
                contrltext = fonts["fpsfont"].render(controls[i], True, (255,255,255))          # Create controls text
                if i == 4:
                    pos = (120,200+(i*30))
                else:
                    pos = (200,200+(i*30))
                screen.blit(contrltext,pos)

        else:
            text = fonts["scorefont"].render("DaPong", True, (255,255,255))                  # Create title logo using big font
            info = "Press 1 for Singlepayer - Press 2 for Multiplayer"
            text2 = fonts["fpsfont"].render(info, True, (255,255,255))                          # Create subtitle text
            

            offset = (text.get_size()[0]/2,text.get_size()[1]/2)    # Get center of the window
            pos = ((size[0]/2)-offset[0],(size[1]/4)-offset[1])     # Center the title text
            screen.blit(text,pos)                                   # Draw title text
            i = 0
            for b in buttons:
                bt = fonts["fpsfont"].render(b[0], True, (255,255,255))
                if selected == i:
                    drawRectOutline(screen,b[1],b[2],b[3],b[4],(128,128,128),(255,255,255))
                else:
                    drawRectOutline(screen,b[1],b[2],b[3],b[4],(0,0,0),(255,255,255))
                screen.blit(bt, (b[1],b[2]+2) )
                i+=1
    
    # END OF DRAW

def keypressed(key,mod):
    global titlescreen
    global controlscreen
    if controlscreen:
        controlscreen = False
    else:
        if titlescreen:
            if key == pygame.K_RETURN:
                titlescreen = False
                coinSfx.play()
            if key == pygame.K_ESCAPE:
                sys.exit()
        else:          
            if key == pygame.K_ESCAPE:
                sys.exit()

def mbuttonreleased(pos,button):
    global selected
    global controlscreen
    if controlscreen:
        controlscreen = False
    else:
        if button == 1:
            if selected == 0:
                clickSfx.play()
                state.change("game",screen)             # Change to game state without AI enabled
            elif selected == 1:
                clickSfx.play()
                state.change("game",screen,{"ai":True}) # Change to game state with AI enabled
            elif selected == 2:
                clickSfx.play()
                controlscreen = True
            elif selected == 3:
                clickSfx.play()
                sys.exit()

def mousemoved(pos,rel,buttns):
    mx = pos[0]
    my = pos[1]
    if not titlescreen:
        global selected
        selected = -1
        i = 0
        for b in buttons:
            x = b[1]
            y = b[2]
            w = b[3]
            h = b[4]
            if mx > x and mx < (x+w) and my > y and my < (y+h):
                selected = i
            i+=1

def quit():
    print("Exiting from menu")

# EOF
