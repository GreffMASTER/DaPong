print("Adding Game State...")

# Imports

import stateman as state
import math, os, random, pygame

from fontman import fonts
from states.game_elements.ball import ball
from states.game_elements.paddle import paddle
from states.game_elements.scoreCounter import scoreCounter

# Variables
class set:
    delta = 0               # Delta time
    screen = None           # Game's main screen
    res = (720,420)              # Window resolution 720,420
    counter = 0
    xpos = 250
    ypos = 200
    ai = False
    aidif = 1
    balls = []

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
    state.change("result",set.screen,message)

def addBall():
    set.balls.append(ball())
    set.balls[len(set.balls)-1].reset(set.res[0]/2,set.res[1]/2)

gamescore = scoreCounter(win,2,8)
set.balls.append(ball())
paddleleft = paddle(25,160,25,100)
paddleright = paddle(set.res[0]-50,160,25,100)

# Functions

def init(scrn,sett=None):
    global scoreSfx
    global wallBncSfx
    global paddBncSfx
    print("Initiating Game State")
    set.counter = 0
    set.ai = False
    if sett:
        if "points" in sett:
            gamescore.setMaxScore(sett["points"])
        if "ai" in sett:
            set.ai = sett["ai"]
        if "aidif" in sett:
            set.aidif = sett["aidif"]

    set.screen = scrn
    set.res = scrn.get_size()

    scoreSfx = pygame.mixer.Sound(os.path.join("sounds", "score.wav"))      # Load score sound effect
    wallBncSfx = pygame.mixer.Sound(os.path.join("sounds", "wallBnc.wav"))  # Load wall bounce sound effect
    paddBncSfx = pygame.mixer.Sound(os.path.join("sounds", "paddBnc.wav"))  # Load paddle bounce sound effect
    
    set.xpos = set.res[0]/2
    set.ypos = set.res[1]/2

    gamescore.reset()
    set.balls = []
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
            
            if ball.getPos()[0] > set.res[0]/4 and ball.getAcc()[0] > 0:
                if ball.getPos()[1] < paddleright.getPos()[1]+50:
                    paddleright.move("up",set.aidif,dt)
                if ball.getPos()[1] > paddleright.getPos()[1]+50:
                    paddleright.move("down",set.aidif,dt)
                
    # Ball physics
    for gameball in set.balls:
        gameball.move(dt)

        if gameball.logicFCCheck(set.res):
            wallBncSfx.play()

        oobcheck = gameball.logicOOBCheck(set.res)
        if oobcheck != None:
            gamescore.addPoints(oobcheck)
            scoreSfx.play()
            gameball.reset(set.res[0]/2, set.res[1]/2, oobcheck)

        # BALL AND PADDLE INTERACTIONS

        if gameball.logicLeftPaddleBounce(set.res,paddleleft): paddBncSfx.play()
        if gameball.logicRightPaddleBounce(set.res,paddleright): paddBncSfx.play()

    set.counter+=dt                     # Increment state counter
    # Move in circles
    set.ypos = set.ypos - math.sin(set.counter)
    set.xpos = set.xpos + math.cos(set.counter)

    # END OF UPDATE

def draw(screen):
    scorestring = str(gamescore.getScore(0)) + ":" + str(gamescore.getScore(1))
    scoretext = fonts["scorefont"].render( scorestring , True, (45,45,45))
    scorsize = scoretext.get_size()
    k = (set.xpos-scorsize[0]/2,set.ypos-scorsize[1]/8)
    
    screen.blit(scoretext,k)    # Draw score counter
    for gameball in set.balls:
        gameball.draw(screen)       # Draw game ball

    paddleleft.draw(screen)     # Draw left paddle
    paddleright.draw(screen)    # Draw right paddle

def keypressed(key,mod):
    if key == pygame.K_ESCAPE:
        state.change("menu",set.screen)

    if key == pygame.K_k:
        addBall()
        
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
