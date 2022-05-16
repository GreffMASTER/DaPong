import pygame

class paddle:
    def __init__(self,x,y,w,h,spd=40,limit=8):
        self.__width = w
        self.__height = h
        self.__accel = 0
        self.__pos = (x,y)
        self.__rect = pygame.Rect(x,y,w,h)
        self.__speed = spd
        self.__limit = limit

    def update(self,dt,res):
        multi = dt * self.__speed

        if self.__accel > self.__limit: self.__accel = self.__limit
        if self.__accel < -self.__limit: self.__accel = -self.__limit

        self.__pos = (self.__pos[0],self.__pos[1]+self.__accel*multi)    # move paddle
        
        if self.__pos[1] <= 0: # limit paddle postion to stay in the screen
            self.__pos = (self.__pos[0],0)
            self.__accel = abs(self.__accel)
        if self.__pos[1]+self.__height >= res[1]:
            self.__pos = (self.__pos[0],res[1]-self.__height)
            self.__accel = -abs(self.__accel)

        self.__accel = self.__accel/(1.15+dt)    # friction for paddle
        self.__rect = pygame.Rect(self.__pos[0],self.__pos[1],self.__width,self.__height)

    def move(self,direction,amount,dt):
        if direction == "up":
            self.__accel -= amount+dt
        if direction == "down":
            self.__accel += amount+dt

    def getAcc(self):
        return self.__accel

    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.__rect)

    def getWH(self):
        return (self.__width,self.__height)

    def getPos(self):
        return self.__pos
