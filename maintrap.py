import Tkinter as tk
import t2
import trapzone
import shapely
import math
# import rospy
# from geometry_msgs.msg import Point


# Publish location of traps to ROS
# def talker(traps):
#     pub = rospy.Publisher('traps', Point, queue_size=10)
#     rospy.init_node('trap_talker', anonymous=True)
#     rate = rospy.Rate(10)  # 10hz
#     messages = []
#     for trap in traps:
#         message = Point(trap[0], trap[1], 0)
#     messages.append(message)
#
#     while not rospy.is_shutdown():
#         for msg in messages:
#             rospy.loginfo(msg)
#             pub.publish(msg)
#             rate.sleep()


def createTraps():
    option = input(
        "(1) Use existing map\n(2) Manually input map\n(3) Use default map (Which is map #3)\nChoose option: ")

    zone = []
    obstacles = []
    if option == 1:
        map = input("Which map? (1, 2, or 3): ")
        if map == 1:
            zone = [
                (0, 0),
                (200, 0),
                (200, 125),
                (0, 125)
            ]
            obstacles = [
                [
                    (35, 45),
                    (55, 45),
                    (55, 60),
                    (35, 60)
                ],
                [
                    (30, 95),
                    (40, 95),
                    (40, 105),
                    (30, 105)
                ],
                [
                    (100, 85),
                    (140, 85),
                    (140, 115),
                    (100, 115)
                ],
                [
                    (150, 30),
                    (160, 30),
                    (160, 40),
                    (150, 40)
                ]

            ]
        if map == 2:
            zone = [
                (0, 0),
                (200, 0),
                (250, 50),
                (175, 125),
                (150, 80),
                (0, 125)
            ]
##            obstacles = [
##                [
##                    (10, 65),
##                    (20, 65),
##                    (20, 75),
##                    (10, 75)
##                ],
##                [
##                    (30, 30),
##                    (50, 30),
##                    (50, 50),
##                    (30, 50)
##                ],
##                [
##                    (80, 55),
##                    (105, 55),
##                    (105, 80),
##                    (80, 80)
##                ],
##                [
##                    (145, 90),
##                    (160, 90),
##                    (160, 115),
##                    (145, 115)
##                ],
##                [
##                    (140, 30),
##                    (160, 30),
##                    (160, 50),
##                    (140, 50)
##                ]
##            ]
        if map == 3:
            zone = [
                (0, 0),
                (150, 0),
                (150, 125),
                (0, 125)
            ]
            obstacles = [
                [
                    (15, 25),
                    (35, 25),
                    (35, 45),
                    (15, 45)
                ],
                [
                    (40, 90),
                    (50, 90),
                    (50, 100),
                    (40, 100)
                ],
                [
                    (80, 50),
                    (90, 50),
                    (90, 60),
                    (80, 60)
                ],
                [
                    (105, 75),
                    (125, 75),
                    (125, 95),
                    (105, 95)
                ],
                [
                    (105, 15),
                    (145, 15),
                    (145, 35),
                    (105, 35)
                ]
            ]

    if option == 2:
        print("DEFINE FLY ZONE")
        num = input("How many points define the shape the of fly zone?\n(Rectangle = 4, Triangle = 3, etc.): ")
        for i in range(1, num + 1):
            tuple = input("Point " + str(i) + " (x,y): ")
            zone = zone + [tuple]

        new = raw_input("New obstacle? (y/n): ")
        while new == "y":
            obstacle = []
            num = input("How many points?: ")
            for i in range(1, num + 1):
                tuple = input("Point " + str(i) + " (x,y): ")
                obstacle = obstacle + [tuple]
            obstacles = obstacles + [obstacle]
            new = raw_input("New obstacle? (y/n): ")

    if option == 3:
        zone = [
            (0, 0),
            (150, 0),
            (150, 125),
            (0, 125)
        ]
        obstacles = [
            [
                (15, 25),
                (35, 25),
                (35, 45),
                (15, 45)
            ],
            [
                (40, 90),
                (50, 90),
                (50, 100),
                (40, 100)
            ],
            [
                (80, 50),
                (90, 50),
                (90, 60),
                (80, 60)
            ],
            [
                (105, 75),
                (125, 75),
                (125, 95),
                (105, 95)
            ],
            [
                (105, 15),
                (145, 15),
                (145, 35),
                (105, 35)
            ]
        ]
    print "transforming zone"


    ros_response = raw_input('Do you want to publish to ROS [y/n]: ')
    # if ros_response == "y":
    #     talker(traps)  # Publishing to ROS


def place_traps(zone, obstacles, radius, buffer_amt):
    zone = shapely.geometry.Polygon(zone)
    obstacles = [shapely.geometry.Polygon(o) for o in obstacles]
    obstacles1 = []
    zone1 = zone
    if buffer_amt:
        erode = True

        zone1 = zone.buffer(-1 * abs(buffer_amt))
        for obstacle in obstacles:
            obstacles1 = obstacles1 + [obstacle.buffer(abs(buffer_amt))]

        tz = trapzone.TrapZone(zone1, obstacles1, radius)
    else:
        tz = trapzone.TrapZone(zone, obstacles, radius)



    # Store the corners of the buffered square
    bounds1 = zone1.bounds
    rect1 = shapely.geometry.Polygon(
        [
            (bounds1[0], bounds1[1]),
            (bounds1[0], bounds1[3]),
            (bounds1[2], bounds1[3]),
            (bounds1[2], bounds1[1])
        ]
    )

    # Obtain the locations of the traps
    traps, trap_points = tz.genPoints()

    # Prepare the window that will display the map
    root = tk.Tk()
    canvas = tk.Canvas(root, width=220, height=220, highlightthickness=0, bg="white")
    canvas.pack()

    # Display the points in the window
    t2.draw_poly(rect1, canvas, 'black')
    t2.draw_poly(zone, canvas, 'red')
    t2.draw_poly(zone1, canvas, 'yellow')
    for obstacle in obstacles1:
        t2.draw_poly(obstacle, canvas, 'black')
    for obstacle in obstacles:
        t2.draw_poly(obstacle, canvas, 'blue')
    trapzone.drawPoints(canvas, traps, 3, 'green')

    root.mainloop()

    return trap_points


if __name__ == '__main__':
    createTraps()
