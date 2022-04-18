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



parser = argparse.ArgumentParser(description='Translates and Rotates molecular coordinates.')
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
        
args = parser.parse_args()
    #return(args)


#def treat_input(args):
    # retrieviebìng 
modnt = np.array(args.translate)
modnr = np.array(args.rotate)
data = np.genfromtxt(args.file, skip_header=1, dtype='str')
    
    
el = data[:,0]
a = data[:,1].astype(float)
b = data[:,2].astype(float)
c = data[:,3].astype(float)


    
print('Selected file: %s' % args.file)
print('TRANSLATION %s in $\AA$' % modnt)
print('ROTATION %s' % modnr)
print('ELEMENTS %s' % el)
print ('COORD X %s' % a)
print ('COORD y %s' % b)
print ('COORD z %s' % c)
    
if (modnt==np.array([0.,0.,0.])).all() & (modnr==np.array([0.,0.,0.])).all():
    print('Not translating nor rotating the molecule')
elif (modnt==np.array([0.,0.,0.])).all():
    print('Only rotating the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    a = a_rot
    b = b_rot
    c = c_rot
elif (modnr==np.array([0.,0.,0.])).all():
    print('Only translating the molecule')
    a_tr, b_tr, c_tr = fc.trasla(a, b, c, modnt)
    a = a_tr
    b = b_tr
    c = c_tr
else:
    print('Roto-translating the molecule')
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr)
    a_tr, b_tr, c_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    a = a_tr
    b = b_tr
    c = c_tr


print ('new COORD X %s' % a)
print ('new COORD y %s' % b)
print ('new COORD z %s' % c)


    
plot.plot_molecule(a, b, c, el)
    

#print("Coordinates loaded")

        

    
    



#def open_file():
    #inFile = sys.argv[1]
    #outFile = sys.argv[2]    
    
    #print(inFile)
    
#data = np.genfromtxt('coordinate-001-H-prova.xyz', skip_header=3, dtype='str')
    #return data


    

        
        
        
