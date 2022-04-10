#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:12:35 2022

@author: chiaracorsini
"""

import numpy as np
import argparse


def get_input():
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
    data = np.genfromtxt('CO2.xyz', skip_header=1, dtype='str')
    
    
    el = data[:,0]
    a = data[:,1].astype(float)
    b = data[:,2].astype(float)
    c = data[:,3].astype(float)
    

    
    return(modnt, modnr, el, a, b, c)
    
    
    #parser.print_help()
    print(args.translate)
    #print(args.accumulate(args.integers))
    
    
    
def main():
    #args = get_input()
    modnt, modnr, el, a, b, c = get_input()
    #modnt, modnr, el, a, b, c = treat_input(args)
    print('TRANSLATION %s' % modnt)
    print('ROTATION %s' % modnr)
    print('ELEMENTS %s' % el)
    print ('COORD X %s' % a)
    print ('COORD X %s' % b)
    print ('COORD X %s' % c)
    

if __name__ == '__main__':
    main()
    

#print("Coordinates loaded")

        

    
    



#def open_file():
    #inFile = sys.argv[1]
    #outFile = sys.argv[2]    
    
    #print(inFile)
    
#data = np.genfromtxt('coordinate-001-H-prova.xyz', skip_header=3, dtype='str')
    #return data


    

        
        
        
