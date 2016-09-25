#given a path and a horizantal speed, estimates how long it will take to complete

#todo: consider adding vertical speed calculation as well?

import math

#given a path (sequence of 2 element list-like objects) and a speed, returns the time it will take to traverse
#the path. Assumes the speed is in units [path units]/[desired time units]
#is if path coords are in meters, want time in secs, speed should be in m/s
def calc_time(path, speed):
    if len(path)<2: #no time to traverse 1 element path
        return 0

    total_dist = 0.
    for i in range(1, len(path)):
        total_dist+=get_distance(path[i-1], path[i])

    return total_dist/speed

#basic distance formula, applied to p1 and p2
def get_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)