class Car:
    def __init__(self,x,y,roadWidth,roadHeight,speed=1,color=(0,0,255),currentElevation=0):
        self.x = x
        self.y = y

        self.roadWidth = roadWidth
        self.roadHeight = roadHeight
        self.speed = speed
        self.color = color

        self.currentElevation = currentElevation