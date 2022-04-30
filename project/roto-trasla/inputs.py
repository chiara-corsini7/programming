#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:12:35 2022

@author: chiaracorsini
"""

import functions as fc
import plot as plot
import numpy as np
import argparse



parser = argparse.ArgumentParser(description='Translate Rotate and Clone molecular coordinates.')
parser.add_argument('-f','--file', action='store', 
                    help=".xyz file with coordinates", default='CO2.xyz', type=str)
parser.add_argument('-t','--translate', action='store', nargs=3, 
                    help="x y and z coordinates of translation vector in $\AA$,"\
                    " default 0. 0. 0.", default = [0.,0.,0.], type=float,
                    metavar=('dx', 'dy', 'dz'))
parser.add_argument('-r','--rotate', action='store', nargs=3, 
                    help="x y and z rotations in degrees,"\
                    "default 0. 0. 0.", default =[0.,0.,0.], type=float,
                    metavar=('rotx', 'roty', 'rotz'))
parser.add_argument('-c','--clone', action='store', nargs=3, 
                    help="Number of replicas in x y and z,"\
                    "default 1 1 1", default =[1,1,1], type=int,
                    metavar=('repx', 'repy', 'repz'))
parser.add_argument('-v','--vectors', action='store', nargs=3, 
                    help="a b and c unit cell vectors,"\
                    "unit cell vectors of 15 Angs side greater than molecule are default", default =[0.,0.,0.], type=float,
                    metavar=('a', 'b', 'c'))
parser.add_argument('-a','--angles', action='store', nargs=3, 
                    help="$\alpha$ $\beta$ and $\gamma$ unit cell angles in degrees,"\
                    "orthorombic cell is default (90. 90. 90.)", default =[90.,90.,90.], type=float,
                    metavar=('$\alpha$', '$\beta$', '$\gamma$'))
        
args = parser.parse_args()



#def treat_input(args):
    # retrieviebìng 
modnt = np.array(args.translate)
modnr = np.array(args.rotate)
modnre = np.array(args.clone)
cell_vec = np.array(args.vectors)
cell_ang = np.array(args.angles)
data = np.genfromtxt(args.file, skip_header=1, dtype='str')

    
    
el = data[:,0]
a = data[:,1].astype(float)
b = data[:,2].astype(float)
c = data[:,3].astype(float)

if (cell_vec==np.array([0.,0.,0.])).all():
    cell_vec[0] = max(a)+15.
    cell_vec[1] = max(b)+15.
    cell_vec[2] = max(c)+15.
    
    
for i in range(len(cell_ang)):
    cell_ang[i] *= np.pi/180


    
print('Selected file: %s' % args.file)
print('TRANSLATION %s in $\AA$' % modnt)
print('ROTATION %s' % modnr)
print('REPLICAS %s' % modnre)
print('ELEMENTS %s' % el)
print ('COORD X %s' % a)
print ('COORD y %s' % b)
print ('COORD z %s' % c)
print ('Cell vectors %s' %cell_vec)
print ('Cell angles %s' %cell_ang)
    
if (modnt==np.array([0.,0.,0.])).all() & (modnr==np.array([0.,0.,0.])).all() & (modnre==np.array([1, 1, 1])).all():
    print('Not translating nor rotating nor cloning the molecule')
elif (modnt==np.array([0.,0.,0.])).all() & (modnre==np.array([1, 1, 1])).all():
    print('Only rotating the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    a = a_rot
    b = b_rot
    c = c_rot
elif (modnr==np.array([0.,0.,0.])).all() & (modnre==np.array([1, 1, 1])).all():
    print('Only translating the molecule')
    a_tr, b_tr, c_tr = fc.trasla(a, b, c, modnt)
    a = a_tr
    b = b_tr
    c = c_tr
elif (modnt==np.array([0.,0.,0.])).all() & (modnr==np.array([0.,0.,0.])).all():
    print('Only cloning the molecule')
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a, b, c, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep
elif (modnre==np.array([1, 1, 1])).all():
    print('Roto-translating the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    a_tr, b_tr, c_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    a = a_tr
    b = b_tr
    c = c_tr
elif (modnr==np.array([0., 0., 0.])).all():
    print('Translating and cloning the molecule')
    a_tr, b_tr, c_tr = fc.trasla(a, b, c, modnt)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_tr, b_tr, c_tr, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep
elif (modnt==np.array([0., 0., 0.])).all():
    print('Rotating and cloning the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_tr, b_tr, c_tr, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep
    
else:
    print('Roto-translating and cloning the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    a_tr, b_tr, c_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_tr, b_tr, c_tr, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep

print ('new elements %s' % el)
print ('new COORD X %s' % a)
print ('new COORD y %s' % b)
print ('new COORD z %s' % c)


cell_vecs_x, cell_vecs_y, cell_vecs_z = fc.cell(cell_vec, cell_ang)    
plot.plot_molecule(a, b, c, el, cell_vecs_x, cell_vecs_y, cell_vecs_z)
    

#print("Coordinates loaded")

        

    
    



#def open_file():
    #inFile = sys.argv[1]
    #outFile = sys.argv[2]    
    
    #print(inFile)
    
#data = np.genfromtxt('coordinate-001-H-prova.xyz', skip_header=3, dtype='str')
    #return data


    

        
        
        
