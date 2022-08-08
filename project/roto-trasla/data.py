#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:19:15 2022

@author: chiaracorsini
"""

import numpy as np


def get_data(data):
    """This function creates the vectors containing elements and coordinates from data file
        
    Parameters:
         data: Natomsx4 string array containing elements and coordinates
        
        
    Returns: 4 Natomsx1 vectors 
         el: string array of elements
         a: float array of x coordinates
         b: float array of y coordinates
         c: float array of z coordinates
        """ 
    
    el = data[:,0]
    a = data[:,1].astype(float)
    b = data[:,2].astype(float)
    c = data[:,3].astype(float)
    
    return(el, a, b, c)

def build_cell(cell_vec,a,b,c):
    """This function builds the default cell vectors in case no cell vectors are entered
    
    Parameters:
         cell_vec: 3x1 zeros float array 
         a: float array of x coordinates
         b: float array of y coordinates
         c: float array of z coordinates
        
    Returns: 
        3x1 float array containing cell vectors 15 Angs greater than molecule
        """ 
    
    cell_vec[0] = max(a)+15.
    cell_vec[1] = max(b)+15.
    cell_vec[2] = max(c)+15.
    
    return(cell_vec)

def angle_rad(cell_ang):
    """This function turns angles in degrees to radians
    
    Parameters:
         cell_ang: 3x1 float array of angles in degrees
        
    Returns: 
        3x1 float array of angles in radians
        
        """ 
    new_ang = np.zeros(len(cell_ang))
    for i in range(len(cell_ang)):
        new_ang[i] = cell_ang[i]*np.pi/180
        
    return(new_ang)