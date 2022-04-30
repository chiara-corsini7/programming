#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:28:19 2022

@author: chiaracorsini
"""

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import numpy as np


def plot_cell(cell_vecs_x, cell_vecs_y, cell_vecs_z):
    
    a = cell_vecs_x
    b = cell_vecs_y
    c = cell_vecs_z
    
    x = [0, a[0], b[0], c[0], a[0]+b[0], c[0]+b[0], a[0]+c[0], a[0]+b[0]+c[0]]
    y = [0, a[1], b[1], c[1], a[1]+b[1], c[1]+b[1], a[1]+c[1], a[1]+b[1]+c[1]]
    z = [0, a[2], b[2], c[2], a[2]+b[2], c[2]+b[2], a[2]+c[2], a[2]+b[2]+c[2]]
    
    v=np.zeros((8,3))
    for i in range(8):
        v[i]=np.array([x[i],y[i],z[i]])
        
        #verts3D = [[v[0],v[1],v[4],v[2]] , [v[3],v[6],v[7],v[5]] , 
                   #[v[0],v[1],v[6],v[3]] , [v[0],v[2],v[5],v[3]] , 
                   #[v[1],v[6],v[7],v[4]] , [v[2],v[5],v[7],v[4]]]
        
    verts   = [[v[0],v[1],v[4],v[2],v[0]] , [v[3],v[6],v[7],v[5],v[3]] , 
               [v[0],v[1],v[6],v[3],v[0]] , [v[0],v[2],v[5],v[3],v[0]] , 
               [v[1],v[6],v[7],v[4],v[1]] , [v[2],v[5],v[7],v[4],v[4]]]
        
    verts=np.array(verts)
    return(verts)

def plot_molecule(a, b, c, el, cell_vecs_x, cell_vecs_y, cell_vecs_z):
    
    verts = plot_cell(cell_vecs_x, cell_vecs_y, cell_vecs_z)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')     
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    for i in range(6):
        ax.plot(verts[i][:,0],verts[i][:,1],verts[i][:,2], color='k')
    
    
    colors = [float(hash(i) % 256) / 256 for i in el] 
    
    
    ax.scatter3D(a, b, c, c=colors, cmap="jet", s=500)
        
#        for name in self.atoms_name:
#            ax.scatter3D(atx,aty,atz, s=100, label=name)
    #ax.legend()
    plt.show()
    #plt.savefig('iimmaaggee.png')