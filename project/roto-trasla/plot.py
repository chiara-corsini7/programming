#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:28:19 2022

@author: chiaracorsini
"""

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


    
    

def plot_molecule(a, b, c, el):
    fig = plt.figure()
    ax = plt.axes(projection='3d')     
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    
    colors = [float(hash(i) % 256) / 256 for i in el] 
    
    
    ax.scatter3D(a, b, c, c=colors, cmap="jet", s=500)
        
#        for name in self.atoms_name:
#            ax.scatter3D(atx,aty,atz, s=100, label=name)
    #ax.legend()
    plt.show()
    #plt.savefig('iimmaaggee.png')