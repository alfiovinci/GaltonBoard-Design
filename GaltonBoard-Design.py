#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:34:45 2022

@author: alfio
"""

import numpy as np
from random import randint
import matplotlib.pyplot as plt
# import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.patches import Circle
plt.close('all')

def galton(n_c, n_b):
    n_l = n_c-1
    containers = np.zeros((int(n_c),))
    for i in range(0,n_b):
        prob = []
        for j in range(0,n_l):
            prob.append(randint(0,1))
        index = sum(prob)
        containers[index] = containers[index]+1
    return containers

#_____________________________________________________________________
# Setting up the board useful size
w, h = 120, 150     # full board 2D size [mm]
#_____________________________________________________________________


#_____________________________________________________________________
# Setting up the spheres properties
N = 100         # numer of spheres
phi_b = 3       # sphere diameter [mm]
V_b = 4/3*np.pi*(phi_b/2)**3    # sphere volume [mm^3]

pack_factor = 0.64      # random sphere packing factor
#_____________________________________________________________________


#_____________________________________________________________________
# Setting up the containers properties
w_c = phi_b*2.5    # container width [mm]
d_c = 5         # container depth [mm]

t_wood = 3      # divider thickness

n_c = round((w+t_wood)/(w_c+t_wood))      # number of containers
#_____________________________________________________________________



#_____________________________________________________________________
# Computing containers height from simulations
max_num_balls = []
number_tests = 300
for i in range(0,number_tests):
    containers = galton(n_c, N)
    max_num_balls.append(np.max(containers))
    
sf = 1.1        # safety factor
h_c_min = round(sf*(np.max(max_num_balls)*V_b/pack_factor)/(w_c*d_c))       # containers height
h_c = round(h_c_min*sf)
#_______________________________________________________________________



#________________________________________________________________________
# Compute containers coordinates x and height of spheres stacks
x = np.linspace(w_c/2,w-w_c/2,len(containers))

y = containers/np.max(containers)*h_c_min

x_bars = x+w_c/2+t_wood/2
#________________________________________________________________________

          

#_______________________________________________________________________
# Compute dots coordinates

x_dots, y_dots = [], []
x_dots.append(x_bars[:-1])
y_dots.append(h_c+3)
gap_y = 8
while len(x_dots[-1]) > 1:
    y_dots.append(y_dots[-1]+gap_y)
    x_temp = []
    for i in range(1,len(x_dots[-1])):
        x_temp.append(x_dots[-1][i-1]+(x_dots[-1][i]-x_dots[-1][i-1])/2)
    x_dots.append(x_temp)
#________________________________________________________________________




#________________________________________________________________________
# Compute stock volume
h_stock = 2 * sf * V_b*N/(pack_factor*w*d_c)
#________________________________________________________________________

print("Number of channels = "+str(n_c))
print("Average max number of spheres: "+str(format(np.mean(max_num_balls),'.2f'))+", Max: "+str(np.max(max_num_balls))+", Min: "+str(np.min(max_num_balls)))
print("Containers min height: "+str(h_c_min)+" mm - Chosen: "+str(h_c)+' mm')




figure, ax = plt.subplots(figsize=(6,7))
ax.plot([w/2,w/2],[-10,h+10],'k',lw=0.5,ls='-.')
ax.add_patch(Rectangle((0,0),w,h,facecolor='lightgray',edgecolor='k'))

ax.add_patch(Rectangle((0,0),w,h_c,facecolor='gray',edgecolor='k'))


for i in range(0,len(x_dots)):
    for j in range(0,len(x_dots[i])):
        ax.add_patch(Circle((x_dots[i][j],y_dots[i]),radius=3,color='k'))

for i in range(0,len(containers)-1):
    ax.bar(x[i],y[i],width=w_c, color='g',edgecolor='k')
for i in range(0,len(containers)-1):
    ax.add_patch(Rectangle((x[i]+w_c/2,0),t_wood,h_c,facecolor='w',edgecolor='k'))


gauss = 1/np.sqrt(2*np.pi*n_c*0.5*0.5)*np.exp(-(np.linspace(0,n_c,int(n_c*10),endpoint=True)-n_c*0.5)**2/(2*n_c*0.5*0.5))
ax.plot(np.linspace(0,w,len(gauss)),gauss/np.max(gauss)*h_c_min*0.9,'-r',lw=2)


ax.set_xlim([0,130])
ax.set_ylim([0,180])
ax.set_xlabel('Width [mm]',fontsize=14)
ax.set_ylabel('Height [mm]',fontsize=14)
ax.axis('equal')

plt.show()