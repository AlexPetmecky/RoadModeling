class LineSegment:
    def __init__(self, startX: int,startY: int,direction: str ,segmentNumber: int, width: int,height: int,elevationStart: int,elevationEnd: int,roadspeed: int ):
        self.startX = startX
        self.startY = startY
        self.direction = direction
        self.segmentNumber = segmentNumber
        self.width = width
        self.height = height
        self.elevationStart = elevationStart
        self.elevationEnd = elevationEnd
        self.roadspeed = roadspeed

class MultiLineSegment:
    def __init__(self,lineSegments: list[LineSegment]):
        self.lineSegments = lineSegments
