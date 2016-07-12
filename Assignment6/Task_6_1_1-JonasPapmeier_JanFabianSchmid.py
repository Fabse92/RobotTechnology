# -*- coding: utf-8 -*-

"""
Lösung basiert auf Repräsentation als numpy arrays
Funktioniert soweit, ist für die späteren Aufgaben aber vieleicht schlecht erweiterbar
Ob die numpy arrays hier überall Geschwindigkeit bringen ist fraglich, denn die
Matrixmultiplikation lies sich nur teilweise ausnutzen
"""

import functools
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

"""
Class to represent an circular object in space
"""
class Circle:
    def __init__(self, origin, radius):
        """
        Create a circle object at point origin with given radius
        params:
            origin: (x,y,scale) numpy array, the center point of the circle
            radius: int, the radius of the circle
        """
        self.origin = origin
        self.radius = radius
        
    def pointInside(self,point):
        """
        Check wether the point lies within the circle
        params:
            point: (x,y,scale) numpy array, the searched point
        return:
            int, 1 when eucleadian distance from point to circle center is < circle radius else 0
        """
        return 1 if self.radius > np.sqrt(np.sum(np.square(point-self.origin))) else 0
        
#Define a basis coordinate system
coordSys = np.array([[1,0,0],[0,1,0],[0,0,1]])

#Base of the robot
base = np.array([[1,0,500],[0,1,500],[0,0,1]])

#initial state for links, joints
#link lenght
l1 = 200
l2 = 200

#joint angle
t1 = 0
t2 = 0

#As the joints are parallel rotational joints they have the same transformation matrix ^i-1_T_i
#Thus 1 function is sufficient to calculate the current homogenous matrix as numpy array
def transJoint(l,t):
    """
    Calculate the homogenous transformation matrix for one joint
    params:
        l: int, lenght of joint
        t: int, rotation of joint as radian
    return:
        A numpy array representing the homogenous transformation matrix for the joint
    """
    return np.array([[math.cos(t),-math.sin(t),l1*math.cos(t)],[math.sin(t),math.cos(t),l*math.sin(t)],[0,0,1]])

def endEffPosition(t1,t2):
    """
    Calculate position of the end effector
    params:
        t1: int, angle of first joint
        t2: int, angle of second joint
    """
    return np.dot(np.dot(np.dot(coordSys,base),transJoint(l1,t1)),transJoint(l2,t2))

obstacles = []

#Define the first 2 circular obstacles
o1 = Circle(np.array([270,620,1]),50)
obstacles.append(o1)
o2 = Circle(np.array([250,200,1]),200)
obstacles.append(o2)

#Define the start and goal positions also as obstacles
#due to laziness and easy use
start = Circle(np.array([900,500,1]),10)
goal1 = Circle(np.array([580,150,1]),10)
goal2 = Circle(np.array([230,470,1]),10)
obstacles.append(start)
obstacles.append(goal1)
obstacles.append(goal2)


def plotCspace(figNum,resolution):
    """
    Plot the configuration space for the robot
    params:
        figNum: int, number of the figure to use
        resolution: int, angular resolution steps
    """
    #Stepsize for joint angle
    resolution_cs = resolution
    #initialize array beforehand
    Cspace = np.zeros((resolution_cs,resolution_cs))
    i = 0
    for t1 in np.linspace(0,math.pi*2,resolution_cs,False):
        j = 0
        for t2 in np.linspace(0,math.pi*2,resolution_cs,False):
            #Calculate End Effector once, only last column needed for x,y coordinates
            curCartesianPosition = endEffPosition(t1,t2)[:,2]
            #Assign each point of the Cspace matrix a value depending on the obstacles found at that point
            #for each object in the obstacle list a 1 or 0 is assigned via map if the point lies within the obstacle
            #with reduce the list is folded as a sum, x*2 creates different values for different obstacles, resulting in different colors
            #in the plot
            Cspace[i][j] = functools.reduce(lambda x, y: x*2+y,list(map(lambda o: o.pointInside(curCartesianPosition), obstacles)))
            j = j+1
        i= i+1
            
    #plot as 2D color plot
    fig = plt.figure(figNum)
    #Transpose as pcolor flips x and y
    plt.pcolor(Cspace.T)
    fig.savefig('Cspace.png')

def plotWspace(figNum,resolution,x,y):
    """
    Plot the workspace for the robot
    params:
        figNum: int, number of the figure to use
        resolution: int, resolution of the workspace
        x: int, size in x dimension
        y: int, size in y dimension
    """
    resolution_ws = resolution
    ws_bounds = (x,y)
    Wspace = np.zeros((resolution_ws,resolution_ws))
    i = 0
    for t1 in np.linspace(0,ws_bounds[0],resolution_ws,False):
        j = 0
        for t2 in np.linspace(0,ws_bounds[1],resolution_ws,False):
            Wspace[i][j] = functools.reduce(lambda x, y: x*2+y,list(map(lambda o: o.pointInside((t1,t2,1)), obstacles)))
            j = j+1
        i = i+1

    fig = plt.figure(figNum)
    plt.pcolor(Wspace.T)
    fig.savefig('Wspace.png')
    
