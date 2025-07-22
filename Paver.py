from math import radians

from Road import Road
import networkx as nx
import math

def Make_EAST(x,y,roadWidth,roadHeight):
    return x+roadWidth,y
def Make_WEST(x,y,roadWidth,roadHeight):
    return x-roadWidth,y
def Make_NORTH(x,y,roadWidth,roadHeight):
    return x, y-roadHeight
def Make_SOUTH(x,y,roadWidth,roadHeight):
    return x, y + roadHeight

def scaleEW(deltaX,deltaY,roadWidth,roadHeight):
    return deltaX/roadWidth,deltaY
def scaleNS(deltaX,deltaY,roadWidth,roadHeight):
    return deltaX,deltaY/roadHeight

class Paver:
    RoadNetwork = nx.DiGraph()
    action_functions = {"E": Make_EAST, "W": Make_WEST, "N": Make_NORTH, "S": Make_SOUTH}
    laneAdditionActionFunctions = {"E": Make_SOUTH, "W": Make_SOUTH, "N": Make_EAST, "S": Make_EAST}
    laneScalerFunctions = {"E": scaleEW, "W": scaleEW, "N": scaleNS,"S": scaleNS}
    def __init__(self):
        pass

    def setEdges(self,roads,wraps = False):
        for i in range(len(roads) - 1):
            self.RoadNetwork.add_edge(roads[i], roads[i + 1])
            print("Connecting: ", i, " ", i + 1)
        if wraps:
            self.RoadNetwork.add_edge(roads[len(roads) - 1], roads[0])

    def setEdgesOfParallelLanes(self,roadSet1,roadSet2):
        for r1,r2 in zip(roadSet1, roadSet2):
            print(r1.x, r1.y, r2.x, r2.y)
            self.RoadNetwork.add_edge(r1, r2)


    def make_road_from_points_list(self, points, width=10,height=10,color: tuple[int, int, int] = (255, 255, 255) ,elevationStart=0,elevationEnd=0,speed=1,wraps=False,stopSignsAt:set[tuple[int,int]] = []):
        segmentCount = len(points)-1
        elevations = self.getEquidistantValues(elevationStart, elevationEnd, segmentCount)

        roads = []
        for point,elevation in zip(points,elevations):
            hasStopSign = False
            if point in stopSignsAt:
                hasStopSign = True
            r = Road(x=point[0],y=point[1], width=width, height=height,color=color,origionalColor=color,elevation=elevation,roadSpeed=speed,hasStopSign=hasStopSign)
            roads.append(r)
            self.RoadNetwork.add_node(r,x=point[0], y=point[1], width=width, height=height,color=color,elevation=elevation,hasStopSign=hasStopSign)

        return roads

    def make_road_from_point(self,point:tuple[float,float],width,height,color,elevation,speed=1,hasStopSign=False):
        r = Road(x=point[0], y=point[1], width=width, height=height, color=color, origionalColor=color,elevation=elevation,roadSpeed=speed, hasStopSign=hasStopSign)
        self.RoadNetwork.add_node(r,x=point[0], y=point[1], width=width, height=height,color=color,elevation=elevation,hasStopSign=hasStopSign)
        return r

    def make_lane_with_endpoints(self,startPoints:tuple[float,float],endPoints:tuple[float,float],roadWidth:int,roadHeight:int,laneCount = 1,direction="E",elevationStart=0,elevationEnd=0):
        roadList = []
        #x_adj = self.getEquidistantValues(startPoints[0], endPoints[0], laneCount)
        #y_adj = self.getEquidistantValues(startPoints[1], endPoints[1], laneCount)
        laneAdjustmentFunction = self.laneAdditionActionFunctions[direction]



        x,y = startPoints[0],startPoints[1]
        x_end,y_end = endPoints[0],endPoints[1]
        segmentCount = abs(round(self.getSegmentCount(startPoints,endPoints,roadWidth,roadHeight)))
        #print("segmentCount", segmentCount," for direction: ",direction)
        #print(segmentCount)
        #elevations = self.getEquidistantValues(elevationStart, elevationEnd, segmentCount)

        for i in range(laneCount):
            #needs to be changed, direction needs to be tracked
            startPoint = (x,y)
            endPoint = (x_end,y_end)

            points = self.getEquidistantPoints(startPoint, endPoint, segmentCount)

            roads = self.make_road_from_points_list(points,roadWidth,roadHeight,elevationStart=elevationStart,elevationEnd=elevationEnd)





            self.setEdges(roads)
            roadList.append(roads)
            x,y = laneAdjustmentFunction(x,y,roadWidth,roadHeight)
            x_end,y_end = laneAdjustmentFunction(x_end,y_end,roadWidth,roadHeight)

        for i in range(len(roadList)-1):
            self.setEdgesOfParallelLanes(roadList[i],roadList[i+1])
            self.setEdgesOfParallelLanes(roadList[len(roadList) - 1 - i], roadList[len(roadList) - 2 - i])

        return roadList


    def make_lane_start_and_count(self,startX = 0,startY=0,direction = "E",segmentNumber = 5,width = 5,height = 5,elevationStart=0,elevationEnd=0,roadspeed=1):
        pass

    def makeArc(self,start:tuple[float,float],end:tuple[float,float],angle=90,numPoints=1,width=5,height=5,elevationStart=0,elevationEnd=0,roadspeed=1,fx=0,fy=1,lx=1,ly=0):
        '''DOES NOT SET EDGES'''
        #https://stackoverflow.com/questions/14384217/how-to-find-points-on-the-circumference-of-a-arc-knowing-a-start-point-an-end-p
        elevations = self.getEquidistantValues(elevationStart, elevationEnd, numPoints)

        radians = math.radians(angle)
        cx,cy,radius = self.get_Center_And_Radius_From_Points_And_Angle(start=start,end=end,angle=angle)
        print(cx,cy,radius)
        #exit()
        x0 = start[0]
        y0 = start[1]

        roads = []
        points = []
        for t in range(numPoints):
            sub_angle = (t/numPoints)*radians
            xi = x0 + radius * (math.sin(sub_angle) * fx + (1 - math.cos(sub_angle)) * (-lx))
            yi = y0 + radius * (math.sin(sub_angle) * fy + (1 - math.cos(sub_angle)) * (-ly))

            #xi = x0 + radius * (math.sin(sub_angle) + (1 - math.cos(sub_angle)) )
            #yi = y0 + radius * (math.sin(sub_angle) + (1 - math.cos(sub_angle)) )
            #xi = cx + radius * math.cos(sub_angle)
            #yi = cy + radius * math.sin(sub_angle)
            r = Road(xi,yi,width=width,height=height,elevation=round(elevations[t]),roadSpeed=roadspeed)
            roads.append(r)
            points.append((xi,yi))
            self.RoadNetwork.add_node(r,x = xi,y = yi,elevation = round(elevations[t]),roadSpeed=roadspeed)

        return roads

    def setStackInterchange(self):
        pass



    def get_Center_And_Radius_From_Points_And_Angle(self,start:tuple[float,float],end:tuple[float,float],angle:float):
        '''Returns cx,cy,r'''
        #this function needs to be tested more
        #https://math.stackexchange.com/questions/1144159/parametric-equation-of-an-arc-with-given-radius-and-two-points
        x_start = start[0]
        y_start = start[1]
        x_end = end[0]
        y_end = end[1]

        cx = ((1+math.cos(angle)) * (y_start - y_end) + math.sin(angle) * (x_start + x_end)) / (2 * math.sin(angle))
        cy = ((math.sin(angle) * (y_start +y_end)) + ((1+math.cos(angle)) * (x_end-x_start))) / (2 *math.sin(angle))

        r = math.sqrt(((x_end - x_start)**2 + (y_end - y_start)**2) / (2*(1-math.cos(angle))))

        return cx,cy,r

    def lerp(self,x0,x1,i):
        return x0+i*(x1-x0)
    def getEquidistantValues(self, start, end, steps):
        return [self.lerp(start, end, 1 / steps * i) for i in range(steps + 1)]

    def getEquidistantPoints(self, p1, p2, n):
        return [(self.lerp(p1[0], p2[0], 1. / n * i), self.lerp(p1[1], p2[1], 1. / n * i)) for i in range(n + 1)]

    def getSegmentCount(self,start,end,roadWidth,roadHeight):
        deltaX = end[0] - start[0]
        deltaY = end[1] - start[1]
        if deltaX != 0:
            return deltaX/roadWidth
        else:
            return deltaY/roadHeight

    def test_road_building(self,ROAD_WIDTH,ROAD_HEIGHT):

        #startPoint = (10,10)
        #endPoint = (50,50)
        #roads = self.makeArc(startPoint,endPoint,angle=180,numPoints=10,width=10,height=10,elevationStart=0,elevationEnd=0,roadspeed=1)
        #roads = self.make_lane_with_endpoints(startPoint,endPoint,roadWidth=10,roadHeight=10,laneCount=2)

        #for road in roads:
        #self.setEdges(roads,wraps=True)

        westStart = (200, 100)
        westEnd = (50, 100)
        mainLaneCount = 2
        space_between_lanes = ROAD_HEIGHT



        #eastStart = (50,50)
        #eastEnd = (200,50)
        #mainLaneCount = 2

        #segNum = (150-50) / ROAD_WIDTH


        westLanes = self.make_lane_with_endpoints(westStart,westEnd,roadWidth=ROAD_WIDTH,roadHeight=ROAD_HEIGHT,laneCount=mainLaneCount,direction="W")
        #print(eastLanes)

        eastStart = (westEnd[0],westEnd[1] + (mainLaneCount * ROAD_HEIGHT)+ space_between_lanes)
        eastEnd = (westStart[0], westStart[1] + (mainLaneCount * ROAD_HEIGHT) + space_between_lanes)
        #westStart = (eastEnd[0],eastEnd[1] + (mainLaneCount * ROAD_HEIGHT)+ ROAD_HEIGHT)
        #westEnd = (eastStart[0],eastStart[1] + (mainLaneCount * ROAD_HEIGHT) + ROAD_HEIGHT)
        #print(westStart,westEnd)

        eastLanes = self.make_lane_with_endpoints(eastStart,eastEnd,roadWidth=ROAD_WIDTH,roadHeight=ROAD_HEIGHT,laneCount=mainLaneCount,direction="E")

        midPoint = (westStart[0]+westEnd[0]) /2 #using westlanes 0 to get the first lane of all lanes
        print("midpoint: ",midPoint)
        #offset = (mainLaneCount * ROAD_WIDTH) + (space_between_lanes/2)
        offset = ((space_between_lanes) /2 ) + mainLaneCount* ROAD_WIDTH

        print("offset: ",offset)
        #len(westLanes[0])
        print("len(westLanes[0]): ",len(westLanes[0]))
        print("space_between_lanes: ",space_between_lanes)
        #space_used_by_eastwest = ROAD_HEIGHT * (mainLaneCount*2) + space_between_lanes
        segments_used_by_eastwest = (mainLaneCount * 2) + (space_between_lanes/ ROAD_HEIGHT)
        y_south_start_offset_segments = (len(westLanes[0]) - segments_used_by_eastwest) / 2
        print("y_south_start_offset_segments: ",y_south_start_offset_segments)
        #print("space_used_by_eastwest: ",space_used_by_eastwest)
        y_start_south =  westEnd[1] - (y_south_start_offset_segments * ROAD_HEIGHT)
        print("y_start_south: ",y_start_south)

        #exit()

        print("y_start_south: ",y_start_south)



        southStart = (midPoint-offset ,y_start_south) #- (mainLaneCount * ROAD_WIDTH)
        print("southStart: ",southStart)
        print("len(westLanes[0]): ",len(westLanes[0]))
        southEnd = (midPoint-offset,y_start_south + (len(westLanes[0])*ROAD_HEIGHT)) #- (mainLaneCount * ROAD_WIDTH)
        print("southEnd: ",southEnd)

        #exit()
        southLanes = self.make_lane_with_endpoints(southStart, southEnd, roadWidth=ROAD_WIDTH, roadHeight=ROAD_HEIGHT,laneCount=2, direction="S",elevationStart=100,elevationEnd=100)
        print(southLanes)


        northStart = (midPoint+(space_between_lanes / 2),southEnd[1])
        northEnd = (midPoint + (space_between_lanes / 2), southStart[1])

        print("westStart: ",westStart)
        print("westEnd: ",westEnd)

        print("southStart: ",southStart)
        print("southEnd: ",southEnd)
        print("northStart: ",northStart)
        print("northEnd: ",northEnd)
        #exit()
        northLanes = self.make_lane_with_endpoints(northStart, northEnd, roadWidth=ROAD_WIDTH, roadHeight=ROAD_HEIGHT,laneCount=2, direction="N",elevationStart=100,elevationEnd=100)
        #exit()


        #cx,cy,r = self.get_Center_And_Radius_From_Points_And_Angle(southStart,westEnd,90)
        arc_offset_adjustment = 1
        #south_t
        southToWest = self.makeArc(start=southStart,end=westEnd,angle=90,numPoints=10,width=ROAD_WIDTH,height=ROAD_HEIGHT,elevationStart=100,elevationEnd=0,roadspeed=1,fx=0,fy=1,lx=1,ly=0)
        self.setEdges(southToWest)


        westToNorth = self.makeArc(start=westStart, end=northEnd, angle=-90, numPoints=10, width=ROAD_WIDTH, height=ROAD_HEIGHT,elevationStart=0, elevationEnd=100, roadspeed=1,fx=1,fy=0,lx=0,ly=1)
        self.setEdges(westToNorth)

        northStartArc = (northStart[0] + (mainLaneCount - 1) * ROAD_WIDTH,northStart[1])
        northToEast = self.makeArc(start=northStartArc, end=eastEnd, angle=90, numPoints=10, width=ROAD_WIDTH, height=ROAD_HEIGHT,elevationStart=100, elevationEnd=0, roadspeed=1,fx=0,fy=-1,lx=-1,ly=0)
        self.setEdges(northToEast)

        eastStartArc = (eastStart[0] , eastStart[1] + (mainLaneCount - 1) * ROAD_HEIGHT)
        eastToSouth = self.makeArc(start=eastStartArc, end=southEnd, angle=-90, numPoints=10, width=ROAD_WIDTH, height=ROAD_HEIGHT,elevationStart=0, elevationEnd=100, roadspeed=1,fx=-1,fy=0,lx=0,ly=-1)
        self.setEdges(eastToSouth)

        return self.RoadNetwork
