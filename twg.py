import map_gen_script
import map_to_path
import maintrap

import argparse
import json
import shapely.geometry as sg
import sys

"""
Trap Waypoint Generator
Proper usage:
    First, use map_gen_script to generate the general map object, with the fly zone and the obstacles
    Name the fly zone 'fly_zone', and all obstacles 'obstacle'
    Next, call this script passing in the arguments as specified.
    Need help? try running python twg.py -h
"""


# turns a shapely point into a list
def to_list(pt):
    return [pt.x, pt.y]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a path for multiple UAVs that places traps throughout an area")

    parser.add_argument("map_file", help="The name of the map file containing the obstacles and zone",
                        type=argparse.FileType("r"))

    parser.add_argument("--num_uavs", help="number of UAVs (default %(default)s)", type=int, default=1)

    parser.add_argument("warehouse", help="Location of the warehouse, specified as 2 doubles (ex: 72.3 92.4)",
                        type=float, nargs=2)

    parser.add_argument("--num_traps", help="number of traps to distribute, if 0, then assume unlimited",
                        type=int, default=0)

    parser.add_argument("--gap", help="the minimum gap between UAVs. Default: %(default)s", default=5,
                        type=float)

    parser.add_argument("radius", help="the coverage radius of a trap", type=int)

    parser.add_argument("--buffer_size", type=float, default=0,
                        help="the size of the buffer on the edges of the fly zone and obstacles for placing traps. Default: %(default)s")

    parser.add_argument("--wp_acc",
                        help="the radius on each waypoint (how close to the actual center must the vehicle be) Default: %(default)s",
                        type=float, default=10)

    args = parser.parse_args()

    # create the map object from the file
    dec = json.JSONDecoder()
    mapobj = dec.decode(args.map_file.read())

    # extract the fly zone
    if "fly_zone" in mapobj:
        zone = mapobj["fly_zone"]
    else:
        print "error, could not find zone called 'fly_zone'"
        sys.exit()

    # extract any obstacles
    obstacles = []
    for k in mapobj.keys():
        if k == "obstacle":
            obstacles.append(mapobj[k].bounds)

    _, trap_points = maintrap.place_traps(zone, obstacles, args.radius, args.buffer_size)
    warehouse = sg.Point(args.warehouse)

    # add start points for all UAVs as the warehouse (or just outside it)
    for i in range(args.num_uavs):
        sp = {"type": "start_point",
              "point": [warehouse.x + args.gap, warehouse.y],
              "vehicle_i": i}
        mapobj["StartPoint"] = sp


    # sort the traps by the distance from the warehouse
    def sort_key(point):
        return point.distance(warehouse)


    trap_points.sort(key=sort_key)

    vehicle_i = 0
    waypoint_num = [0 for i in range(args.num_uavs)]

    def add_wp(trap):
        wp = {"type": "waypoint",
              "center": to_list(trap),
              "radius": args.wp_acc,
              "index": waypoint_num[vehicle_i],
              "vehicle_i": vehicle_i}
        waypoint_num[vehicle_i] += 1
        mapobj["wp"]=wp

    def add_warehouse():
        add_wp(warehouse)
        vehicle_i= (vehicle_i+1) %args.num_uavs #cycle the vehicle index to the next one

    for trap in trap_points:
        add_wp(trap)
        add_warehouse() #must return to warehouse before going out again

    paths = map_to_path.createPathFromMap(mapobj, height_gap=args.gap)

    #deal with paths!
