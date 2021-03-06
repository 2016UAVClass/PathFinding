# This file generates somewhat evenly distributed points in a given polygon. 
# The polygon can take on any shape. The algorithm works by accepting the 
# points of the polygon and the number of traps to be placed down. 

import shapely
import shapely.geometry as sg
import math
import random


# The TrapZone class represents the area that traps need to be distributed
# in. It is assumed that the entire TrapZone is a fly-zone. 
class TrapZone(object):
    def __init__(self, zone, obstacles, radius):
        self.zone = zone
        self.obstacles = obstacles
        self.radius = radius

    # function that generates the locations of the traps.
    # returns a list of xy pairs for each trap. The algorithm finds a 
    # rectangle that surrounds the polygon. Then it evenly distributes 
    # points inside that rectangle. Then, the program iterates through
    # all of the points and only keeps the ones that are contained inside
    # the polygon.
    def genPoints(self):
        bounds = self.zone.bounds  # get the corners of the rectangle that contain the Polygon
        width = math.ceil(bounds[2] - bounds[0])
        height = math.ceil(bounds[3] - bounds[1])
        # generate coordinates in a rectangle
        points = self.genCoords(width, height)
        points = [[x[0] + bounds[0], x[1] + bounds[1]] for x in points]
        return self.pointsInZone(points)

    def genCoords(self, width, height):

        # First, use the radius to populate the rectangle
        inc = 1.8 * self.radius
        points = []
        w = 0
        while w < width:
            h = 0
            while h < height:
                points = points + [(w, h)]
                h = h + inc
            w = w + inc
        # center the points in the rectangle
        x_shift = (width - points[len(points) - 1][0]) / 2
        y_shift = (height - points[len(points) - 1][1]) / 2
        points = [[x[0] + x_shift, x[1] + y_shift] for x in points]
        return points

    def pointsInZone(self, points):
        trap_locs = []
        trap_loc_pts = []
        for x in points:
            ptx = shapely.geometry.Point(x)
            if self.zone.contains(ptx):
                if not self.obstacles or all([not obs.contains(ptx) for obs in self.obstacles]):
                    trap_locs.append(x)
                    trap_loc_pts.append(ptx)
            else:
                #so point not in zone, look to where it can be placed
                #calculate closest point on zone border
                zone = self.zone
                d=zone.boundary.project(ptx)
                cp = zone.boundary.interpolate(d)
                if cp.distance(ptx)<self.radius: #only move if moving less than a trap's area away
                    #now move cp off the border
                    OFFSET = 5
                    #move new_point offset units into polygon
                    new_point = sg.Point(cp.x + math.copysign(OFFSET, cp.x-ptx.x),
                                         cp.y + math.copysign(OFFSET, cp.y-ptx.y))
                    #if the new point is at least half a radius from all other trap locations, add it
                    dists = [new_point.distance(sg.Point(tl[0], tl[1])) for tl in trap_locs]
                    if all([d > self.radius/2. for d in dists]):
                        trap_locs.append([new_point.x, new_point.y])
                        trap_loc_pts.append(new_point)
                
                
                
        return trap_locs, trap_loc_pts


def drawPoints(canvas, points, size, color):
    for x in points:
        canvas.create_oval(x[0] - size, x[1] + size, x[0] + size, x[1] - size, fill=color)
