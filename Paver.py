from Road import Road
import networkx as nx
import math
class Paver:
    RoadNetwork = nx.DiGraph()
    def __init__(self):
        pass

    def make_road_from_points_list(self, points, width=10,height=10,color: tuple[int, int, int] = (255, 255, 255) ,elevationStart=0,elevationEnd=0,speed=1,wraps=False,stopSignsAt:set[tuple[int,int]] = []):
        segmentCount = len(points)-1
        elevations = self.getEquidistantPoints(elevationStart, elevationEnd, segmentCount)

        roads = []
        for point,elevation in points,elevations:
            hasStopSign = False
            if point in stopSignsAt:
                hasStopSign = True
            r = Road(x=point[0],y=point[1], width=width, height=height,color=color,origionalColor=color,elevation=elevation,hasStopSign=hasStopSign)
            roads.append(r)
            self.RoadNetwork.add_node(r,x=point[0], y=point[1], width=width, height=height,color=color,elevation=elevation,hasStopSign=hasStopSign)


    def make_lane(self,startPoints:tuple[float,float],endPoints:tuple[float,float],roadWidth:int,roadHeight:int):
        if startPoints[0] == endPoints[0] or startPoints[1] == endPoints[1]:
            pass


    def lerp(self,x0,x1,i):
        return x0+i*(x1-x0)
    def getEquidistantPoints(self, start, end, steps):
        return [self.lerp(start, end, 1 / steps * i) for i in range(steps + 1)]


    def test_road_building(self):
        pass