print("Adding Game State...")

# Imports

import stateman as state
import audioman as audio
import math, os, random, pygame

from fontman import fonts
from states.game_elements.ball import ball
from states.game_elements.paddle import paddle
from states.game_elements.scoreCounter import scoreCounter

# Variables
class set:
    delta = 0           # Delta time
    screen = None       # Game's main screen
    res = (720,420)     # Window resolution 720,420
    counter = 0         # State counter
    xpos = 250          # Score text x position
    ypos = 200          # Score text y position
    ai = False          # AI mode bool
    aidif = 1           # AI difficulty level
    balls = []          # Ball list
    demo = False        # Demo mode bool
    ballcount = 1       # Ball count
    debug = False       # Debug mode bool
    p1ai = False        # Player 1 AI mode bool

def win(plyrindx):
    message = ""
    if plyrindx == 0:
        message = "Player 1 Wins!"
    elif plyrindx == 1:
        if set.ai:
            message = "CPU Wins!"
        else:
            message = "Player 2 Wins!"
    print(message)
    deleteAllBalls()
    state.change("result",set.screen,message)


def addBall(i=None):
    set.balls.append(ball())
    if i:
        direct = i%2
        set.balls[len(set.balls)-1].reset(set.res[0]/2,set.res[1]/2,direct)
    else:
        set.balls[len(set.balls)-1].reset(set.res[0]/2,set.res[1]/2)

def deleteAllBalls():
    for ball in set.balls:
        del ball
        
# Create main game objects

gamescore = scoreCounter(win,2,8)
paddleleft = paddle(25,160,25,100)
paddleright = paddle(set.res[0]-50,160,25,100)


# Functions

def init(scrn,sett=None):
    # Reset all variables
    paddleleft.reset(25,160)
    paddleright.reset(set.res[0]-50,160)
    set.counter = 0
    set.ai = False
    set.demo = False
    set.ballcount = False
    set.p1ai = False
    if sett:
        if "points" in sett:
            gamescore.setMaxScore(sett["points"])   # Change max score
        if "ai" in sett:
            set.ai = sett["ai"]                     # Enable AI
        if "aidif" in sett:
            set.aidif = sett["aidif"]               # Set AI difficulty
        if "demo" in sett:
            set.demo = sett["demo"]                 # Enable demo mode
        if "ballcount" in sett:
            set.ballcount = sett["ballcount"]       # Set amount of balls
        if "debug" in sett:
            set.debug = sett["debug"]               # Enable debug mode
            if set.debug == True:
                state.printMsg("Debug mode enabled",3)

    set.screen = scrn
    set.res = scrn.get_size()
    set.xpos = set.res[0]/2
    set.ypos = set.res[1]/2

    gamescore.reset()
    set.balls = []
    
    for i in range(0,set.ballcount):
        addBall()
    
    for ball in set.balls:
        ball.reset( set.res[0]/2, set.res[1]/2 )



def update(dt,clock):
    set.delta = dt
    # Paddle physcis
    paddleleft.update(dt,set.res)
    paddleright.update(dt,set.res)

    if set.ai:
        for ball in set.balls:

            for j,b in enumerate(set.balls):
                if b.getPos()[0] > ball.getPos()[0] and b.getAcc()[0] > 0:
                    ball = b

            if ball.getAcc()[0] > 0:
                if ball.getPos()[1] < paddleright.getPos()[1]+paddleright.getWH()[1]/2:
                    paddleright.move("up",set.aidif,dt)
                if ball.getPos()[1] > paddleright.getPos()[1]+paddleright.getWH()[1]/2:
                    paddleright.move("down",set.aidif,dt)

        if set.demo or set.p1ai:
            for ball in set.balls:
                for j,b in enumerate(set.balls):
                    if b.getPos()[0] < ball.getPos()[0] and b.getAcc()[0] < 0:
                        ball = b

                if ball.getAcc()[0] < 0:
                    if ball.getPos()[1] < paddleleft.getPos()[1]+paddleleft.getWH()[1]/2:
                        paddleleft.move("up",set.aidif,dt)
                    if ball.getPos()[1] > paddleleft.getPos()[1]+paddleleft.getWH()[1]/2:
                        paddleleft.move("down",set.aidif,dt)
                
    # Ball physics
    for gameball in set.balls:  # Do for each ball in the list

        gameball.move(dt)       # Move ball

        if gameball.logicFCCheck(set.res):  # Floor/Ceiling collisions
            audio.play("wallBncSfx")

        oobcheck = gameball.logicOOBCheck(set.res)  # Out of bounds check

        if oobcheck != None:                # If is out of bounds
            gamescore.addPoints(oobcheck)   # Give a point for a player
            audio.play("scoreSfx")
            gameball.reset(set.res[0]/2, set.res[1]/2, oobcheck)    # Reset ball

        # Ball and paddles interaction

        if gameball.logicLeftPaddleBounce(set.res,paddleleft):
            audio.play("paddBncSfx")
        if gameball.logicRightPaddleBounce(set.res,paddleright):
            audio.play("paddBncSfx")

    set.counter+=dt                     # Increment state counter

    # Move score text in circles
    set.ypos = set.ypos - math.sin(set.counter)
    set.xpos = set.xpos + math.cos(set.counter)

    # END OF UPDATE

def draw(screen):
    # Score text
    scorestring = str(gamescore.getScore(0)) + ":" + str(gamescore.getScore(1))
    scoretext = fonts["scorefont"].render( scorestring , True, (45,45,45))
    scorsize = scoretext.get_size()
    k = (set.xpos-scorsize[0]/2,set.ypos-scorsize[1]/8)
    screen.blit(scoretext,k)        # Draw score counter

    ballsurface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for gameball in set.balls:      # For each ball in the list
        gameball.draw(ballsurface)  # Draw game ball onto the surface
    screen.blit(ballsurface,(0,0))  # Draw surface with all the balls

    paddleleft.draw(screen)         # Draw left paddle
    paddleright.draw(screen)        # Draw right paddle

    if set.demo:    # Draw demo text
        demotext = fonts["medfont"].render( "DEMO" , True, (255,255,255))
        demotext2 = fonts["fpsfont"].render( "Press ESC to return." , True, (255,255,255))
        screen.blit(demotext,(6,6))
        screen.blit(demotext2,(6,76))

def keypressed(key,mod):
    if key == pygame.K_ESCAPE:
        deleteAllBalls()
        state.change("menu",set.screen)

    if set.debug:
        if key == pygame.K_k:
            addBall()
            state.printMsg("Added new ball")
        if key == pygame.K_i:
            set.p1ai = not set.p1ai
            if set.p1ai == True:
                state.printMsg("Player 1 AI enabled")
            else:
                state.printMsg("Player 1 AI disabled")
        
def keydown(keys):
    if keys[pygame.K_s]:
        paddleleft.move("down",2,set.delta) # Move left paddle down

    if keys[pygame.K_w]:
        paddleleft.move("up",2,set.delta)   # Move left paddle up
        
    if set.ai == False:                     # Only if AI is disabled
        if keys[pygame.K_DOWN]:
            paddleright.move("down",2,set.delta) # Move right paddle down

        if keys[pygame.K_UP]:
            paddleright.move("up",2,set.delta)   # Move right paddle up

# EOF
