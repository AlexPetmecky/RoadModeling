from networkx.algorithms.cuts import normalized_cut_size
from networkx.algorithms.distance_measures import radius

from Road import Road
import networkx as nx
import math
from RoadDataObjects.LineSegment import LineSegment
from RoadDataObjects.CurveData import CurveData



def Make_EAST(x,y,roadWidth,roadHeight):
    return x+roadWidth,y
def Make_WEST(x,y,roadWidth,roadHeight):
    return x-roadWidth,y
def Make_NORTH(x,y,roadWidth,roadHeight):
    return x, y-roadHeight
def Make_SOUTH(x,y,roadWidth,roadHeight):
    return x, y + roadHeight


class BuildRoadNetwork:
    #RoadNetwork = {}
    RoadNetwork = nx.DiGraph()
    action_functions = {"E":Make_EAST, "W":Make_WEST, "N":Make_NORTH, "S":Make_SOUTH}
    parallelActionFunctions = {"E":Make_SOUTH,"W":Make_SOUTH,"N":Make_EAST,"S":Make_EAST}
    def __init__(self):
        pass


    def getArc(self,x0,y0,radius=0,num_points=0,angle=0,width=5,height=5,elevation=0,roadspeed=1):
        roads = []
        w = width
        h = height
        fx = 0
        fy = 1
        lx = 1
        ly = 0

        for t in range(num_points):
            radians = math.radians(angle)
            sub_angle = (t / 10) * radians
            xi = x0 + radius * (math.sin(sub_angle) * fx + (1 - math.cos(sub_angle)) * (-lx))
            yi = y0 + radius * (math.sin(sub_angle) * fy + (1 - math.cos(sub_angle)) * (-ly))
            r = Road(xi, yi, w, h,elevation=elevation,roadSpeed=roadspeed)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=xi, y=yi)
        print("ROADS: ",len(roads))
        return roads

    def setSegment(self,startX = 0,startY=0,direction = "E",segmentNumber = 5,width = 5,height = 5,elevation=0,roadspeed=1):
        direction_function = self.action_functions[direction]
        roads = []
        x = startX
        y = startY
        r = Road(x, y, width, height,elevation=elevation,roadSpeed=roadspeed)
        #roads.append(r)
        roads.append(r)
        self.RoadNetwork.add_node(r, x=x, y=y,elevation=elevation)
        for i in range(segmentNumber - 1):
            x, y = direction_function(x, y, width, height)
            r = Road(x, y, width, height,elevation=elevation,roadSpeed=roadspeed)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=x, y=y,elevation=elevation)
        print("LEN OF ROADS: ", len(roads))
        return roads

        #for i in range(len(roads) - 1):
        #    self.RoadNetwork.add_edge(roads[i], roads[i + 1])
        #    print("Connecting: ", i, " ", i + 1)
        #if wraps:
        #    self.RoadNetwork.add_edge(roads[len(roads) - 1], roads[0])

    def segmentWithElevationChange(self,startX = 0,startY=0,direction = "E",segmentNumber = 5,width = 5,height = 5,elevationStart=0,elevationEnd=0,roadspeed=1):
        #x = x1 + (x2 - x1) * t
        #y = y1 + (y2 - y1) * t


       #elevations = self.getE
        elevations = self.getEquidistantPoints(elevationStart,elevationEnd,segmentNumber)

        #elevationStep = elevationStart+(elevationEnd-elevationStart) * segmentNumber
        #print("Elevation STEP: ", elevationStep)
        direction_function = self.action_functions[direction]
        roads = []
        x = startX
        y = startY
        r = Road(x, y, width, height, elevation=elevations[0],roadSpeed=roadspeed)
        # roads.append(r)
        roads.append(r)
        self.RoadNetwork.add_node(r, x=x, y=y, elevation=elevationStart)
        for i in range(segmentNumber - 1):
            #elevationCurrent = elevationStep * (i+2)

            x, y = direction_function(x, y, width, height)
            r = Road(x, y, width, height, elevation=round(elevations[i+1]),roadSpeed=roadspeed)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=x, y=y, elevation=round(elevations[i+1]))
        print("LEN OF ROADS: ", len(roads))
        return roads


    def arcWithElevationChange(self,x0,y0,radius=0,num_points=0,angle=0,width=5,height=5,elevationStart=0,elevationEnd=0,roadspeed=1,fx=0,fy=1,lx=1,ly=0):
        elevations = self.getEquidistantPoints(elevationStart, elevationEnd, num_points)

        roads = []
        w = width
        h = height
        fx = fx
        fy = fy
        lx = lx
        ly = ly
        points = []

        radians = math.radians(angle)
        for t in range(num_points):

            sub_angle = (t / num_points) * radians
            xi = x0 + radius * (math.sin(sub_angle) * fx + (1 - math.cos(sub_angle)) * (-lx))
            yi = y0 + radius * (math.sin(sub_angle) * fy + (1 - math.cos(sub_angle)) * (-ly))

            r = Road(xi, yi, w, h,elevation=round(elevations[t]),roadSpeed=roadspeed)
            roads.append(r)
            points.append((xi, yi))

            self.RoadNetwork.add_node(r, x=xi, y=yi,elevation=round(elevations[t]))
        print("ROADS: ", len(roads))
        return roads#,points


    def makeRoadsFromPoints(self,points=[],elevations=[],roadSpeeds=[],direction = "E",segmentNumber = 5,width = 5,height = 5):
        roads = []
        for (x,y),elevation,roadspeed in zip(points,elevations,roadSpeeds):
            r = Road(x, y, width, height,elevation=elevation,roadSpeed=roadspeed)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=x, y=y,elevation=round(elevation))
        return roads


    def setSegmentFromData(self,roadData:LineSegment):
        roads = self.segmentWithElevationChange(startX=roadData.startX,startY=roadData.startY,direction=roadData.direction,segmentNumber=roadData.segmentNumber,width=roadData.width,height=roadData.height,elevationStart=roadData.elevationStart,elevationEnd=roadData.elevationEnd,roadspeed=roadData.roadspeed)
        return roads

    def setCurveFromData(self,curveData:CurveData):
        roads = self.arcWithElevationChange(x0=curveData.x0,y0=curveData.y0,radius=curveData.radius,num_points=curveData.num_points,angle=curveData.angle,width=curveData.width,height=curveData.height,elevationStart=curveData.elevationStart,elevationEnd=curveData.elevationEnd,roadspeed=curveData.roadspeed,fx=curveData.fx,fy=curveData.fy,lx=curveData.lx,ly=curveData.ly)
        return roads


    def setEdges(self,roads,wraps=False):
     for i in range(len(roads) - 1):
        self.RoadNetwork.add_edge(roads[i], roads[i + 1])
        print("Connecting: ", i, " ", i + 1)
     if wraps:
        self.RoadNetwork.add_edge(roads[len(roads) - 1], roads[0])

    def setEdgesOfParallelLanes(self,roadSet1,roadSet2):
        #r1_length = len(roadSet1)
        #r2_length = len(roadSet2)
        for r1,r2 in zip(roadSet1, roadSet2):
            print(r1.x, r1.y, r2.x, r2.y)
            self.RoadNetwork.add_edge(r1, r2)


    def make_edge(self,node1,node2):
        self.RoadNetwork.add_edge(node1,node2)

    def make(self,ROAD_WIDTH,ROAD_HEIGHT):

        #self.makeSegment(10, 10, "E", 10, ROAD_WIDTH, ROAD_HEIGHT, True)
        #self.make_arc(x0=100,y0=200,radius=100,num_points=10,angle=90,j=100,k=100)#r=0,num_points=0,angle=0,j=0,k=0


        #r1 = self.setSegment(10, 10, "E", 10, ROAD_WIDTH, ROAD_HEIGHT, True)
        #r2 = self.getArc(x0=110,y0=10,radius=100,num_points=10,angle=90,width=ROAD_WIDTH,height=ROAD_HEIGHT)
        #r3 = self.setSegment(startX=10,startY=20,direction="S",segmentNumber=5,width=ROAD_WIDTH,height=ROAD_HEIGHT)
        #r_set = r1+r2
        #self.setEdges(r_set,wraps=True)
        #self.setEdges(r3,wraps=False)
        #self.make_edge(r1[0],r3[0])

        # for r in r2:
        #    print(r.x," ",r.y)
        # exit()

        #r1 = self.setSegment(10, 10, "E", 10, ROAD_WIDTH, ROAD_HEIGHT)
        #r2 = self.getArc(x0=110, y0=20, radius=50, num_points=11, angle=180, width=ROAD_WIDTH, height=ROAD_HEIGHT)
        #r_set = r1+r2
        #self.setEdges(r_set,wraps=True)

        #r3 = self.setSegment(110,10, "E", 10, ROAD_WIDTH, ROAD_HEIGHT)
        #self.setEdges(r3,wraps=False)
        #self.make_edge(r1[-1],r3[0])
        #self.make_edge(r3[-1],r1[0])

        #r1 = self.setSegment(50,10,"S",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=0)
        #r2 = self.setSegment(10,50,"E",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=100)
        #self.setEdges(r1,wraps=True)
        #self.setEdges(r2,wraps=True)

        #r1 = self.segmentWithElevationChange(50,10,"S",10,ROAD_WIDTH,ROAD_HEIGHT,elevationStart=0,elevationEnd=100)
        #self.setEdges(r1,True)



        #freeway exit loop
        #r1 = self.setSegment(50,100,"N",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=0,roadspeed=6)
        #r2 = self.setSegment(10,50,"E",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=100,roadspeed=4)
        #self.setEdges(r1,wraps=False)
        #self.setEdges(r2,wraps=False)

        #r3 = self.arcWithElevationChange(101,51,50,10,90,ROAD_WIDTH,ROAD_HEIGHT,elevationStart=100,elevationEnd=0,roadspeed=10)
        #self.setEdges(r3)
        #self.make_edge(r3[-1],r1[0])
        #self.make_edge(r2[-1],r3[0])
        #self.make_edge(r1[-1],r2[0])


        #testing multilane street
        #self.makeMultiLaneStreet(startX=10,startY=10,laneCount=5,segmentNumber=20,direction="E",width=ROAD_WIDTH,height=ROAD_HEIGHT,roadspeed=1,elevationStart=0,elevationEnd=100)


        #self.makeMultiLaneArc(x0=150,y0=100,laneCount=3,radius=100,num_points=10,angle=90,width=ROAD_WIDTH,height=ROAD_HEIGHT,elevationStart=0,elevationEnd=0,roadspeed=1)
        #r3 = self.arcWithElevationChange(101, 51, 50, 10, 90, ROAD_WIDTH, ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10,fx=0,fy=1,lx=1,ly=0)
        #r3 = self.arcWithElevationChange(101, 51, 50, 10, 90, ROAD_WIDTH, ROAD_HEIGHT, elevationStart=100,elevationEnd=0, roadspeed=10, fx=0, fy=-1, lx=-1, ly=0)

        eastLaneStartX = 100 #top left of interchange
        eastLaneStartY = 100
        segNum = 30
        mainRoadLanes = 3

        dis = (segNum * ROAD_WIDTH) - round(ROAD_WIDTH/2) #10
        westLaneStartX = eastLaneStartX + (segNum * ROAD_WIDTH) - round(ROAD_WIDTH/2)  #eastLaneStartX+90
        hypotLen = math.sqrt(round((dis/2)**2) + (round(dis/2)**2))  #pythagorean theorem to find the length of the hypot, then use it w/ 45 degree angle to get the top of the cross
        print("hypotLen: ", hypotLen)

        southStartY = round(eastLaneStartY - hypotLen * math.cos(45)) - (segNum) #this is normally `y + hypotLen` however positive is down in pygame
        print("southStartY: ", southStartY)
        northStartY = dis + southStartY #normally add but positive is down in pygame

        adj = 2* ROAD_WIDTH

        #exit()

        southStartX = (segNum*ROAD_WIDTH)/2 + eastLaneStartX - (ROAD_WIDTH * mainRoadLanes + adj) #80
        #east = LineSegment(eastLaneStartX,eastLaneStartY,"E",segmentNumber=segNum,width=ROAD_WIDTH,height=ROAD_HEIGHT,elevationStart=0,elevationEnd=0,roadspeed=1)
        east = self.makeMultiLaneStreet(startX=eastLaneStartX,startY=eastLaneStartY,laneCount=mainRoadLanes,direction="E",segmentNumber=segNum,width=ROAD_WIDTH,height=ROAD_HEIGHT,roadspeed=1,elevationStart=0,elevationEnd=0)

        #west = LineSegment(westLaneStartX, eastLaneStartY+(20*mainRoadLanes), "W", segmentNumber=segNum, width=ROAD_WIDTH,height=ROAD_HEIGHT, elevationStart=0, elevationEnd=0, roadspeed=1)
        west = self.makeMultiLaneStreet(startX=westLaneStartX, startY=eastLaneStartY+(adj*mainRoadLanes), laneCount=mainRoadLanes,direction="W", segmentNumber=segNum, width=ROAD_WIDTH, height=ROAD_HEIGHT,roadspeed=1, elevationStart=0, elevationEnd=0)

        #south = LineSegment(southStartX, southStartY, "S", segmentNumber=segNum, width=ROAD_WIDTH, height=ROAD_HEIGHT, elevationStart=100, elevationEnd=100, roadspeed=1)
        south = self.makeMultiLaneStreet(startX=southStartX, startY=southStartY + (mainRoadLanes * ROAD_HEIGHT), laneCount=mainRoadLanes,direction="S", segmentNumber=segNum, width=ROAD_WIDTH, height=ROAD_HEIGHT,roadspeed=1, elevationStart=100, elevationEnd=100)

        #north = LineSegment(southStartX+(20 *mainRoadLanes), northStartY + (mainRoadLanes * ROAD_HEIGHT), "N", segmentNumber=segNum, width=ROAD_WIDTH, height=ROAD_HEIGHT, elevationStart=100, elevationEnd=100, roadspeed=1)
        north = self.makeMultiLaneStreet(startX=southStartX+(adj *mainRoadLanes) , startY=northStartY + (mainRoadLanes * ROAD_HEIGHT), laneCount=mainRoadLanes, direction="N", segmentNumber=segNum, width=ROAD_WIDTH,height=ROAD_HEIGHT, roadspeed=1, elevationStart=100, elevationEnd=100)


        radius = (((hypotLen**2)/(8* dis/2)) ) + (dis/2)/2 #This works as a rough approximation
        print("radius: ", radius)
        #exit()
        south_to_west = self.arcWithElevationChange(southStartX, southStartY + (mainRoadLanes * ROAD_HEIGHT), radius, 10, 90, ROAD_WIDTH, ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10, fx=0, fy=1, lx=1, ly=0)
        north_to_east = self.arcWithElevationChange(southStartX+(adj *mainRoadLanes)+ (ROAD_WIDTH*mainRoadLanes), y0=northStartY + (mainRoadLanes * ROAD_HEIGHT) ,radius=radius, num_points=10, angle=90,width=ROAD_WIDTH,height= ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10, fx=0, fy=-1, lx=-1, ly=0)

        StE_start_idx = round(len(south_to_west)/3)
        StE_end_idx = round(len(north_to_east)/3)*2

        NtW_start_idx = round(len(north_to_east)/4)



        StE_start_road = south_to_west[StE_start_idx]
        NtW_start_road = north_to_east[NtW_start_idx]

        #print("StE_start: ", StE_start)
        #exit()
        south_to_east = self.arcWithElevationChange(x0=StE_start_road.x, y0=StE_start_road.y ,radius=radius-40, num_points=10, angle=150,width=ROAD_WIDTH,height= ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10, fx=0, fy=1, lx=-1, ly=-1)
        #southToWest = CurveData(100, 50, 30, 4,90, width=ROAD_WIDTH, height=ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10,fx=0,fy=1,lx=1,ly=0)
        north_to_west = self.arcWithElevationChange(x0=NtW_start_road.x-ROAD_WIDTH, y0=NtW_start_road.y-ROAD_HEIGHT ,radius=radius-30, num_points=10, angle=150,width=ROAD_WIDTH,height= ROAD_HEIGHT, elevationStart=100, elevationEnd=0, roadspeed=10, fx=0, fy=0, lx=1, ly=1)




        #westBoundRoads = self.setSegmentFromData(roadData=west)
        #northBoundRoads = self.setSegmentFromData(roadData=north)
        #southBoundRoads = self.setSegmentFromData(roadData=south)

        #south_to_west = self.setCurveFromData(curveData=southToWest)


        #self.stackInterchange(eastBoundLanes=east,westBoundLanes=west,northBoundLanes=north,southBoundLanes=south,southToWest=southToWest)
        return self.RoadNetwork

    def makeMultiLaneArc(self,x0,y0,laneCount=1,radius=0,num_points=0,angle=0,width=5,height=5,elevationStart=0,elevationEnd=0,roadspeed=1):
        elevationChange = elevationEnd - elevationStart
        roadSets = []
        # actionFunction = self.parallelActionFunctions[direction]
        x, y = x0, y0

        for i in range(laneCount):
            roadSet = []
            if elevationChange > 0:
                roadSet =self.arcWithElevationChange(x0=x,y0=y,radius=radius,num_points=num_points,angle=angle,width=width,height=height,elevationStart=elevationStart,elevationEnd=elevationEnd,roadspeed=roadspeed)
            else:
                roadSet = self.arcWithElevationChange(x0=x, y0=y, radius=radius, num_points=num_points, angle=angle,
                                                      width=width, height=height, elevationStart=elevationStart,
                                                      elevationEnd=elevationEnd, roadspeed=roadspeed)
                #roadSet = self.getArc(x0=x, y0=y, radius=radius, num_points=num_points, angle=angle, width=width, height=height,elevation=elevationStart,roadspeed=roadspeed)

            self.setEdges(roadSet)
            roadSets.append(roadSet)
            #x, y = actionFunction(x=x, y=y, roadWidth=width, roadHeight=height)#what to do here?
            x,y = x+width,y
            #radius = radius + width + (width/2.5)
            radius = radius + width
            num_points = num_points + 1

        #print("Roadset Count")
        #print(len(roadSets))

        #for i in range(len(roadSets) - 1):
        #    self.setEdgesOfParallelLanes(roadSets[i], roadSets[i + 1])

        #for i in range(len(roadSets) - 1):
        #    self.setEdgesOfParallelLanes(roadSets[len(roadSets) - 1 - i], roadSets[len(roadSets) - 2 - i])

        return roadSets

    def lerp(self,x0,x1,i):
        return x0+i*(x1-x0)
    def getEquidistantPoints(self,start,end,steps):
        return [self.lerp(start,end,1/steps*i) for i in range(steps+1)]


    '''This function will build streets top to bottom and left to right'''
    def makeMultiLaneStreet(self,startX = 0,startY=0,laneCount=1,direction = "E",segmentNumber = 5,width = 5,height = 5,roadspeed=1,elevationStart=0,elevationEnd=0):
        elevationChange = elevationEnd-elevationStart
        roadSets = []
        actionFunction = self.parallelActionFunctions[direction]
        x,y = startX,startY
        for i in range(laneCount):
            roadSet = []
            if elevationChange > 0:
                roadSet = self.segmentWithElevationChange(startX=x, startY=y, direction=direction, segmentNumber=segmentNumber, width=width, height=height, elevationStart=elevationStart, elevationEnd=elevationEnd, roadspeed=roadspeed)
            else:
                roadSet = self.setSegment(startX=x,startY=y,direction=direction,segmentNumber=segmentNumber,width=width,height=height,elevation=elevationStart,roadspeed=roadspeed)

            self.setEdges(roadSet)
            roadSets.append(roadSet)
            x,y = actionFunction(x=x,y=y,roadWidth = width,roadHeight=height)

        print("Roadset Count")
        print(len(roadSets))

        for i in range(len(roadSets)-1):
            self.setEdgesOfParallelLanes(roadSets[i],roadSets[i+1])

        for i in range(len(roadSets)-1):
            self.setEdgesOfParallelLanes(roadSets[len(roadSets)-1-i],roadSets[len(roadSets)-2-i])

        return roadSets


    def computeNormals(self,points):
        normals = []
        for i in range(len(points)):
            if i == 0:
                dx = points[i+1][0] - points[i][0]
                dy = points[i+1][1] - points[i][1]
            elif i == len(points)-1:
                dx = points[i][0] - points[i-1][0]
                dy = points[i][1] - points[i-1][1]
            else:
                dx = points[i+1][0] - points[i-1][0]
                dy = points[i+1][1] - points[i-1][1]

            length = math.hypot(dx,dy)
            if length == 0:
                normals.append((0,0))
            else:
                nx = -dy/length
                ny = dx/length
                normals.append((nx,ny))
        return normals

    def offsetCurve(self,points,normals,offset):
        offsetPoints = []
        for (x,y),(nx,ny) in zip(points,normals):
            offsetPoints.append((x + nx * offset,y + ny * offset))

        return offsetPoints



    def cloverInterchange(self, eastBoundLanes:LineSegment,westBoundLanes:LineSegment,southBoundLanes: LineSegment,northBoundLanes: LineSegment):
        #east/westbound lanes
        eastBoundRoads = self.setSegmentFromData(roadData=eastBoundLanes)
        westBoundRoads = self.setSegmentFromData(roadData=westBoundLanes)
        northBoundRoads = self.setSegmentFromData(roadData=northBoundLanes)
        southBoundRoads = self.setSegmentFromData(roadData=southBoundLanes)

        #crossAtE

    def stackInterchange_(self,eastBoundLanes:LineSegment,westBoundLanes : LineSegment,southBoundLanes : LineSegment,northBoundLanes : LineSegment,southToWest:CurveData):
        eastBoundRoads = self.setSegmentFromData(roadData=eastBoundLanes)
        westBoundRoads = self.setSegmentFromData(roadData=westBoundLanes)
        northBoundRoads = self.setSegmentFromData(roadData=northBoundLanes)
        southBoundRoads = self.setSegmentFromData(roadData=southBoundLanes)

        south_to_west = self.setCurveFromData(curveData=southToWest)

    def stackInterchange(self):
        pass



    def makeCurvedLine(self,startX,startY,endX,endY,radius):
        distance = math.dist((startX,startY),(endX,endY))#euclidean distance between 2 pts
        sagitta = self.computeSagitta(radius,distance/2)
        midpoint = self.computeMidpoint(startX,startY,endX,endY)

    def computeSagitta(self,radius,length):
        return (radius - (math.sqrt((radius * radius) - (length * length))))

    def computeMidpoint(self,startX,startY,endX,endY):
        return (startX+endX)/2,(startY+endY)/2
