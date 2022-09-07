#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:12:35 2022

@author: chiaracorsini
"""

import functions as fc
import plot as plot
import data as dt
import numpy as np
import argparse
import os

########################################################################
              ############## GETTING INPUT #############
#########################################################################              
              
# getting input from bash through ArgumentParser class of argparse

parser = argparse.ArgumentParser(description='Translate Rotate and Clone molecular coordinates.')

# getting input file POSITIONAL ARGUMENT == MANDATORY ARGUMENT

parser.add_argument('file', action='store', 
                    help=".xyz file with coordinates",  type=str)

# getting translations 

parser.add_argument('-t','--translate', action='store', nargs=3, 
                    help=r"x y and z coordinates of translation vector,"\
                    " default 0. 0. 0.", default = [0.,0.,0.], type=float,
                    metavar=('dx', 'dy', 'dz'))

# getting rotations in degrees    
    
parser.add_argument('-r','--rotate', action='store', nargs=3, 
                    help="x y and z rotations in degrees,"\
                    "default 0. 0. 0.", default =[0.,0.,0.], type=float,
                    metavar=('rotx', 'roty', 'rotz'))
    
# getting numbers of replicas 
    
parser.add_argument('-c','--clone', action='store', nargs=3, 
                    help="Number of replicas in x y and z,"\
                    "default 1 1 1", default =[1,1,1], type=int,
                    metavar=('repx', 'repy', 'repz'))
    
# getting if it is a free molecule or bulk
    
parser.add_argument('-m','--molecule', action='store',
                    help="Input file a free molecule (True) or bulk (False)"\
                    "default, var==True", default=True, type=bool,
                    metavar='var') 
    
# getting unit cell vectors    
    
parser.add_argument('-v','--vectors', action='store', nargs=3, 
                    help="a b and c unit cell vectors,"\
                    "unit cell vectors of 15 units side greater than molecule are default", default =[0.,0.,0.], type=float,
                    metavar=('a', 'b', 'c'))
    
# getting unit cell angles
    
parser.add_argument('-a','--angles', action='store', nargs=3, 
                    help="α β and γ unit cell angles in degrees,"\
                    "orthorombic cell is default (90. 90. 90.)", default =[90.,90.,90.], type=float,
                    metavar=('α', 'β', 'γ'))
    
    
    
parser.add_argument('-i', '--image', action='store_true', 
    help="saves image of the system")
        
args = parser.parse_args()


########################################################################
              ############## ASSIGNING VARIABLES #############
######################################################################### 


# assigning arguments to variables 

modnt = np.array(args.translate)
modnr = np.array(args.rotate)
modnre = np.array(args.clone)
cell_vec = np.array(args.vectors)
cell_ang = np.array(args.angles)
var = args.molecule
path, old_file = os.path.split(args.file)

if path == '':
    path = path
else:
    path = path+'/'

data = np.genfromtxt(args.file, skip_header=2, dtype='str')


#getting data

el, a, b, c = dt.get_data(data)

# building defaukt cell if not provided

if (cell_vec==np.array([0.,0.,0.])).all():
    cell_vec = dt.build_cell(cell_vec, a, b, c)
    
    
# changing angles to radians  
   
cell_ang = dt.angle_rad(cell_ang)



########################################################################
              ############## PRINTING INPUT #############
######################################################################### 

# Printing input info
 
print('\n') 
print('Selected file: %s' % args.file)
print('TRANSLATION %s' % modnt)
print('ROTATION %s' % modnr)
print('REPLICAS %s' % modnre)
print('ELEMENTS %s' % el)
print ('COORD X %s' % a)
print ('COORD y %s' % b)
print ('COORD z %s' % c)
print ('Cell vectors %s' %cell_vec)
print ('Cell angles %s' %cell_ang)
print('\n')


# initializing new file name
new_file = old_file
file_add = ''


########################################################################
        ############## PERFORMING TRANSFORMATIONS #############
######################################################################### 

translate = True
rotate = True
clone = True

if (modnt==np.array([0.,0.,0.])).all(): 
    translate = False
if (modnr==np.array([0.,0.,0.])).all(): 
    rotate = False
if (modnre==np.array([1, 1, 1])).all(): 
    clone = False



# deciding what operations to perform

# No operations
   
if translate == False and rotate == False and clone == False:
    print('Not translating nor rotating nor cloning the molecule')

# Rotation
    
elif translate == False and clone == False:
    print('Only rotating the molecule')
    file_add='R-'
    
    # degrees to radians
    
    modnr=dt.angle_rad(modnr)
    
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr, var)
    a = a_rot
    b = b_rot
    c = c_rot
    
# Translation
    
elif rotate ==  False and clone == False:
    print('Only translating the molecule')
    file_add='T-'
    
    
    a_tr, b_tr, c_tr = fc.trasla(a, b, c, modnt)
    a = a_tr
    b = b_tr
    c = c_tr
    
# Clonation
        
elif translate == False and rotate == False:
    print('Only cloning the molecule')
    file_add='C-'
    
    
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a, b, c, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep
    
# Rotation + Translation
        
elif clone == False:
    print('Roto-translating the molecule')
    file_add='R+T-'
    
    # degrees to radians
    
    modnr=dt.angle_rad(modnr)
    
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr, var)
    a_tr, b_tr, c_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    a = a_tr
    b = b_tr
    c = c_tr
    
# Translation + Clonation
        
elif rotate == False:
    print('Translating and cloning the molecule')
    file_add='T+C-'
    
    
    a_tr, b_tr, c_tr = fc.trasla(a, b, c, modnt)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_tr, b_tr, c_tr, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep
    
# Rotation + Clonation
        
elif translate == False:
    print('Rotating and cloning the molecule')
    file_add='R+C-'
    
    # degrees to radians
    
    modnr=dt.angle_rad(modnr)
    
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr, var)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_rot, b_rot, c_rot, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep

# Rotation + Translation + Clonation
        
else:
    print('Roto-translating and cloning the molecule')
    file_add='R+T+C-'
    
    # degrees to radians
    
    modnr=dt.angle_rad(modnr)
    
    a_rot, b_rot, c_rot = fc.ruota(a, b, c, modnr, var)
    a_tr, b_tr, c_tr = fc.trasla(a_rot, b_rot, c_rot, modnt)
    el_rep, a_rep, b_rep, c_rep = fc.replica(el, a_tr, b_tr, c_tr, modnre, cell_vec, cell_ang)
    el = el_rep
    a = a_rep
    b = b_rep
    c = c_rep




########################################################################
              ############## PRINTING OUTPUT #############
######################################################################### 


# Printing output info

print('\n')
print ('new elements %s' % el)
print ('new COORD X %s' % a)
print ('new COORD y %s' % b)
print ('new COORD z %s' % c)
print('\n')


# Printing output file



if file_add+new_file != old_file:

    print('########################################')
    print('########## NEW .xyz FILE ###############')
    print('########################################')

    print('\n')
    print(len(el),'\n')


    for i in range(len(el)):
        print(el[i] , round(a[i],6) ,round(b[i],6) ,round(c[i], 6))
    
    print('\n')     
      
else:
    print('No changes --> nothing printed')


# Plotting output

if args.image:
    file_name = path+file_add+new_file 
    file_name = file_name.replace('.xyz', '.png')
    cell_vecs_x, cell_vecs_y, cell_vecs_z = fc.cell(cell_vec, cell_ang)    
    plot.plot_molecule(a, b, c, el, cell_vecs_x, cell_vecs_y, cell_vecs_z, file_name)
    print('Image saved in', file_name)





#print("Coordinates loaded")

        

    
    



#def open_file():
    #inFile = sys.argv[1]
    #outFile = sys.argv[2]    
    
    #print(inFile)
    
#data = np.genfromtxt('coordinate-001-H-prova.xyz', skip_header=3, dtype='str')
    #return data


    

        
        
        
