#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:19:15 2022

@author: chiaracorsini
"""

import numpy as np


def get_data(data):
    el = data[:,0]
    a = data[:,1].astype(float)
    b = data[:,2].astype(float)
    c = data[:,3].astype(float)
    return(el, a, b, c)

def build_cell(cell_vec,a,b,c):
    cell_vec[0] = max(a)+15.
    cell_vec[1] = max(b)+15.
    cell_vec[2] = max(c)+15.
    return(cell_vec)

def angle_rad(cell_ang):
    for i in range(len(cell_ang)):
        cell_ang[i] *= np.pi/180
    return(cell_ang)