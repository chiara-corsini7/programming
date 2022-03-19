#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:12:35 2022

@author: chiaracorsini
"""

import numpy as np
import sys



def get_coords(data):
    
        
        el = data[:,0]
        a = data[:,1].astype(float)
        b = data[:,2].astype(float)
        c = data[:,3].astype(float)
        num_atom = len(el)
        
        print("Coordinates loaded")
        
        return el, a, b, c, num_atom



#def open_file():
    #inFile = sys.argv[1]
    #outFile = sys.argv[2]    
    
    #print(inFile)
    
data = np.genfromtxt('coordinate-001-H-prova.xyz', skip_header=3, dtype='str')
    #return data


    

        
        
        
        
        
##############################################################################
#########################   TESTING    #######################################
##############################################################################


import hypothesis
import pytest
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import hypothesis.extra.numpy as xnp



def test_get_coords(data):
    
    el, a, b, c, num_atom = get_coords(data)
    #test weather the input are the same length
    
    assert num_atom == len(a)
    assert num_atom == len(b)
    assert num_atom == len(c)

    
    
    
test_get_coords(data)  