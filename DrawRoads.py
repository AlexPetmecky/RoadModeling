import pygame
import random
import math
from pygame.display import update


class DrawRoads:
    #SCREEN_WIDTH = 640
    #SCREEN_HEIGHT = 480
    def __init__(self,SCREEN_WIDTH=640,SCREEN_HEIGHT=480,refreshRate=1):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.refreshRate = refreshRate


        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #pygame.time.delay(2000)
    def setRoads(self,roads):
        self.roads = roads

        for road in roads:
            #print("DRAWING")
            #r = pygame.Rect((road.x,road.y,road.width,road.height))
            #pygame.draw.rect(self.screen,road.color,r)

            r = pygame.Surface((road.width,road.height),pygame.SRCALPHA)
            r.fill(road.color)

            #angle = math.degrees(math.atan2(road.width,road.height))
            #rotated= pygame.transform.rotate(r,20)
            #r = pygame.transform.rotate(r,100)

            r = pygame.transform.rotate(r, road.rotate_deg)
            #rect = rotated_surface.get_rect(center=(100, 100))


            self.screen.blit(r,(road.x,road.y))
           # pygame.draw.rect(self.screen,road.color,r)

        pygame.display.update()
        #pygame.display.flip()
        #print(self.roads.nodes(data=True))


    def setCars(self,cars=[]):
        self.cars = cars
        #for x,y in self.roads.nodes()(data=True):
        #    print(x,y)
        for car in cars:
            #print(car.x,car.y)
            carNodes = [x for x, y in self.roads.nodes(data=True) if y['x'] == car.x and y['y'] == car.y]
            #print(carNodes)
            for road in carNodes:
                road.color = car.color
                #road.color = (0,0,255)
        self.setRoads(self.roads)

    def updateCars(self):
        for car in self.cars:
            try:
                carNodes = [x for x, y in self.roads.nodes(data=True) if y['x'] == car.x and y['y'] == car.y]
                #print(carNodes)
                #print("Possible Nodes: ",carNodes)
                road = carNodes[0]
                #print(road)
                nextRoads = list(self.roads.successors(road))
                print("Possible roads: ",nextRoads)
                nextRoad = random.choice(nextRoads)
                if nextRoad.color == nextRoad.origionalColor:
                    #road.color = (255,255,255)
                    road.color = road.origionalColor
                    nextRoad.color = car.color
                    #nextRoad.color = (0,0,255)
                    #car.x+=10#NEEDS TO BE CHANGED
                    car.x = nextRoad.x
                    car.y = nextRoad.y
                print("MOVING")
            except:
                print("NOT MOVING")
                pass
            #self.roads.
        self.setRoads(self.roads)


    def render(self):
        run  = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            try:
                self.update()
            except:
                pass


        pygame.quit()

    def update(self):

        #self.setRoads()
        self.updateCars()
        pygame.display.update()
        self.clock.tick(self.refreshRate)