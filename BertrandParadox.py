import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np



fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)

t = np.linspace(0, 2*np.pi, num=100)
circleX = np.cos(t)
circleY = np.sin(t)

for i in range(3):
    axs[i].plot(circleX, circleY, 'b')
    axs[i].set_box_aspect(1)
    axs[i].set_title(f'Method {i+1}')
    axs[i].set_xlim([-1.1, 1.1])
    axs[i].set_ylim([-1.1, 1.1])

line1, = axs[0].plot([], [], 'g')
line2, = axs[1].plot([], [], 'g')
radius2, = axs[1].plot([], [], 'r')
line3, = axs[2].plot([], [], 'g')
points1, = axs[0].plot([], [], 'm.')
points2, = axs[1].plot([], [], 'm.')
points3, = axs[2].plot([], [], 'm.')
label1 = axs[0].text(1.2, 0.9, 'Success Rate: 0.0')
label2 = axs[1].text(1.2, 0.9, 'Success Rate: 0.0')
label3 = axs[2].text(1.2, 0.9, 'Success Rate: 0.0')
success1 = 0
success2 = 0
success3 = 0
trials = 0

def MethodOneGet():
    generator = np.random.default_rng()
    points = generator.uniform(0, 2*np.pi, 2)
    return points

def MethodTwoGet():
    generator = np.random.default_rng()
    radiusangle = generator.uniform(0, 2*np.pi)
    point = generator.uniform(0, 1)
    return radiusangle, point

def MethodThreeGet():
    generator = np.random.default_rng()
    point = generator.uniform(0, 1, 2)
    while np.linalg.norm(point) > 1.0:
        point = generator.uniform(0, 1, 2)
    return point

def MethodOnePlot(line, points):
    xdata = [np.cos(points[0]), np.cos(points[1])]
    ydata = [np.sin(points[0]), np.sin(points[1])]
    
    line.set_data(xdata, ydata)
    return line

def MethodTwoPlot(radius, line, angle, dist):
    radiuspoint = [dist*np.cos(angle), dist*np.sin(angle)]
    chordlength = np.sqrt(1 - np.square(dist))
    dir1 = angle + np.pi/2
    dir2 = angle - np.pi/2
    point1 = [radiuspoint[0]+chordlength*np.cos(dir1), radiuspoint[1]+chordlength*np.sin(dir1)]
    point2 = [radiuspoint[0]+chordlength*np.cos(dir2), radiuspoint[1]+chordlength*np.sin(dir2)]
    
    radiusx = [0, np.cos(angle)]
    radiusy = [0, np.sin(angle)]
    xdata = [point1[0], radiuspoint[0], point2[0]]
    ydata = [point1[1], radiuspoint[1], point2[1]]
    
    radius.set_data(radiusx, radiusy)
    line.set_data(xdata, ydata)
    return radius, line

def MethodThreePlot(line, point):
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
    
    xdata = [point1[0], point[0], point2[0]]
    ydata = [point1[1], point[1], point2[1]]
    
    line.set_data(xdata, ydata)
    return line

def PlotPoints(line1, line2, line3):
    points1.set_data(line1.get_xdata(), line1.get_ydata())
    points2.set_data(line2.get_xdata(), line2.get_ydata())
    points3.set_data(line3.get_xdata(), line3.get_ydata())

def UpdateSuccess(data1, data2, data3):
    global trials
    trials += 1
    
    if np.abs(data1[0]-data1[1]) >= 2*np.pi/3 and np.abs(data1[0]-data1[1]) <= 4*np.pi/3:
        global success1
        success1 += 1
    
    if data2 <= 0.5:
        global success2
        success2 += 1
    
    if np.linalg.norm(data3) <= 0.5:
        global success3
        success3 += 1
    
    label1.set_text(f'Success Rate: {success1/trials}')
    label2.set_text(f'Success Rate: {success2/trials}')
    label3.set_text(f'Success Rate: {success3/trials}')
    return

def animate(i):
    method1points = MethodOneGet()
    method2angle, method2dist = MethodTwoGet()
    method3point = MethodThreeGet()
    
    MethodOnePlot(line1, method1points)
    MethodTwoPlot(radius2, line2, method2angle, method2dist)
    MethodThreePlot(line3, method3point)
    PlotPoints(line1, line2, line3)
    UpdateSuccess(method1points, method2dist, method3point)
    
    return

anim = animation.FuncAnimation(fig, animate, interval=500)
plt.tight_layout()
plt.show()