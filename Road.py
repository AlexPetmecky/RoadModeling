import pygame


class Road:
    def __init__(self,x,y,width=5,height=5,color=(255,255,255)):
        #pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color


        self.inbound = []
        self.outbound = []

        self.rotate_deg = 0
        self.elevation = 0

    def addInbound(self,road):
        self.inbound.append(road)

    def addOutbound(self,road):
        self.outbound.append(road)
