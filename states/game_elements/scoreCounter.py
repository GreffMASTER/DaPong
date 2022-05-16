class scoreCounter:
    def __init__(self,winfunc=None,players=2,maxs=8):
        self.__players = players
        self.__maxscore = maxs
        self.__scores = []
        self.__winfunc = winfunc
        for i in range(0,players):
            self.__scores.append(0)

    def reset(self):
        for i in range(0,self.__players):
            self.__scores[i] = 0

    def setMaxScore(self,value):
        print("Setting to",value,"points")
        self.__maxscore = value
    
    def addPoints(self,plyrindx,amount=1):
        self.__scores[plyrindx] += amount
        if self.__scores[plyrindx] >= self.__maxscore:
            if self.__winfunc: self.__winfunc(plyrindx)

    def removePoints(self,plyrindx,amount=1):
        self.__scores[plyrindx] -= amount

    def getScore(self,plyrindx):
        return self.__scores[plyrindx]

    def getScores(self):
        return self.__scores

    def setScore(self,plyrindx,value):
        self.__scores[plyrindx] = value
