#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 16:06:58 2022

@author: chiaracorsini
"""

import pytest
import glob
import functions as fc
import data as dt
import numpy as np

def pytest_generate_tests(metafunc):
    """Generating parameters for tests"""
    if "fileName" in metafunc.fixturenames:
        filelist = glob.glob('test-files/*.xyz')
        metafunc.parametrize("fileName", filelist )
        
@pytest.fixture  
def retreive_data(fileName):
    """Get data from .xyz files"""
    data = np.genfromtxt(fileName, skip_header=2, dtype='str')
    el = data[:,0]
    a = data[:,1].astype(float)
    b = data[:,2].astype(float)
    c = data[:,3].astype(float)
    return(el, a, b, c)


@pytest.mark.parametrize('modnt', [np.array([2., 7., 20.])])#, 
                                   #np.array([-10., 70000., 0.])])
@pytest.mark.parametrize('angle', [np.array([2., 7., 20.])])#, 
                                   #np.array([-10., 70000., 0.])])
@pytest.mark.parametrize('var', [True, False])
def test_trasla_ruota(retreive_data, modnt, angle, var):
    
    if var == True:
        el, a_iniz, b_iniz, c_iniz = retreive_data
        angle_rad = dt.angle_rad(angle)
    
        a_rot, b_rot, c_rot = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)
        a_tr, b_tr, c_tr = fc.trasla(a_iniz, b_iniz, c_iniz, modnt)
    
        a_rot_tr, b_rot_tr, c_rot_tr = fc.ruota(a_tr, b_tr, c_tr, angle_rad, var)
        a_tr_rot, b_tr_rot, c_tr_rot = fc.trasla(a_rot, b_rot, c_rot, modnt)
    
        np.testing.assert_array_almost_equal(a_rot_tr, a_tr_rot)
        np.testing.assert_array_almost_equal(b_rot_tr, b_tr_rot)
        np.testing.assert_array_almost_equal(c_rot_tr, c_tr_rot)
    else:
        pytest.skip("When not free molecule rot and translation are not commutative")
    
    
    
    
    
    
    
    
    
    
    