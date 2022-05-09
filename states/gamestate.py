print("Adding Game State...")

# Imports

import stateman as state
import math, os, random
from fontman import fonts

pygame = state.pygame   # Get pygame module from state manager

# Variables

delta = 0               # Delta time
screen = None           # Game's main screen
res = None              # Window resolution

score = {
    "p1":0,
    "p2":0
}

ballacc = {
    "x":3,
    "y":1.5
}

ballpos = {
    "x":200.0,
    "y":200.0
}

paddle1 = {
    "pos":160,
    "acc":0,
    "rect":pygame.Rect(25,25,25,100)
}

paddle2 = {
    "pos":160,
    "acc":0,
    "rect":pygame.Rect(125,25,25,100)
}
counter = 0
xpos = 250
ypos = 200

ai = False
offset = 100

# Functions

def init(scrn,sett=None):
    global counter,xpos,ypos,ballpos,ballacc,screen,res,paddle1,paddle2,score,ai
    global scoreSfx
    global wallBncSfx
    global paddBncSfx
    
    state.printMsg("Initiating Game State...",3)
    print("Initiating Game State")
    counter = 0
    ai = False
    if sett:
        if "ai" in sett:
            ai = sett["ai"]

    screen = scrn
    res = scrn.get_size()
    
    scoreSfx = pygame.mixer.Sound(os.path.join("sounds", "score.wav"))      # Load score sound effect
    wallBncSfx = pygame.mixer.Sound(os.path.join("sounds", "wallBnc.wav"))  # Load wall bounce sound effect
    paddBncSfx = pygame.mixer.Sound(os.path.join("sounds", "paddBnc.wav"))  # Load paddle bounce sound effect
    
    xpos = res[0]/2
    ypos = res[1]/2
    score = {
        "p1":0,
        "p2":0
    }

    paddle1 = {
        "pos":160,
        "acc":0,
        "rect":pygame.Rect(25,25,25,100)
    }

    paddle2 = {
        "pos":160,
        "acc":0,
        "rect":pygame.Rect(125,25,25,100)
    }
    
    resetBall()

