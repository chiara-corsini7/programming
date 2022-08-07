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
import CustomError as CE

def pytest_generate_tests(metafunc):
    """Generating parameters for tests:
        -> List of .xyz test files
        -> Random 3x1 float array with angles for rotations
        -> Random 3x1 float array with vector for rtranslations
        -> Random 3x1 float array with cell vectors
        -> Random 3x1 float array with cell angles [0,180)
        -> Random 3x1 positive integer array with number of replicas 
    """
    
    if "fileName" in metafunc.fixturenames:
        filelist = glob.glob('test-files/*.xyz')
        metafunc.parametrize("fileName", filelist )
    if "angle" in metafunc.fixturenames:
        rd_angle = np.random.uniform(-360.,360., 3)
        metafunc.parametrize('angle', [rd_angle])
    if "modnt" in metafunc.fixturenames:
        rd_modnt = np.random.uniform(-100000.,100000., 3)
        metafunc.parametrize('modnt', [rd_modnt])
    if "cell_vec" in metafunc.fixturenames:
        rd_cell_vec = np.random.uniform(-10.,100., 3)
        metafunc.parametrize('cell_vec', [rd_cell_vec])
    if "cell_ang" in metafunc.fixturenames:
        rd_cell_ang = np.random.uniform(0.,180., 3)
        metafunc.parametrize('cell_ang', [rd_cell_ang])
    if "modnre"  in metafunc.fixturenames:
        rd_modnre = np.random.randint(1, 3, 3)
        metafunc.parametrize('modnre', [rd_modnre])
        
@pytest.fixture  
def retreive_data(fileName):
    """Get data from .xyz files"""
    data = np.genfromtxt(fileName, skip_header=2, dtype='str')
    el = data[:,0]
    a = data[:,1].astype(float)
    b = data[:,2].astype(float)
    c = data[:,3].astype(float)
    return(el, a, b, c)



@pytest.mark.parametrize('var', [True, False])
def test_trasla_ruota(retreive_data, modnt, angle, var):
    """
    GIVEN: Test .xyz files and random translation vector modnt and rotation angles and var==True
    
    WHEN: Function trasla and ruota are applied subsequently
    
    THEN: They commute
    
    """
    
    
    if var == True:
        
        # GIVEN
        
        el_iniz, a_iniz, b_iniz, c_iniz = retreive_data
        angle_rad = dt.angle_rad(angle)
        
        # WHEN
        
        a_rot, b_rot, c_rot = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)
        a_tr, b_tr, c_tr = fc.trasla(a_iniz, b_iniz, c_iniz, modnt)
    
        a_tr_rot, b_tr_rot, c_tr_rot = fc.ruota(a_tr, b_tr, c_tr, angle_rad, var)
        a_rot_tr, b_rot_tr, c_rot_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
        
        #THEN
        
        np.testing.assert_array_almost_equal(a_rot_tr, a_tr_rot)
        np.testing.assert_array_almost_equal(b_rot_tr, b_tr_rot)
        np.testing.assert_array_almost_equal(c_rot_tr, c_tr_rot)
        
    # skipping test for var==False since makes ruota not to commute
    else:
        pytest.skip("When not free molecule rot and translation are not commutative")




def test_trasla_replica(retreive_data, modnt, cell_vec, cell_ang, modnre):
    
    """
    GIVEN: Test .xyz files and random translation vector modnt and 
           number of replicas and cell vector and angle
    
    WHEN: Function trasla and replica are applied subsequently
    
    THEN: They commute
    
    """
    
    try:
        
        # GIVEN
        
        el_iniz, a_iniz, b_iniz, c_iniz = retreive_data
        angle_rad = dt.angle_rad(cell_ang)
        
        # WHEN
    
        el_rep, a_rep, b_rep, c_rep = fc.replica(el_iniz, a_iniz, b_iniz, c_iniz, modnre, cell_vec, angle_rad)
        a_tr, b_tr, c_tr = fc.trasla(a_iniz, b_iniz, c_iniz, modnt)
    
        a_rep_tr, b_rep_tr, c_rep_tr = fc.trasla(a_rep, b_rep, c_rep, modnt)
        el_tr_rep, a_tr_rep, b_tr_rep, c_tr_rep = fc.replica(el_iniz, a_tr, b_tr, c_tr, modnre, cell_vec, angle_rad)
        
        # THEN
        
        np.testing.assert_array_almost_equal(a_rep_tr, a_tr_rep)
        np.testing.assert_array_almost_equal(b_rep_tr, b_tr_rep)
        np.testing.assert_array_almost_equal(c_rep_tr, c_tr_rep)

    # Raising exceptions for wrong cell angles or too large systems
    except CE.NumbersOfReplicas:
        pytest.xfail('ValueError')
        pass
    except CE.SystemException:
        pytest.xfail('Exception')
        pass
    

