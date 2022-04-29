print("Adding Game State...")

import stateman as state
import math, os, random
from fontman import fonts

screen = None
res = None

pygame = state.pygame
counter = 0
delta = 0

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

xpos = 250
ypos = 200

ai = False
offset = 100

def init(scrn,sett=None):
    global counter,xpos,ypos,ballpos,ballacc,screen,res,paddle1,paddle2,score,ai
    ai = False
    if sett:
        if "ai" in sett:
            ai = sett["ai"]

    screen = scrn
    res = scrn.get_size()
    state.printMsg("Initiating Game State...",3)
    print("Initiating Game State")
    counter = 0
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
        #if ballpos["x"] < res[0]/4*3:
        #    if ballpos["y"] < paddle1["pos"]+50:
        #        paddle1["acc"] -= 3+dt
        #    if ballpos["y"] > paddle1["pos"]+50:
        #        paddle1["acc"] += 3+dt

    paddle1["acc"] = paddle1["acc"]/(1.15+dt)    # friction for paddle 1
    paddle2["acc"] = paddle2["acc"]/(1.15+dt)    # friction for paddle 2

    paddle1["rect"] = pygame.Rect(25,paddle1["pos"],25,100)
    paddle2["rect"] = pygame.Rect(res[0]-50,paddle2["pos"],25,100)

    # Ball physics
    ballpos["x"] += ballacc["x"]*speed
    ballpos["y"] += ballacc["y"]*speed

    if ballpos["x"] >= res[0]:  # if ball hits the right wall
        score["p1"] += 1
        resetBall()

    if ballpos["x"] <= 0:       # if ball hits the left wall
        score["p2"] += 1
        resetBall()


    if ballpos["y"]+20 >= res[1]:   # bounce ball off the floor
        ballacc["y"] = -abs(ballacc["y"])

    if ballpos["y"]-20 <= 0:        # bounce ball off the ceiling
        ballacc["y"] = abs(ballacc["y"])


    if ballpos["x"]-20 < 50 and ballpos["x"] > 25:  # bounce ball off the left paddle
        if ballpos["y"] < paddle1["pos"]+100 and ballpos["y"] > paddle1["pos"]:
            if ballacc["x"] < 0:
                ballacc["y"] = ballacc["y"]+paddle1["acc"]/2
                if ballacc["y"] >= 8 or ballacc["y"] <= -8:
                    ballacc["y"] /= 2
                ballacc["x"] = abs(ballacc["x"])    # reverse x acceleration
                ballacc["x"] += 0.1

    if ballpos["x"]+20 > res[0]-50 and ballpos["x"] < res[0]-25:  # bounce ball off the right paddle
        if ballpos["y"] < paddle2["pos"]+100 and ballpos["y"] > paddle2["pos"]:
            if ballacc["x"] > 0:
                ballacc["y"] = ballacc["y"]+paddle2["acc"]/2
                if ballacc["y"] >= 8 or ballacc["y"] <= -8:
                    ballacc["y"] /= 2
                ballacc["x"] = -abs(ballacc["x"])    # reverse x acceleration
                ballacc["x"] -= 0.1


    counter+=dt

    ypos = ypos - math.sin(counter)
    xpos = xpos + math.cos(counter)
    
    #if counter > 6.25:
    #    counter = 0
# END OF UPDATE

def draw(screen):
    scorestring = str(score["p1"]) + ":" + str(score["p2"])
    scoretext = fonts["scorefont"].render( scorestring , True, (45,45,45))

    scorsize = scoretext.get_size()
    scorpos = (res[0]/2-scorsize[0]/2,res[1]/2-scorsize[1]/2)
    k = (xpos-scorsize[0]/2,ypos-scorsize[1]/8)
    scorpos += k
    screen.blit(scoretext,k)
    pygame.draw.circle(screen,(255,255,255),(ballpos["x"],ballpos["y"]),20)
    pygame.draw.rect(screen,(255,255,255),paddle1["rect"])
    pygame.draw.rect(screen,(255,255,255),paddle2["rect"])
    #text = fonts["fpsfont"].render("Game State!", True, (0,255,0))
    #screen.blit(text,(xpos,ypos))

def keypressed(key,mod):

    if key == pygame.K_ESCAPE:
        state.change("menu",screen)
        

def keyreleased(key,mod):
    pass

def mousemoved(pos,rel,buttons):
    pass

def mbuttonreleased(pos,button):
    pass

def mbuttonpressed(pos,button):
    pass

def keydown(keys):
    global paddle1, paddle2

    if keys[pygame.K_s]:
        paddle1["acc"] += 2+delta

    if keys[pygame.K_w]:
        paddle1["acc"] -= 2+delta

    if keys[pygame.K_DOWN]:
        paddle2["acc"] += 2+delta

    if keys[pygame.K_UP]:
        paddle2["acc"] -= 2+delta

def quit():
    pass

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
