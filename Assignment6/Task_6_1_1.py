# -*- coding: utf-8 -*-

"""
Als Vorschlag für 6_1_1 gedacht. Basiert auf Repräsentation als numpy arrays
Funktioniert soweit, ist für die späteren Aufgaben aber vieleicht schlecht erweiterbar
Ob die numpy arrays hier überall Geschwindigkeit bringen ist fraglich
Matrixmultiplikation lies sich nur teilweise ausnutzen
TODO: diesen Kommentar für mögliche Abgabe entfernen
"""

import numpy as np
import math
import matplotlib

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
    return np.dot(np.dot(np.dot(coordSys,base),transJoint(l1,t1)),transJoint(l2,t2))

#Define the first 2 circular obstacles
o1 = Circle(np.array([270,620,1]),50)
o2 = Circle(np.array([250,200,1]),200)

#Stepsize for joint angle
resolution = 360
#initialize array beforehand
Cspace = np.zeros((resolution,resolution))
i = 0
for t1 in np.linspace(0,math.pi*2,resolution,False):
    j = 0
    for t2 in np.linspace(0,math.pi*2,resolution,False):
        #Calculate End Effector once, only last column needed for x,y coordinates
        curCartesianPosition = endEffPosition(t1,t2)[:,2]
        #TCP Missing?
        Cspace[i][j] = o1.pointInside(curCartesianPosition) + o2.pointInside(curCartesianPosition) * 0.5 #Scaling by 0.5 changes color in plot 
        j = j+1
    i= i+1
    
#plot as 2D color plot
matplotlib.pyplot.pcolor(Cspace)
    