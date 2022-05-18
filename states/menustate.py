print("Adding Menu State...")

# Imports

import stateman as state
import dapong
import os, sys, pygame
from fontman import fonts

class menuvars:
    dt = 0
    timer = 0
    screen = None
    selected = -1
    titlescreen = True
    controlscreen = False
    ctrlhold = False
    points = 8
    balls = 1

buttons = [["VS PLAYER",130,200,120,60],["POINTS",296,200,120,60],["VS CPU",460,200,120,60],["CONTROLS",130,300,120,60],["BALLS",296,300,120,60],["QUIT",460,300,120,60]]

def drawRectOutline(scrn,x,y,w,h,bgc,olc):
    ol = pygame.Rect(x-4,y-4,w+8,h+8)
    bg = pygame.Rect(x,y,w,h)
    pygame.draw.rect(scrn,olc,ol)
    pygame.draw.rect(scrn,bgc,bg)

def init(scrn,sett=None):   # Initiate state
    global coinSfx
    global delta
    global clickSfx
    menuvars.ctrlhold = False
    menuvars.timer = 0
    menuvars.selected = -1
    menuvars.screen = scrn                                               # Get game's main screen
    coinSfx = pygame.mixer.Sound(os.path.join("sounds", "score.wav"))   # Load coin sound effect
    clickSfx = pygame.mixer.Sound(os.path.join("sounds", "click.wav"))  # Load click sound effect

def update(dt,clck):
    menuvars.dt = dt
    menuvars.timer += dt
    if menuvars.titlescreen:
        if menuvars.timer > 20:
            state.change("game",menuvars.screen,{"points":99,"ai":True,"aidif":2,"demo":True,"ballcount":2}) # Change to game state with demo mode
            menuvars.titlescreen = False

def draw(screen):
    size = screen.get_size()    # Get window resolution
    if menuvars.titlescreen:             # Draw title screen
    
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
        if menuvars.controlscreen:
            text = fonts["medfont"].render("Controls", True, (255,255,255))
            controls = [None,None,None,None,None]
            controls[0] = "PLAYER 1              PLAYER 2"
            controls[1] = "W                           UP"
            controls[2] = "S                            DOWN"
            controls[3] = ""
            controls[4] = "Show FPS - F1, Screenshot - F10, ESC - Quit"

            offset = (text.get_size()[0]/2,text.get_size()[1]/2)                                # Get center of the window
            pos = ((size[0]/2)-offset[0],(size[1]/4)-offset[1])                                 # Center the title text
            screen.blit(text,pos)
            for i in range(5):
                contrltext = fonts["fpsfont"].render(controls[i], True, (255,255,255))          # Create controls text
                if i == 4:
                    pos = (140,200+(i*30))
                else:
                    pos = (220,200+(i*30))
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
                if menuvars.selected == i:
                    drawRectOutline(screen,b[1],b[2],b[3],b[4],(128,128,128),(255,255,255))
                else:
                    drawRectOutline(screen,b[1],b[2],b[3],b[4],(0,0,0),(255,255,255))
                screen.blit(bt, (b[1],b[2]+2) )
                i+=1
            points = fonts["fpsfont"].render(str(menuvars.points), True, (255,255,255))
            balls = fonts["fpsfont"].render(str(menuvars.balls), True, (255,255,255))
            screen.blit(points, (296,238) )
            screen.blit(balls, (296,338) )
    
    # END OF DRAW

def keypressed(key,mod):
    if key == pygame.K_LCTRL:
        menuvars.ctrlhold = True

    if menuvars.controlscreen:
        menuvars.controlscreen = False
    else:
        if menuvars.titlescreen:
            if key == pygame.K_RETURN:
                menuvars.titlescreen = False
                coinSfx.play()
            if key == pygame.K_ESCAPE:
                sys.exit()
        else:          
            if key == pygame.K_ESCAPE:
                sys.exit()

def keyreleased(key,mod):
    if key == pygame.K_LCTRL:
        menuvars.ctrlhold = False

def mbuttonreleased(pos,button):
    if menuvars.controlscreen:
        menuvars.controlscreen = False
    else:
        if button == 1:
            if menuvars.selected == 0:
                clickSfx.play()
                state.change("game",menuvars.screen,{"points":menuvars.points,"ballcount":menuvars.balls,"debug":menuvars.ctrlhold})                    # Change to game state
            elif menuvars.selected == 1:
                clickSfx.play()
                menuvars.points += 1
                if menuvars.points > 24:
                    menuvars.points = 1
            elif menuvars.selected == 2:
                clickSfx.play()
                state.change("game",menuvars.screen,{"points":menuvars.points,"ai":True,"aidif":1,"ballcount":menuvars.balls,"debug":menuvars.ctrlhold})              # Change to game state with AI enabled
            elif menuvars.selected == 3:
                clickSfx.play()
                menuvars.controlscreen = True
            elif menuvars.selected == 4:
                clickSfx.play()
                menuvars.balls += 1
                if menuvars.balls > 10:
                    menuvars.balls = 1
            elif menuvars.selected == 5:
                clickSfx.play()
                sys.exit()
        if button == 3:
            if menuvars.selected == 1:
                clickSfx.play()
                menuvars.points -= 1
                if menuvars.points < 1:
                    menuvars.points = 24
            elif menuvars.selected == 4:
                clickSfx.play()
                menuvars.balls -= 1
                if menuvars.balls < 1:
                    menuvars.balls = 10

def mousemoved(pos,rel,buttns):
    mx = pos[0]
    my = pos[1]
    if not menuvars.titlescreen:
        menuvars.selected = -1
        i = 0
        for b in buttons:
            x = b[1]
            y = b[2]
            w = b[3]
            h = b[4]
            if mx > x and mx < (x+w) and my > y and my < (y+h):
                menuvars.selected = i
            i+=1

def quit():
    print("Exiting from menu")

# EOF