def test_trasla_inv(retreive_data, modnt):
    """
    GIVEN: Test .xyz files and random translation vector modnt and its inverse -modnt
    
    WHEN: Function trasla is applied and then invertedly applied
    
    THEN: Original coordinates are obtained
    
    """
    
    # GIVEN
    
    el, a_test, b_test, c_test = retreive_data
    modnt_inv = - modnt
    
    # WHEN
    
    a_tr, b_tr, c_tr = fc.trasla(a_test, b_test, c_test, modnt)
    
    a_out, b_out, c_out = fc.trasla(a_tr, b_tr, c_tr, modnt_inv)
    
    # THEN
    
    np.testing.assert_array_almost_equal(a_out, a_test)
    np.testing.assert_array_almost_equal(b_out, b_test)
    np.testing.assert_array_almost_equal(c_out, c_test)
    


@pytest.mark.parametrize('var', [True, False])
def test_ruota_inv(retreive_data, var, angle):
    """
    GIVEN: Test .xyz files and random rotation angles and their inverse -angle
    
    WHEN: Function ruota is applied and then invertedly applied
    
    THEN: Original coordinates are obtained
    
    """
    
    # GIVEN
    
    el, a_test, b_test, c_test = retreive_data
    angle_rad = dt.angle_rad(angle)
    angle_inv = - angle
    angle_rad_inv = dt.angle_rad(angle_inv)
    
    # WHEN
    
    a_rot, b_rot, c_rot = fc.ruota(a_test, b_test, c_test, angle_rad, var)
    
    # rotation matrix in ruota is RxRyRz so the inverse is obtained by applying -(RzRyRx)
    
    a_out1, b_out1, c_out1 = fc.ruota(a_rot, b_rot, c_rot, np.array([angle_rad_inv[0], 0., 0.]), var)
    a_out2, b_out2, c_out2 = fc.ruota(a_out1, b_out1, c_out1, np.array([0., angle_rad_inv[1], 0.]), var)
    a_out, b_out, c_out = fc.ruota(a_out2, b_out2, c_out2, np.array([0., 0., angle_rad_inv[2]]), var)
    
    # THEN
    
    np.testing.assert_array_almost_equal(a_out, a_test)
    np.testing.assert_array_almost_equal(b_out, b_test)
    np.testing.assert_array_almost_equal(c_out, c_test)
    
@pytest.mark.parametrize('var', [True, False])
def test_ruota_xyz(retreive_data, var, angle):
    """
    GIVEN: Test .xyz files and random rotation angles 
    
    WHEN: Function ruota is applied and then singularly rotated in z,y and x
    
    THEN: Obtain correctly rotated coordinates
    
    """
    
    # GIVEN
    
    el, a_iniz, b_iniz, c_iniz = retreive_data
    angle_rad = dt.angle_rad(angle)

    # WHEN
    
    a_out, b_out, c_out = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)
    
    # rotation matrix in ruota is RxRyRz so I apply Rz then Ry then Rx since the matrices do not commute
    
    a_test1, b_test1, c_test1 = fc.ruota(a_iniz, b_iniz, c_iniz, np.array([0., 0., angle_rad[2]]), var)
    a_test2, b_test2, c_test2 = fc.ruota(a_test1, b_test1, c_test1, np.array([0., angle_rad[1], 0.]), var)
    a_test, b_test, c_test = fc.ruota(a_test2, b_test2, c_test2, np.array([angle_rad[0], 0., 0.]), var)
    
    # THEN
    
    np.testing.assert_array_almost_equal(a_out, a_test)
    np.testing.assert_array_almost_equal(b_out, b_test)
    np.testing.assert_array_almost_equal(c_out, c_test)

 

    
    
    