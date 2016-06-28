
import numpy as np
import matplotlib.pyplot as plt

#Recursive way to define a basis spline
def recBasisSpline(i,k,t):
    if k < 2:    #trivial case
        if t > i and t < (i+1):
            return 1
        else:
            return 0
    else:         #Tree recursion as described by slide 260
        return ((t-i)/(i+k-1-i)) * recBasisSpline(i,k-1,t) + ((i+k-t)/(i+k-(i+1))) * recBasisSpline(i+1,k-1,t)

#Create plot
for k in range(1,5):  #order 1 to 4
    x = np.linspace(0,5)  #time values from 0 to 5 given by numpy
    #Here, some magic happens
    #when we create a new function out of the recBasisSpline Function via lambda which only accepts one time value
    #while the rest of the arguments is set to our needs
    #then the function is applied to all time values in the list via map
    line, = plt.plot(x, list(map(lambda x: recBasisSpline(0,k,x),x)), '-', linewidth=1.5, label='order '+str(k)) #creation of line in the plot for bspline of order k
    
plt.legend()                    #Add the legend
plt.xlabel('time t')            #Add the xlabel
plt.ylabel('function value')    #Add the ylabel
#plt.show()                     #in case we directly want to see the plot
plt.savefig('Task_5_1.png')     #save the plot to .png
