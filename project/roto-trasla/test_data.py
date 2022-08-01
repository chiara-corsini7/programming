#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:47:35 2022

@author: chiaracorsini
"""

import pytest
#import glob
#import functions as fc
import data as dt
import numpy as np


@pytest.mark.parametrize('angle', [np.array([2., 7., 20.]), 
                                   np.array([-10., 70000., 0.])])
def test_angle_rad(angle):
    ''' Checking that the function angle_rad transforms the angles into radians'''
    
    angle_test=np.zeros(len(angle))
    for i in range(len(angle)):
        angle_test[i] = angle[i]*np.pi/180
        
    anglerad = dt.angle_rad(angle)
    
    
    np.testing.assert_array_almost_equal(anglerad, angle_test)   
   
 
    
# @pytest.mark.parametrize('angle', [np.array([90., 90., 90.]), 
#                                    np.array([45., 45., 0.])])
# def test_angle_deg(angle):
    
#     print('ANGLE IN', angle)
#     anglerad = dt.angle_rad(angle)
#     print('ANGLE RAD', anglerad)
#     angle_test = np.zeros(len(anglerad))
    
#     for i in range(len(anglerad)):
#         angle_test[i] = anglerad[i]*180/np.pi
#     print('ANGLE DEG', angle_test)
    
    
#     np.testing.assert_array_almost_equal(angle_test, angle)
    
