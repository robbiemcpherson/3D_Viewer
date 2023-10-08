import math as m

def SPHERE(n, radius):
    points = []
    
    # Calculate the angle increment for latitude and longitude
    phi_increment = m.pi / n
    theta_increment = 2 * m.pi / n

    for i in range(n):
        for j in range(n):
            # Calculate latitude (phi) and longitude (theta) for this point
            phi = i * phi_increment - m.pi / 2  # Range from -pi/2 to pi/2
            theta = j * theta_increment  # Range from 0 to 2*pi

            # Convert spherical coordinates to Cartesian coordinates
            x = radius * m.cos(phi) * m.cos(theta)
            y = radius * m.cos(phi) * m.sin(theta)
            z = radius * m.sin(phi)

            points.append([x, y, z])

    return points

def RECTANGLE(length, width, height, spacing = 10, edges = False):
    if edges:
        global RECT_WITH_EDGES
        RECT_WITH_EDGES = True
        #coordinates for a rectangular prism with side lengths defined above
        points = [[length//2, width//2, height//2], #front, right, bottom
                  [length//2, width//2, - height//2], #front, right, top
                  [length//2, - width//2, height//2], #front, left, bottom
                  [length//2, - width//2, - height//2], #front , left, top
                  [- length//2, width//2, height//2], #back, right, bottom
                  [- length//2, width//2, - height//2], #back, right, top
                  [- length//2, - width//2, height//2], #back, left, bottom
                  [- length//2, - width//2, - height//2]] #back, left, top
        return points
    
    points = []

    for x in range(-length//2, length//2+1, spacing):
        for y in range(-width//2, width//2+1, spacing):
            for z in range(-height//2, height//2+1, spacing):
                points.append([x, y, height//2])
                points.append([x, y, -height//2])
                points.append([x, width//2, z])
                points.append([x, -width//2, z])
                points.append([length//2, y, z])
                points.append([-length//2, y, z])

    return points

def BALL_TRAJECTORY(speed, h1, angle, dt, g= 9.8):
    """parameters all in SI units. Angle in degrees. Scale is 20 pixels per meter"""
    g *= -100 #m/s^2 --> pixels/s^2
    vel = (speed*100*m.cos(angle*m.pi/180), speed*100*m.sin(angle*m.pi/180))
    h1 *= 100

    time = (-vel[1]+m.sqrt((vel[1])**2-2*g*h1))/(g)
    if time < 0:
        time = (-vel[1]-m.sqrt((vel[1])**2-2*g*h1))/(g)

    print(time)
    points = []

    t=0
    while t<time:
        points.append([0, vel[0]*t, -1*(0.5*g*t**2 + vel[1]*t+h1)])
        t+= dt

    for x in range(int(-vel[0]*time),int(vel[0]*time), 40):
        for y in range(int(-vel[0]*time),int(vel[0]*time), 40):
            points.append([x, y, 0])
    return points


def function(z="m.sqrt(-x**2-y**2+16)", spacing=0.2, bounds=10, plusMinus=False, scale=100):
    points = []

    x=-bounds//2
    y=-bounds//2
    while x<=bounds//2:
        while y<=bounds//2:
            try:   
                points.append([int(scale*x), int(scale*y), -int(scale*eval(z))])
                if plusMinus:
                    points.append([int(scale*x), int(scale*y), int(scale*eval(z))])
            except:
                pass
            y+=spacing
        x+=spacing
        y=-bounds//2


    return points
