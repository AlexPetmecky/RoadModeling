import pygame

from DrawRoads import DrawRoads
from Road import Road
from Car import Car
from BuildRoadNetwork import BuildRoadNetwork

ROAD_WIDTH = 10
ROAD_HEIGHT = 10

if __name__ == '__main__':


    dr = DrawRoads(refreshRate=5)
    BuildRN = BuildRoadNetwork()

    #road1 = Road(10,10)
    #r_list = [road1]
    #dr.setRoads(r_list)
    #roads = BuildRN.makeSegment(10,10,"E",10,ROAD_WIDTH,ROAD_HEIGHT,True)
    #roads = BuildRN.make_arc(x0=100,y0=200,radius=100,num_points=10,angle=90,j=100,k=100)#r=0,num_points=0,angle=0,j=0,k=0
    roads = BuildRN.make(ROAD_WIDTH,ROAD_HEIGHT)
    print(roads.edges())
    dr.setRoads(roads)

    car = Car(10,10,ROAD_WIDTH,ROAD_HEIGHT,color=(255,0,0))
    car2 = Car(20,10,ROAD_WIDTH,ROAD_HEIGHT)
    car3 = Car(50, 10, ROAD_WIDTH, ROAD_HEIGHT)

    cars = [car,car2,car3]
    dr.setCars(cars)


    dr.render()