def update(dt,clock):
    global counter, ypos, xpos, ballpos, ballacc, paddle1, paddle2, delta
    delta = dt
    # Paddle physcis
    speed = dt * 40

    if paddle1["acc"] > 8: paddle1["acc"] = 8
    if paddle1["acc"] < -8: paddle1["acc"] = -8

    if paddle2["acc"] > 8: paddle2["acc"] = 8
    if paddle2["acc"] < -8: paddle2["acc"] = -8
    
    paddle1["pos"] += paddle1["acc"]*speed    # move paddle 1
    paddle2["pos"] += paddle2["acc"]*speed    # move paddle 2    

    if paddle1["pos"] <= 0: # limit paddle 1 postion to stay in the screen
        paddle1["pos"] = 0
        paddle1["acc"] = abs(paddle1["acc"])
    if paddle1["pos"]+100 >= res[1]:
        paddle1["pos"] = res[1]-100
        paddle1["acc"] = -abs(paddle1["acc"])

    if paddle2["pos"] <= 0: # limit paddle 2 postion to stay in the screen
        paddle2["pos"] = 0
        paddle2["acc"] = abs(paddle2["acc"])
    if paddle2["pos"]+100 >= res[1]:
        paddle2["pos"] = res[1]-100
        paddle2["acc"] = -abs(paddle2["acc"])

    if ai:
        if ballpos["x"] > res[0]/4:
            if ballpos["y"] < paddle2["pos"]+50:
                paddle2["acc"] -= 1+dt
            if ballpos["y"] > paddle2["pos"]+50:
                paddle2["acc"] += 1+dt
                
    paddle1["acc"] = paddle1["acc"]/(1.15+dt)    # friction for paddle 1
    paddle2["acc"] = paddle2["acc"]/(1.15+dt)    # friction for paddle 2

    paddle1["rect"] = pygame.Rect(25,paddle1["pos"],25,100)
    paddle2["rect"] = pygame.Rect(res[0]-50,paddle2["pos"],25,100)

    # Ball physics
    ballpos["x"] += ballacc["x"]*speed
    ballpos["y"] += ballacc["y"]*speed

    if ballpos["x"] >= res[0]:  # if ball hits the right wall
        score["p1"] += 1
        scoreSfx.play()
        resetBall()

    if ballpos["x"] <= 0:       # if ball hits the left wall
        score["p2"] += 1
        scoreSfx.play()
        resetBall()


    if ballpos["y"]+20 >= res[1]:   # bounce ball off the floor
        ballacc["y"] = -abs(ballacc["y"])
        wallBncSfx.play()

    if ballpos["y"]-20 <= 0:        # bounce ball off the ceiling
        ballacc["y"] = abs(ballacc["y"])
        wallBncSfx.play()

    # BALL AND PADDLE INTERACTIONS
    # The paddle collision is a little bit wider to give more room to hit the ball
    
    if ballpos["x"]-20 < 50 and ballpos["x"] > 25:                                  # If ball reached the left paddle
        if ballpos["y"] < paddle1["pos"]+110 and ballpos["y"] > paddle1["pos"]-10:  # If ball is in range of paddle width
            if ballacc["x"] < 0:                                                    # Only if ball is going towards the paddle
                ballacc["x"] = abs(ballacc["x"])                # Reverse x acceleration
                ballacc["x"] += 0.25                            # Increase ball speed
                ballacc["y"] = ballacc["y"]+paddle1["acc"]/2    # Influence ball y momentum with paddle's momentum
                if ballacc["y"] >= 8 or ballacc["y"] <= -8:     # If ball is going too fast on y axis
                    ballacc["y"] /= 2                           # Slow it down
                paddBncSfx.play()                               # Play sound effect

    if ballpos["x"]+20 > res[0]-50 and ballpos["x"] < res[0]-25:                    # If ball reached the right paddle
        if ballpos["y"] < paddle2["pos"]+110 and ballpos["y"] > paddle2["pos"]-10:  # If ball is in range of paddle width
            if ballacc["x"] > 0:                                                    # Only if ball is going towards the paddle
                ballacc["x"] = -abs(ballacc["x"])               # Reverse x acceleration
                ballacc["x"] -= 0.25                            # Increase ball speed
                ballacc["y"] = ballacc["y"]+paddle2["acc"]/2    # Influence ball y momentum with paddle's momentum
                if ballacc["y"] >= 8 or ballacc["y"] <= -8:     # If ball is going too fast on y axis
                    ballacc["y"] /= 2                           # Slow it down
                paddBncSfx.play()                               # Play sound effect

    counter+=dt                     # Increment state counter
    # Move in circles
    ypos = ypos - math.sin(counter)
    xpos = xpos + math.cos(counter)

    # END OF UPDATE

def draw(screen):
    scorestring = str(score["p1"]) + ":" + str(score["p2"])
    scoretext = fonts["scorefont"].render( scorestring , True, (45,45,45))

    scorsize = scoretext.get_size()
    k = (xpos-scorsize[0]/2,ypos-scorsize[1]/8)
    
    screen.blit(scoretext,k)    # Draw score counter
    
    pygame.draw.circle(screen,(255,255,255),(ballpos["x"],ballpos["y"]),20) # Draw ball
    pygame.draw.rect(screen,(255,255,255),paddle1["rect"])                  # Draw left paddle
    pygame.draw.rect(screen,(255,255,255),paddle2["rect"])                  # Draw right paddle

def keypressed(key,mod):
    if key == pygame.K_ESCAPE:
        state.change("menu",screen)
        
def keydown(keys):
    global paddle1, paddle2

    if keys[pygame.K_s]:
        paddle1["acc"] += 2+delta       # Move left paddle down

    if keys[pygame.K_w]:
        paddle1["acc"] -= 2+delta       # Move left paddle up
        
    if ai == False:                     # Only if AI is disabled
        if keys[pygame.K_DOWN]:
            paddle2["acc"] += 2+delta   # Move right paddle down

        if keys[pygame.K_UP]:
            paddle2["acc"] -= 2+delta   # Move right paddle up
    
# Other functions

def resetBall():
    global ballpos, ballacc
    ballpos["x"] = res[0]/2
    ballpos["y"] = res[1]/2
    direction = random.randint(0,1)
    if direction == 1:
        ballacc["x"] = 4
    else:
        ballacc["x"] = -4
    ballacc["y"] = random.randint(-2,2)
    if ballacc["y"] == 0: ballacc["y"] = 1

# EOF
