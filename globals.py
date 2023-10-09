from math import pi

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Frames per second
FPS = 60

#window dimensions
WIDTH, HEIGHT = 800, 800

#Allow mouse input or not
ALLOW_MOUSE_INPUT = True

#connect all the points to eachother?
CONNECT_ALL = False

#for if its a rectangular prims with edges
RECT_WITH_EDGES = False

#angular velocity (radians per frame) --> FOR WHEN ALLOW_MOUSE_INPUT IS FALSE
ANG_VEL_X = (2 / 10) * (2 * pi / FPS) # (num_rotations / time) * (2pi/FPS)
ANG_VEL_Y = (2 / 10) * (2 * pi / FPS)
ANG_VEL_Z = (2 / 10) * (2 * pi / FPS)

#starting corner coordinates --> cube centered at (0, 0, 0)
ORIGIN = (0, WIDTH//2, HEIGHT//2)

#offset from origin
oX, oY, oZ = 0, 0, 0