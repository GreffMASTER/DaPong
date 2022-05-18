import pygame
import stateman as state
from fontman import fonts

class settings:
    timer = 0
    resmsg = ""
    screen = None
    res = (720,420)

def init(scrn,sett=None):
    settings.timer = 0
    settings.resmsg = sett
    settings.screen = scrn
    settings.res = scrn.get_size()

def update(dt,clock):
    settings.timer += dt

def draw(screen):
    text = fonts["medfont"].render(settings.resmsg, True, (255,255,255))
    offset = (text.get_size()[0]/2,text.get_size()[1]/2)
    pos = ((settings.res[0]/2)-offset[0],(settings.res[1]/2)-offset[1])
    screen.blit(text,pos)
    text = fonts["fpsfont"].render("Press any key to continue.", True, (255,255,255))
    offset = (text.get_size()[0]/2,text.get_size()[1]/2)
    pos = ((settings.res[0]/2)-offset[0],(settings.res[1]/2)-offset[1]+60)
    screen.blit(text,pos)

def keypressed(key,mod):
    if settings.timer > 1:
        state.change("menu",settings.screen)

def mbuttonreleased(pos,button):
    if settings.timer > 1:
        state.change("menu",settings.screen)
