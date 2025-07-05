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
class BuildRoadNetwork:
    #RoadNetwork = {}
    RoadNetwork = nx.DiGraph()
    action_functions = {"E":Make_EAST, "W":Make_WEST, "N":Make_NORTH, "S":Make_SOUTH}
    def __init__(self):
        pass

    def makeSegment(self,startX = 0,startY=0,direction = "E",segmentNumber = 5,width = 5,height = 5,wraps=False):
        direction_function = self.action_functions[direction]
        roads = []
        x = startX
        y = startY
        r = Road(x, y, width, height)
        roads.append(r)
        self.RoadNetwork.add_node(r, x=x, y=y)
        for i in range(segmentNumber-1):
            x,y = direction_function(x,y,width,height)
            #roads.append(Road(x, y, width, height))
            r = Road(x,y,width,height)
            roads.append(r)
            self.RoadNetwork.add_node(r,x=x,y=y)
        print("LEN OF ROADS: ", len(roads))

        for i in range(len(roads)-1):

            self.RoadNetwork.add_edge(roads[i],roads[i+1])
            print("Connecting: ",i," ",i+1)
        if wraps:
            self.RoadNetwork.add_edge(roads[len(roads)-1],roads[0])


            #if not roads:
    #            roads.append(Road(x, y, width, height))

            #else:
            #    prev = roads[-1]
        print(self.RoadNetwork)
        print(self.RoadNetwork.nodes())
        #return roads
        return self.RoadNetwork
    #def AddNode(self,):


    def make_arc(self,x0=0,y0=0,x1=0,y1=0,radius=0,num_points=0,angle=0,j=0,k=0):
        #sub_angle = angle/num_points
        roads = []
        w = 5
        h = 5
        fx = 1
        fy = 0
        lx = 0
        ly = 1
        for t in range(num_points):
            #radians = 22.5 * (math.pi / 180)
            radians = math.radians(angle)
            sub_angle = (t / 10) * radians
            #285.206
            xi = x0 + radius * (math.sin(sub_angle) * fx + (1 - math.cos(sub_angle)) * (-lx))
            yi = y0 + radius * (math.sin(sub_angle) * fy + (1 - math.cos(sub_angle)) * (-ly))

            #sub_angle = (i / 10) * deg2rad(22.5);
            #xi = x + 285.206 * (sin(sub_angle) * fx + (1 - cos(sub_angle)) * (-lx))
            #yi = y + 285.206 * (sin(sub_angle) * fy + (1 - cos(sub_angle)) * (-ly))


            #x = radius * math.cos(t) + j
            #y = radius *math.sin(t) + k
            r = Road(xi,yi,w,h)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=xi, y=yi)

        for i in range(len(roads)-1):
            self.RoadNetwork.add_edge(roads[i],roads[i+1])
            print("Connecting: ",i," ",i+1)
        #if wraps:
        #    self.RoadNetwork.add_edge(roads[len(roads)-1],roads[0])

        return self.RoadNetwork

    def getArc(self,x0,y0,radius=0,num_points=0,angle=0,width=5,height=5):
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
            r = Road(xi, yi, w, h)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=xi, y=yi)
        print("ROADS: ",len(roads))
        return roads

    def setSegment(self,startX = 0,startY=0,direction = "E",segmentNumber = 5,width = 5,height = 5,elevation=0):
        direction_function = self.action_functions[direction]
        roads = []
        x = startX
        y = startY
        r = Road(x, y, width, height)
        roads.append(r)
        self.RoadNetwork.add_node(r, x=x, y=y)
        for i in range(segmentNumber - 1):
            x, y = direction_function(x, y, width, height)
            r = Road(x, y, width, height,elevation=elevation)
            roads.append(r)
            self.RoadNetwork.add_node(r, x=x, y=y)
        print("LEN OF ROADS: ", len(roads))
        return roads

        #for i in range(len(roads) - 1):
        #    self.RoadNetwork.add_edge(roads[i], roads[i + 1])
        #    print("Connecting: ", i, " ", i + 1)
        #if wraps:
        #    self.RoadNetwork.add_edge(roads[len(roads) - 1], roads[0])

    def setEdges(self,roads,wraps=False):
     for i in range(len(roads) - 1):
        self.RoadNetwork.add_edge(roads[i], roads[i + 1])
        print("Connecting: ", i, " ", i + 1)
     if wraps:
        self.RoadNetwork.add_edge(roads[len(roads) - 1], roads[0])

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

        r1 = self.setSegment(50,10,"S",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=0)
        r2 = self.setSegment(10,50,"E",10,ROAD_WIDTH,ROAD_HEIGHT,elevation=0)
        self.setEdges(r1,wraps=True)
        self.setEdges(r2,wraps=True)

        return self.RoadNetwork

