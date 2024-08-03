import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np



fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
fig.canvas.manager.set_window_title("Bertrand Paradox Simulator")

t = np.linspace(0, 2*np.pi, num=100)
circleX = np.cos(t)
circleY = np.sin(t)

for i in range(3):
    axs[i].plot(circleX, circleY, 'b')
    axs[i].set_box_aspect(1)
    axs[i].set_xlim([-1.1, 1.1])
    axs[i].set_ylim([-1.1, 1.1])

axs[0].set_title('Random Endpoints Method')
axs[1].set_title('Random Radial Point Method')
axs[2].set_title('Random Midpoint Method')

axs[2].plot(0.5*np.cos(t), 0.5*np.sin(t), 'k')

radial_point_method_radius, = axs[1].plot([], [], 'r')
endpoints_method_triangle, = axs[0].plot([], [], 'k')
radial_point_method_triangle, = axs[1].plot([], [], 'k')
endpoints_method_line, = axs[0].plot([], [], 'g')
radial_point_method_line, = axs[1].plot([], [], 'g')
midpoint_method_line, = axs[2].plot([], [], 'g')
endpoints_method_points_, = axs[0].plot([], [], 'm.')
radial_point_method_points, = axs[1].plot([], [], 'm.')
midpoint_method_points, = axs[2].plot([], [], 'm.')
endpoints_method_label = axs[0].text(1.2, 0.9, 'Success Rate: 0.0000')
radial_point_method_label = axs[1].text(1.2, 0.9, 'Success Rate: 0.0000')
midpoint_method_label = axs[2].text(1.2, 0.9, 'Success Rate: 0.0000')
endpoints_method_success = 0
radial_point_method_success = 0
midpoint_method_success = 0
trials = 0

def EndpointsMethodGet():
    generator = np.random.default_rng()
    points = generator.uniform(0, 2*np.pi, 2)
    return points

def RadialPointMethodGet():
    generator = np.random.default_rng()
    radiusangle = generator.uniform(0, 2*np.pi)
    point = generator.uniform(0, 1)
    return radiusangle, point

def MidpointMethodGet():
    generator = np.random.default_rng()
    point = generator.uniform(0, 1, 2)
    while np.linalg.norm(point) > 1.0:
        point = generator.uniform(0, 1, 2)
    return point

def EndpointsMethodPlot(line, plotpoints, triangle, points):
    point1 = [np.cos(points[0]), np.sin(points[0])]
    point2 = [np.cos(points[1]), np.sin(points[1])]
    xdata = [point1[0], point2[0]]
    ydata = [point1[1], point2[1]]
    
    trianglex = [np.cos(points[0]-2*np.pi/3), point1[0], np.cos(points[0]+2*np.pi/3), np.cos(points[0]-2*np.pi/3)]
    triangley = [np.sin(points[0]-2*np.pi/3), point1[1], np.sin(points[0]+2*np.pi/3), np.sin(points[0]-2*np.pi/3)]
    
    line.set_data(xdata, ydata)
    plotpoints.set_data(xdata, ydata)
    triangle.set_data(trianglex, triangley)
    return line

def RadialPointMethodPlot(radius, line, plotpoints, triangle, angle, dist):
    radiuspoint = [dist*np.cos(angle), dist*np.sin(angle)]
    triangleradiuspoint = [0.5*np.cos(angle), 0.5*np.sin(angle)]
    chordlength = np.sqrt(1 - np.square(dist))
    trianglelength = np.sqrt(1 - np.square(0.5))
    dir1 = angle + np.pi/2
    dir2 = angle - np.pi/2
    point1 = [radiuspoint[0]+chordlength*np.cos(dir1), radiuspoint[1]+chordlength*np.sin(dir1)]
    point2 = [radiuspoint[0]+chordlength*np.cos(dir2), radiuspoint[1]+chordlength*np.sin(dir2)]
    trianglepoint1 = [triangleradiuspoint[0]+trianglelength*np.cos(dir1), triangleradiuspoint[1]+trianglelength*np.sin(dir1)]
    trianglepoint2 = [triangleradiuspoint[0]+trianglelength*np.cos(dir2), triangleradiuspoint[1]+trianglelength*np.sin(dir2)]
    
    radiusx = [0, np.cos(angle)]
    radiusy = [0, np.sin(angle)]
    xdata = [point1[0], point2[0]]
    ydata = [point1[1], point2[1]]
    pointx = [radiuspoint[0]]
    pointy = [radiuspoint[1]]
    trianglex = [trianglepoint1[0], trianglepoint2[0]]
    triangley = [trianglepoint1[1], trianglepoint2[1]]
    
    plotpoints.set_data(pointx, pointy)
    radius.set_data(radiusx, radiusy)
    line.set_data(xdata, ydata)
    triangle.set_data(trianglex, triangley)
    return radius, line

def MidpointMethodPlot(line, plotpoints, point):
    angle = 0
    if point[0] == 0 and point[1] >= 0:
        angle = np.pi/2
    elif point[0] == 0 and point[1] < 0:
        angle = 3*np.pi/2
    else:
        angle = np.arctan(point[1]/point[0])
    
    dist = np.linalg.norm(point)
    chordlength = np.sqrt(1 - np.square(dist))
    dir1 = angle + np.pi/2
    dir2 = angle - np.pi/2
    point1 = [point[0]+chordlength*np.cos(dir1), point[1]+chordlength*np.sin(dir1)]
    point2 = [point[0]+chordlength*np.cos(dir2), point[1]+chordlength*np.sin(dir2)]
    
    xdata = [point1[0], point2[0]]
    ydata = [point1[1], point2[1]]
    pointx = [point[0]]
    pointy = [point[1]]
    
    plotpoints.set_data(pointx, pointy)
    line.set_data(xdata, ydata)
    return line

def UpdateSuccess(endpoints_method_data, radial_point_method_data, midpoint_method_data):
    global trials
    trials += 1
    
    if np.abs(endpoints_method_data[0]-endpoints_method_data[1]) >= 2*np.pi/3 and np.abs(endpoints_method_data[0]-endpoints_method_data[1]) <= 4*np.pi/3:
        global endpoints_method_success
        endpoints_method_success += 1
    
    if radial_point_method_data <= 0.5:
        global radial_point_method_success
        radial_point_method_success += 1
    
    if np.linalg.norm(midpoint_method_data) <= 0.5:
        global midpoint_method_success
        midpoint_method_success += 1
    
    endpoints_method_label.set_text(f'Success Rate: {endpoints_method_success/trials:.4f}')
    radial_point_method_label.set_text(f'Success Rate: {radial_point_method_success/trials:.4f}')
    midpoint_method_label.set_text(f'Success Rate: {midpoint_method_success/trials:.4f}')
    return

def animate(i):
    endpoints_method_points = EndpointsMethodGet()
    radial_point_method_angle, radial_point_method_dist = RadialPointMethodGet()
    midpoint_method_point = MidpointMethodGet()
    
    EndpointsMethodPlot(endpoints_method_line, endpoints_method_points_, endpoints_method_triangle, endpoints_method_points)
    RadialPointMethodPlot(radial_point_method_radius, radial_point_method_line, radial_point_method_points, radial_point_method_triangle, radial_point_method_angle, radial_point_method_dist)
    MidpointMethodPlot(midpoint_method_line, midpoint_method_points, midpoint_method_point)
    UpdateSuccess(endpoints_method_points, radial_point_method_dist, midpoint_method_point)
    
    return

anim = animation.FuncAnimation(fig, animate, interval=1000)
plt.tight_layout()
plt.show()