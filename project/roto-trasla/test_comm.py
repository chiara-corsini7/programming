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
    """Generating parameters for tests"""
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


# @pytest.mark.parametrize('modnt', [np.array([10., 100., -20.]), 
#                                    np.array([0., 0., 0.])])
# @pytest.mark.parametrize('angle', [np.array([-0.5, 90., -97.]), 
#                                    np.array([0., 0., 0.])])
@pytest.mark.parametrize('var', [True, False])

# @pytest.mark.skip

def test_trasla_ruota(retreive_data, modnt, angle, var):
    
    if var == True:
        el_iniz, a_iniz, b_iniz, c_iniz = retreive_data
        angle_rad = dt.angle_rad(angle)
    
        a_rot, b_rot, c_rot = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)
        a_tr, b_tr, c_tr = fc.trasla(a_iniz, b_iniz, c_iniz, modnt)
    
        a_tr_rot, b_tr_rot, c_tr_rot = fc.ruota(a_tr, b_tr, c_tr, angle_rad, var)
        a_rot_tr, b_rot_tr, c_rot_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    
        np.testing.assert_array_almost_equal(a_rot_tr, a_tr_rot)
        np.testing.assert_array_almost_equal(b_rot_tr, b_tr_rot)
        np.testing.assert_array_almost_equal(c_rot_tr, c_tr_rot)
    else:
        pytest.skip("When not free molecule rot and translation are not commutative")



# @pytest.mark.parametrize('modnt', [np.array([10., 100., -20.]), 
#                                    np.array([0., 0., 0.])])
# @pytest.mark.parametrize('cell_vec', [np.array([1., 1., 1.])])
#                                     #np.array([900., 56., 23.])])

# @pytest.mark.parametrize('cell_ang', [np.array([90., 90., 90.]),
#                                   np.array([90., 30., 60.])])

# @pytest.mark.parametrize('modnre', [np.array([2, 2, 3])])#,
#                                     #np.array([2, 4, 5])])       
# @pytest.mark.skip
# @pytest.mark.skip

def test_trasla_replica(retreive_data, modnt, cell_vec, cell_ang, modnre):
    
    try:
        el_iniz, a_iniz, b_iniz, c_iniz = retreive_data
        angle_rad = dt.angle_rad(cell_ang)
    
        el_rep, a_rep, b_rep, c_rep = fc.replica(el_iniz, a_iniz, b_iniz, c_iniz, modnre, cell_vec, angle_rad)
        a_tr, b_tr, c_tr = fc.trasla(a_iniz, b_iniz, c_iniz, modnt)
    
        a_rep_tr, b_rep_tr, c_rep_tr = fc.trasla(a_rep, b_rep, c_rep, modnt)
        el_tr_rep, a_tr_rep, b_tr_rep, c_tr_rep = fc.replica(el_iniz, a_tr, b_tr, c_tr, modnre, cell_vec, angle_rad)
    
        np.testing.assert_array_almost_equal(a_rep_tr, a_tr_rep)
        np.testing.assert_array_almost_equal(b_rep_tr, b_tr_rep)
        np.testing.assert_array_almost_equal(c_rep_tr, c_tr_rep)

    except CE.NumbersOfReplicas:
        pytest.xfail('ValueError')
        pass
    except CE.SystemException:
        pytest.xfail('Exception')
        pass
    
# @pytest.mark.parametrize('modnt', [np.array([10., 100., -20.]), 
#                                     np.array([120., -1526243., 0.763536272])])
def test_trasla_inv(retreive_data, modnt):
    
    
    el, a_test, b_test, c_test = retreive_data
    
    modnt_inv = - modnt
    
    a_tr, b_tr, c_tr = fc.trasla(a_test, b_test, c_test, modnt)
    
    a_out, b_out, c_out = fc.trasla(a_tr, b_tr, c_tr, modnt_inv)
    
    np.testing.assert_array_almost_equal(a_out, a_test)
    np.testing.assert_array_almost_equal(b_out, b_test)
    np.testing.assert_array_almost_equal(c_out, c_test)
    

