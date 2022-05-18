# State Manager (stateman) Luke Lasok 2022

# The state manager works by assigning imported modules to a "curstate" variable.
# That variable is later called to execute hooked functions.
# Add imported modules to the state dictionary and use "change(<state_keyname>)"
# function to change the state.

print("Adding State Manager...")

import sys, pygame, os
import fontman                  # Import the font manager

from fontman import fonts
from datetime import datetime

# Import state modules
import states.menustate as menu      # Import menu state
import states.gamestate as game      # Import game state
import states.resultstate as result # Import result state

states = {      # State dictionary
    "menu":menu,
    "game":game,
    "result":result
}

# Variables
drawfps = False     # If fps counter should be drawn on screen
class message:      # Used to display a message in top left corner of the screen for x amount of time      
    text = ""
    time = 0

# Hooks
curstate = None # Current state hook
screen = None   # Game's main screen
clock = None    # Game's main clock

def change(statestr,scrn,sett=None):          # Change current state
    global curstate
    if statestr in states:
        curstate = states[statestr]
        init(scrn,sett)
    else:
        print("No such state as",statestr)
        sys.exit()

def init(scrn,sett=None):           # Call function to initiate the current state
    if "init" in dir(curstate):
        curstate.init(scrn,sett)

def update(dt,clck):                # Call function to perform logic update in the current state
    global clock, message
    clock = clck
    if message.time>0:
        message.time -= dt

    if curstate and "update" in dir(curstate):
        curstate.update(dt,clck)

    clock.tick(60)

def draw(scrn):                     # Call function to draw on the screen surface in the current state
    global screen
    screen = scrn

    if curstate and "draw" in dir(curstate):
        curstate.draw(scrn)
    if message.time>0:
        msg_text = fonts["infofont"].render(message.text, True, (0, 255, 255))
        scrn.blit(msg_text, (0, 0))
    if drawfps:
        fps_text = fontman.drawFps(fonts["fpsfont"], clock.get_fps())   # Create FPS text surface
        scrn.blit(fps_text, (0, scrn.get_size()[1]-24))                                     # And draw it

def keypressed(key,mod):            # Call function when key is pressed in the current state
    if key == pygame.K_F10:
        takeScreenshot(screen)
    elif key == pygame.K_F1:
        global drawfps
        drawfps = not drawfps

    if curstate and "keypressed" in dir(curstate):
        curstate.keypressed(key, mod)

def keyreleased(key,mod):           # Call function when key is released in the current state
    if curstate and "keyreleased" in dir(curstate):
        curstate.keyreleased(key, mod)

def mousemoved(pos,rel,buttons):    # Call function when mouse has moved in the current state
    if curstate and "mousemoved" in dir(curstate):
        curstate.mousemoved(pos, rel, buttons)

def mbuttonreleased(pos,button):    # Call function when mouse button is released in the current state
    if curstate and "mbuttonreleased" in dir(curstate):
        curstate.mbuttonreleased(pos, button)

def mbuttonpressed(pos,button):     # Call function when mouse button is pressed in the current state
    if curstate and "mbuttonpressed" in dir(curstate):
        curstate.mbuttonpressed(pos, button)

def keydown(keys):                  # Call function when a key is down in the curremt state
    if curstate and "keydown" in dir(curstate):
        curstate.keydown(keys)

def quit():                         # Call function when the game window is closed in the current state
    if curstate and "quit" in dir(curstate):
        curstate.quit()
    sys.exit()

def printMsg(string,time=1):        # Print a message in top left corner of the screen for x amount of time
    message.text = string
    message.time = time

def takeScreenshot(scrn):           # Takes a screenshot of a given screen
    curtime = datetime.now()                                                        # Get current time and date
    datestr = curtime.strftime("%d.%m.%Y_%H-%M-%S")                                 # Format the date and time
    x, y = scrn.get_size()
    rect = pygame.Rect(0, 0, x, y)                                                  # Select entire window
    if not os.path.exists("screenshots"):                                           # If 'screenshots' folder doesn't exist, create it
        os.mkdir("screenshots")
    filename = "DaPongScreenshot_"+datestr+".png"                                   # Prepare filename string
    pygame.image.save(scrn.subsurface(rect), os.path.join("screenshots", filename)) # Save screenshot
    printMsg("Screenshot saved as "+filename,3)                                     # Display message

# EOF
