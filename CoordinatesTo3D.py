import pygame as pg
import math as m
import shapes
from globals import *
pg.init()

"""
note: for axis --> x is out of screen, y is to the right, z is down (because of pygame)
"""

#------------------------------------------------------------
def main():
    
    global COORDINATES
    global MAX_DIST_FROM_ORIGIN
    global WIN
    
    """----DEFINE THE SHAPE OF 3D OBJECTS----"""
    COORDINATES = shapes.FUNCTION() 
    
    #allows for object to be translated in x, y, z and still rotate about the origin
    adjust_coordinates_to_origin(oX, oY, oZ)

    MAX_DIST_FROM_ORIGIN = get_max_from_origin()

    mousePosNow = pg.mouse.get_pos()
    mousePosLast = pg.mouse.get_pos()

    holding = False # track whether or not the mouse button is being held down

    #INITIALIZE PYGAME WINDOW AND START CLOCK
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("3D Viewer")
    clock = pg.time.Clock()

    #MAIN LOOP
    while(True):
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                holding = True
                mousePosNow=pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONUP:
                holding = False
            if event.type == pg.MOUSEWHEEL:
                zoom(event.y)
        
        if ALLOW_MOUSE_INPUT:
            #track the change in mouse position while it is being held down
            if holding:
                mousePosLast = mousePosNow
                mousePosNow = pg.mouse.get_pos()

            #rotates based of change in mouse position, after hold it continues with whatever the last speed was
            rotate_Y(m.atan((mousePosNow[1]-mousePosLast[1])/(WIDTH/2)))
            rotate_Z(m.atan((mousePosNow[0]-mousePosLast[0])/(WIDTH/2)))

        else: #if mouse input was not allowed, the object is rotated based off parameters
            rotate_X()
            rotate_Y()
            rotate_Z()
        
        update_display()

def update_display():
    """re-draws all points, lines, etc."""
    
    WIN.fill(BLACK)

    WIN.set_at((ORIGIN[1], ORIGIN[2]), WHITE) # --> marks origin with single white pixel

    draw_points()

    if RECT_WITH_EDGES:
        connect_corners()
    elif CONNECT_ALL:
        connect_everything()

    pg.display.update()


def rotate_X(angle = ANG_VEL_X):
    """rotate about x axis (out of screen)"""
    a, b = ORIGIN[1], ORIGIN[2]

    for point in COORDINATES:
        point[1], point[2] = (point[1]-a)*m.cos(angle)-(point[2]-b)*m.sin(angle)+a, (point[2]-b)*m.cos(angle)+(point[1]-a)*m.sin(angle)+b

def rotate_Y(angle = ANG_VEL_Y):
    """rotate about y axis (horizontal)"""
    a, b = ORIGIN[0], ORIGIN[2]
    
    for point in COORDINATES:
        point[0], point[2] = (point[0]-a)* m.cos(angle)-(point[2]-b)*m.sin(angle)+a, (point[2]-b)* m.cos(angle)+(point[0]-a)*m.sin(angle)+b

def rotate_Z(angle = ANG_VEL_Z):
    """rotate about z axis (vertical)"""
    a, b = ORIGIN[0], ORIGIN[1]

    for point in COORDINATES:
        point[0], point[1] = (point[0]-a)* m.cos(angle)-(point[1]-b)*m.sin(angle)+a, (point[1]-b)* m.cos(angle)+(point[0]-a)*m.sin(angle)+b

def adjust_coordinates_to_origin(x=0, y=0, z=0):
    """aligns coordinates origin with display origin and allows for offsets"""
    for point in COORDINATES:
        point[0] += ORIGIN[0]+x
        point[1] += ORIGIN[1]+y
        point[2] += ORIGIN[2]+z

def draw_points():
    """Draws all the points from back to front and makes closer points brighter"""
    for point in quicksort(COORDINATES):
        x = (point[0]+MAX_DIST_FROM_ORIGIN)/(2*MAX_DIST_FROM_ORIGIN)*255
        pg.draw.circle(WIN, (x, x, x), (point[1], point[2]), 4)

def connect_corners():
    """only for rectangular prisms in specific coordinate format"""

    #lines from front, bottom, right point
    pg.draw.line(WIN, WHITE, pt_yz(0), pt_yz(1))
    pg.draw.line(WIN, WHITE, pt_yz(0), pt_yz(2))
    pg.draw.line(WIN, WHITE, pt_yz(0), pt_yz(4))

    #lines from front, top, left point
    pg.draw.line(WIN, WHITE, pt_yz(3), pt_yz(2))
    pg.draw.line(WIN, WHITE, pt_yz(3), pt_yz(1))
    pg.draw.line(WIN, WHITE, pt_yz(3), pt_yz(7))

    #lines from back, top, right point
    pg.draw.line(WIN, WHITE, pt_yz(5), pt_yz(4))
    pg.draw.line(WIN, WHITE, pt_yz(5), pt_yz(7))
    pg.draw.line(WIN, WHITE, pt_yz(5), pt_yz(1))

    #lines from back, bottom, left point
    pg.draw.line(WIN, WHITE, pt_yz(6), pt_yz(7))
    pg.draw.line(WIN, WHITE, pt_yz(6), pt_yz(4))
    pg.draw.line(WIN, WHITE, pt_yz(6), pt_yz(2))

def pt_yz(pt_index):
    """returns the (y, z) projection of the point at COORDINATES[n]"""
    return (COORDINATES[pt_index][1], COORDINATES[pt_index][2])

def connect_everything():
    """connects all points to eachother"""
    pairs = []
    for index1 in range(len(COORDINATES)):
        for index2 in range(len(COORDINATES)):
            if index1 != index2 and (index1, index2) not in pairs:
                pg.draw.line(WIN, WHITE, pt_yz(index1), pt_yz(index2))
                pairs.append([index1, index2])

    """connects all points on surface of sphere"""
    pairs = []
    for index1, pt1 in enumerate(COORDINATES):
        for index2, pt2 in enumerate(COORDINATES):
            if index1 != index2 and (index1, index2) not in pairs and (pt1[0]*pt2[0]+pt1[1]*pt2[1]+pt1[2]*pt2[2]) == 0:
                pg.draw.line(WIN, WHITE, pt_yz(index1), pt_yz(index2))
                pairs.append([index1, index2])

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2][0]
    left = [x for x in arr if x[0] < pivot]
    middle = [x for x in arr if x[0] == pivot]
    right = [x for x in arr if x[0] > pivot]
    
    return quicksort(left) + middle + quicksort(right)

def get_max_from_origin():
    maximum =0
    for point in COORDINATES:
        dist = m.sqrt((point[0]-ORIGIN[0])**2+(point[1]-ORIGIN[1])**2+(point[2]-ORIGIN[2])**2)
        if dist > maximum:
            maximum = dist

    return maximum

def zoom(direction):
    for point in COORDINATES:
        point[0] = (point[0]-oX-ORIGIN[0]) * (1+direction/10) + oX + ORIGIN[0]
        point[1] = (point[1]-oY-ORIGIN[1]) * (1+direction/10) + oY + ORIGIN[1]
        point[2] = (point[2]-oZ-ORIGIN[2]) * (1+direction/10) + oZ + ORIGIN[2]

    global MAX_DIST_FROM_ORIGIN
    MAX_DIST_FROM_ORIGIN =get_max_from_origin()


if __name__ == "__main__":
    main()