import json

struc={}

#gets a point, call if the new object type has points
def getPoint():
    done=False
    while not done:
        pt=input("enter a point [x, y]: ")
        while not pt:
            pt=input("enter a point [x, y]: ")
        try:
            x, y=pt.split(", ")
        except:
            print("error splitting data, please enter 2 numbers seperated by comma")
            continue
        if not x.isdigit() or not y.isdigit():
            print("invalid integers, try again")
        else:
            return (int(x), int(y))

#gets an integer
def getInt(prompt):
    while True:
        i=input(prompt)
        while not i.isdigit():
            i=input("Invalid int "+prompt)
        return int(i)

#type names for objects
VALID_MAP_OBJ={
    "ZONE" : "zone",
    "WAYPOINT" : "waypoint",
    "START_POINT":"start_point"
    }

#creates a zone, adds it to struc
    #takes a zone_name which defaults to fly_zone
    #takes a can_fly parameter, specifies if fly or no fly zone
    #also accepts keyword arguments, adds those to the dictionary 
def createZone(can_fly, zone_name, **kwargs):
    global struc
    print("enter the boundaries of the fly zone")
    zone=dict(**kwargs)
    done=False
    pts=[]
    numpts=getInt("How many points are there?")
    print
    for i in range(numpts):
        pts.append(getPoint())

    zone["type"]=VALID_MAP_OBJ["ZONE"]
    zone["bounds"]=pts
    zone["flight_legal"]=can_fly
    struc[zone_name]=zone

#creates the waypoint numbered index, applied to vehicle number vehicle_i
#vehicle_i defaults to 0, which is the first vehicle
def createWaypoint(index, vehicle_i=0):
    print("Enter the center of waypoint", index)
    loc=getPoint()
    rad=getInt("Enter the radius of the waypoint")
    wp={}
    wp["type"]=VALID_MAP_OBJ["WAYPOINT"]
    wp["center"]=loc
    wp["radius"]=rad
    wp["index"]=index
    wp["vehicle_i"]=vehicle_i
    global struc
    struc["Waypoint"+str(index)]=wp

#creates num waypoints, numbered 1-num
def createManyWaypoints(num):
    vehicle_i = getInt("Enter the index of the vehicle (0 is first vehicle)")
    for i in range(1, num+1):
        createWaypoint(i, vehicle_i)


def createStartPoint():
    p=getPoint()
    vi = getInt("Enter vehicle index")

    sp = {}
    sp["type"]=VALID_MAP_OBJ["START_POINT"]
    sp["point"]=p
    sp["vehicle_i"]=vi
    global struc
    struc["StartPoint"+str(vi)]=sp

#writes struc to the provided file as JSON data
def writeToFile(filename):
    global struc
    with open(filename, "w") as outfile:
        enc=json.JSONEncoder()
        outfile.write(enc.encode(struc))
        



##############TODOS########
#in file
        #write objects in order they were added?
            #sorted dic, in AI project somewhere i think

#overall
#overall, need to specify that all area is not flight legal, except inside a legal fly zone
#figure out how to check zones etc
        
    
