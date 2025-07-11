class RoadData:
    def InterchangeSegmentLine(self,):
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