#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:28:19 2022

@author: chiaracorsini
"""

import matplotlib.pyplot as plt
import numpy as np

# plotting cell

def plot_cell(cell_vecs_x, cell_vecs_y, cell_vecs_z):
    """This function constructs the faces of the cell to be plotted
        
    Parameters:
        cell_vecs_x : 3x1 float array containing first row of unit cell matrix
        cell_vecs_y : 3x1 float array containing second row of unit cell matrix
        cell_vecs_z : 3x1 float array containing third row of unit cell matrix
        
    Returns:
        Matrix of faces aces of the unit cell
        """  
    
    a = cell_vecs_x
    b = cell_vecs_y
    c = cell_vecs_z
    
    # creating x, y and z coordinates for the cell vertices
    
    x = [0, a[0], b[0], c[0], a[0]+b[0], c[0]+b[0], a[0]+c[0], a[0]+b[0]+c[0]]
    y = [0, a[1], b[1], c[1], a[1]+b[1], c[1]+b[1], a[1]+c[1], a[1]+b[1]+c[1]]
    z = [0, a[2], b[2], c[2], a[2]+b[2], c[2]+b[2], a[2]+c[2], a[2]+b[2]+c[2]]
    
    # creating 8x3 matrix containing the xyz coordinates for each vertex
    
    v=np.zeros((8,3))
    for i in range(8):
        v[i]=np.array([x[i],y[i],z[i]])
        
    # Matrix of faces of unit cell 
    
    verts   = [[v[0],v[1],v[4],v[2],v[0]] , [v[3],v[6],v[7],v[5],v[3]] , 
               [v[0],v[1],v[6],v[3],v[0]] , [v[0],v[2],v[5],v[3],v[0]] , 
               [v[1],v[6],v[7],v[4],v[1]] , [v[2],v[5],v[7],v[4],v[4]]]
        
    verts=np.array(verts)
    return(verts)

def plot_molecule(a, b, c, el, cell_vecs_x, cell_vecs_y, cell_vecs_z):
    """This function plots the cell and the atoms form output
        
    Parameters:
        a, b, c : x, y, z coordinates of atoms
        el : atoms names
        cell_vecs_x : 3x1 float array containing first row of unit cell matrix
        cell_vecs_y : 3x1 float array containing second row of unit cell matrix
        cell_vecs_z : 3x1 float array containing third row of unit cell matrix
        
    Returns:
        plot of the final system
        """  
    
    verts = plot_cell(cell_vecs_x, cell_vecs_y, cell_vecs_z)
    
    ax = plt.axes(projection='3d')     
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # plotting the cell
    
    for i in range(6):
        ax.plot(verts[i][:,0],verts[i][:,1],verts[i][:,2], color='k')
    
    # creating colormap for atoms
    
    colors = [float(hash(i) % 256) / 256 for i in el] 
    
    # plotting atoms
    
    ax.scatter3D(a, b, c, c=colors, cmap="jet", s=300, depthshade=False)
        

    plt.show()
