import random,pygame

class ball:
    def __init__(self,spd=40):
        self.__pos = (200,200)
        self.__accel = (0,0)
        self.__speed = 0
        self.__size = 20
        self.__speed = spd
        self.__prevpos = [self.__pos,self.__pos,self.__pos]

    def move(self,dt):
        self.__prevpos[2] = self.__prevpos[1]
        self.__prevpos[1] = self.__prevpos[0]
        self.__prevpos[0] = self.__pos
            
        multi = dt * self.__speed
        acx = self.__pos[0] + self.__accel[0] * multi
        acy = self.__pos[1] + self.__accel[1] * multi
        self.__pos = ( acx, acy )

    def logicFCCheck(self,res):
        if self.__pos[1]+self.__size >= res[1]:
            self.__accel = (self.__accel[0],-abs(self.__accel[1]))
            return True

        if self.__pos[1]-self.__size <= 0:
            self.__accel = (self.__accel[0],abs(self.__accel[1]))
            return True

    def logicOOBCheck(self,res):
        if self.__pos[0] <= 0:
            return 1
        if self.__pos[0] >= res[0]:
            return 0

    def logicLeftPaddleBounce(self,res,pad):
        if self.__pos[0]-self.__size < 50 and self.__pos[0]+self.__size > 25:
            if self.__pos[1] < pad.getPos()[1]+pad.getWH()[1]+(self.__size/2) and self.__pos[1] > pad.getPos()[1]-(self.__size/2):
                if self.__accel[0] < 0:
                    self.__accel = ( abs(self.__accel[0]),self.__accel[1])
                    self.__accel = ( self.__accel[0]+0.25,self.__accel[1])
                    self.__accel = ( self.__accel[0],self.__accel[1]+pad.getAcc()/2)

                    if self.__accel[1] >= 8 or self.__accel[1] <= -8:
                        self.__accel = (self.__accel[0],self.__accel[1]/2)
                    return True

    def logicRightPaddleBounce(self,res,pad):
        if self.__pos[0]+self.__size > res[0]-50 and self.__pos[0]-self.__size < res[0]-25:
            if self.__pos[1] < pad.getPos()[1]+pad.getWH()[1]+(self.__size/2) and self.__pos[1] > pad.getPos()[1]-(self.__size/2):
                if self.__accel[0] > 0:
                    self.__accel = ( -abs(self.__accel[0]),self.__accel[1])
                    self.__accel = ( self.__accel[0]-0.25,self.__accel[1])
                    self.__accel = ( self.__accel[0],self.__accel[1]+pad.getAcc()/2)

                    if self.__accel[1] >= 8 or self.__accel[1] <= -8:
                        self.__accel = (self.__accel[0],self.__accel[1]/2)
                    return True

    def draw(self,surface):
        totalspeed = abs(self.__accel[0])+abs(self.__accel[1])
        if totalspeed > 20:
            pygame.draw.circle(surface,(255,255,255,32), self.__prevpos[2], self.__size)
        if totalspeed > 15:
            pygame.draw.circle(surface,(255,255,255,64), self.__prevpos[1], self.__size)
        if totalspeed > 10:
            pygame.draw.circle(surface,(255,255,255,128),self.__prevpos[0], self.__size)

        pygame.draw.circle(surface,(255,255,255,255),    self.__pos,        self.__size)

    def setPos(self,x,y):
        self.__pos = (x,y)

    def getPos(self):
        return self.__pos

    def setAcc(self,x,y):
        if x == None:
            self.__accel = (self.__accel[0],y)
        elif y == None:
            self.__accel = (x,self.__accel[1])
        else:
            self.__accel = (x,y)

    def getAcc(self):
        return self.__accel

    def setSize(self,size):
        self.__size = size

    def getSize(self):
        return self.__size

    def reset(self,x,y,direct=None):
        self.__pos = (x,y)
        self.__prevpos = [self.__pos,self.__pos,self.__pos]

        if direct != None:
            direction = dir
        else:
            direction = random.randint(0,1)
        if direction == 1:
            self.__accel = (4,self.__accel[1])
        else:
            self.__accel = (-4,self.__accel[1])
        angle = random.randint(-4,4)
        if angle == 0: angle = 1
        self.__accel = (self.__accel[0],angle)
