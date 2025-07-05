import pygame


class Road:
    def __init__(self,x,y,width=5,height=5,color=(255,255,255),origionalColor = (255,255,255),elevation = 0):
        #pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (color[0]-elevation,color[1]-elevation,color[2]-elevation)
        self.origionalColor = origionalColor


        self.inbound = []
        self.outbound = []

        self.rotate_deg = 0
        self.elevation = elevation

    def addInbound(self,road):
        self.inbound.append(road)

    def addOutbound(self,road):
        self.outbound.append(road)