# @pytest.mark.parametrize('angle', [np.array([90., 90., 90.]), 
#                                     np.array([120., -1526243., 0.763536272])])
@pytest.mark.parametrize('var', [True, False])
def test_ruota_inv(retreive_data, var, angle):
    
    el, a_test, b_test, c_test = retreive_data
    angle_rad = dt.angle_rad(angle)
    angle_inv = - angle
    angle_rad_inv = dt.angle_rad(angle_inv)
    
    
    a_rot, b_rot, c_rot = fc.ruota(a_test, b_test, c_test, angle_rad, var)
    
    
    a_out1, b_out1, c_out1 = fc.ruota(a_rot, b_rot, c_rot, np.array([angle_rad_inv[0], 0., 0.]), var)
    a_out2, b_out2, c_out2 = fc.ruota(a_out1, b_out1, c_out1, np.array([0., angle_rad_inv[1], 0.]), var)
    a_out, b_out, c_out = fc.ruota(a_out2, b_out2, c_out2, np.array([0., 0., angle_rad_inv[2]]), var)
    
    np.testing.assert_array_almost_equal(a_out, a_test)
    np.testing.assert_array_almost_equal(b_out, b_test)
    np.testing.assert_array_almost_equal(c_out, c_test)

 

  
# @pytest.mark.parametrize('angle', [np.array([-0.5, 90., -97.])])#, 
#                                   # np.array([0., 0., 0.])])
# @pytest.mark.parametrize('var', [True, False])

# @pytest.mark.parametrize('cell_vec', [np.array([1., 1., 1.])])#,
#                                     #np.array([900., 56., 23.])])

# @pytest.mark.parametrize('cell_ang', [np.array([90., 90., 90.])])#,
#                                   #np.array([90., 30., 60.])])

# @pytest.mark.parametrize('modnre', [np.array([1, 2, 1])])#,
#                                     #np.array([2, 4, 5])])       

# def test_ruota_replica(retreive_data, angle, var, cell_vec, cell_ang, modnre):    
    
#     try:
#         if var == True:
            
#             el_iniz, a_iniz, b_iniz, c_iniz = retreive_data
#             cell_angle_rad = dt.angle_rad(cell_ang)
#             angle_rad = dt.angle_rad(angle)
            
#             #cell_vec_ruot = np.zeros(3)
            
#             el_rep, a_rep, b_rep, c_rep = fc.replica(el_iniz, a_iniz, b_iniz, c_iniz, modnre, cell_vec, cell_angle_rad)
#             #cell_vec_ruot[0], cell_vec_ruot[1], cell_vec_ruot[2] = fc.ruota(cell_vec[0], cell_vec[1], cell_vec[2], angle_rad, var)
#             a_rot, b_rot, c_rot = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)
        
#             a_rep_rot, b_rep_rot, c_rep_rot = fc.ruota(a_rep, b_rep, c_rep, angle_rad, var)
#             el_rot_rep, a_rot_rep, b_rot_rep, c_rot_rep = fc.replica(el_iniz, a_rot, b_rot, c_rot, modnre, cell_vec_ruot, cell_angle_rad)
        
#             np.testing.assert_array_almost_equal(a_rep_rot, a_rot_rep)
#             np.testing.assert_array_almost_equal(b_rep_rot, b_rot_rep)
#             np.testing.assert_array_almost_equal(c_rep_rot, c_rot_rep)
#             #np.testing.assert_array_almost_equal(el_rep, el_rot_rep)
            
#             # print('EL_INIZ', el_iniz)
#             # print('EL_REP', el_rep)
#             # print('EL_ROT_REP', el_rot_rep)
        
#         else:
#             pytest.skip("When not free molecule rot and translation are not commutative")
    
#     except ValueError:
#         pytest.xfail('ValueError')
#         pass
    
    
    
    
    
    