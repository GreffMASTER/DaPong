print("Adding Menu State...")

import stateman as state
import dapong
from fontman import fonts

pygame = state.pygame

screen = None
titlescreen = True

def init(scrn,sett=None):
    print("DaPong v."+dapong.version)
    global screen
    screen = scrn
    state.printMsg("Initiating Menu State...",3)
    print("Initiating Menu State")

def update(dt,clock):
    pass

def draw(screen):
    size = screen.get_size()
    if titlescreen:
        text = fonts["scorefont"].render("DaPong", True, (255,255,255))
        text2 = fonts["fpsfont"].render("Insert coin or press Enter.", True, (255,255,255))
        vertext = fonts["fpsfont"].render("v."+dapong.version, True, (255,255,255))

        offset = (text.get_size()[0]/2,text.get_size()[1]/2)
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])
        screen.blit(text,pos)

        offset = (text2.get_size()[0]/2,text2.get_size()[1]/2)
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])
        screen.blit(text2,(pos[0]+10,pos[1]+70))
        screen.blit(vertext,(5,size[1]-25))
    else:
        text = fonts["scorefont"].render("Mode", True, (255,255,255))
        info = "Press 1 for Singlepayer - Press 2 for Multiplayer"
        text2 = fonts["fpsfont"].render(info, True, (255,255,255))
        controls = "Controls: P1 - W,S  P2 - UP,DOWN  Show FPS - F1  Screenshot - F10"
        contrltext = fonts["fpsfont"].render(controls, True, (255,255,255))

        offset = (text.get_size()[0]/2,text.get_size()[1]/2)
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])
        screen.blit(text,pos)

        offset = (text2.get_size()[0]/2,text2.get_size()[1]/2)
        pos = ((size[0]/2)-offset[0],(size[1]/2)-offset[1])
        screen.blit(text2,(pos[0]+10,pos[1]+70))
        screen.blit(contrltext,(5,size[1]-25))

def keypressed(key,mod):
    global titlescreen
    if titlescreen:
        if key == pygame.K_RETURN:
            titlescreen = False
    else:
        if key == pygame.K_1:
            state.change("game",screen,{"ai":True})
        if key == pygame.K_2:
            state.change("game",screen)

def keyreleased(key,mod):
    pass

def mousemoved(pos,rel,buttons):
    pass

def mbuttonreleased(pos,button):
    pass

def mbuttonpressed(pos,button):
    pass
    
def quit():
    pass

# EOF
