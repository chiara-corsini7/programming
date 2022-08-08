#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Wed Mar  9 16:50:00 2022@author: chiaracorsini"""import numpy as npimport CustomError as CEdef trasla (a, b, c, modnt):    """This function translates the initial coordinates of the wanted amount.            Parameters:        a, b, c : x, y, z initial coordinates        modnt : 3x1 float array containing x, y and z displacements            Returns:        translated coordinates        """            print("Translating ...")            a_new = a + modnt[0]    b_new = b + modnt[1]    c_new = c + modnt[2]        return a_new, b_new, c_new    def r_matrix (modnr):     """This function creates the x, y, z rotation matrices from rotation angles            Parameters:        modnr : 3x1 float array containing x, y and z rotation angles in radians            Returns:        x, y and z rotation matrices: R1, R2, R3        """        # Initializing the matrices        R1 = np.zeros((3,3))    R2 = np.zeros((3,3))    R3 = np.zeros((3,3))    # R1 = Rx --> x rotation matrix    R1[0,:] = [1,0,0]    R1[1,:] = [0,np.cos(modnr[0]),-np.sin(modnr[0])]    R1[2,:] = [0,np.sin(modnr[0]),np.cos(modnr[0])]        # R2 = Ry --> y rotation matrix    R2[0,:] = [np.cos(modnr[1]),0,np.sin(modnr[1])]    R2[1,:] = [0,1,0]    R2[2,:] = [-np.sin(modnr[1]),0,np.cos(modnr[1])]    # R2 = Ry --> y rotation matrix    R3[0,:] = [np.cos(modnr[2]),-np.sin(modnr[2]),0]    R3[1,:] = [np.sin(modnr[2]),np.cos(modnr[2]),0]    R3[2,:] = [0,0,1]        return R1, R2, R3def ruota (a, b, c, modnr, var):    """This function rotates the initial coordinates of the wanted amount       and relocates the coordinate for a free molecule            Parameters:        a, b, c : x, y ,z initial coordinates        modnr : 3x1 float array containing x, y and z rotation angles        var : bool for free molecule            Returns:        rotated coordinates        """            print("Rotating ...")        # initializing new coordinates        M = len(a)        a_new = np.zeros(M)    b_new = np.zeros(M)    c_new = np.zeros(M)    # getting mean x, y, z coordinates of the molecule to reposition it in case it is a free molecule    a0=np.mean(a)    b0=np.mean(b)    c0=np.mean(c)         # getting rotation matrices     R1, R2, R3 = r_matrix(modnr)        # creating the RxRyRz rotation matrix        Rxy = np.dot(R1, R2)    Rxyz = np.dot(Rxy, R3)    for j in range(len(a)):                # creating position vector for each atom                x = [a[j],b[j],c[j]]                # performing rotation                x_rot= np.dot(Rxyz, x)                # assigning rotated coordinates to new vectors                a_new[j] = x_rot[0]        b_new[j] = x_rot[1]        c_new[j] = x_rot[2]            # repositioning the free molecule        if var == True :            a1=np.mean(a_new)        b1=np.mean(b_new)        c1=np.mean(c_new)        a_new = a_new - (a1-a0)        b_new = b_new - (b1-b0)        c_new = c_new - (c1-c0)                      return a_new, b_new, c_newdef cell(cell_vec, cell_ang):    """This function creates the matrix vectors to describe the unit cell             Parameters:        cell_vec : 3x1 float array containing x, y and z unit cell vectors        cell_ang : 3x1 nfloat array containing x, y and z unit cell angles [0,180)deg            Returns:        3 3x1 matrix vectors to describe the unit cell        """       # Raising Errors for cell angles that are greater than 180° or smaller than 0°        if cell_ang[0] > np.pi or cell_ang[1] > np.pi or cell_ang[2] > np.pi:        raise CE.CellAngle("Cell angles greater than 180° don't have physical sense")    if cell_ang[0] < 0. or cell_ang[1] < 0. or cell_ang[2] < 0.:        raise CE.CellAngle("Cell angles smaller than 0° don't have physical sense")        # assigning variables to build the matrix        a1 = cell_vec[0]    a2 = cell_vec[1]    a3 = cell_vec[2]            th1 = cell_ang[0]    th2 = cell_ang[1]    th3 = cell_ang[2]          # making the matrix        # For an orthorombic cell        if th1 == np.pi/2 and th2 == np.pi/2 and th3 == np.pi/2:        print('Orthorombic cell')        cell_vecs_x = np.array([a1, 0., 0.], dtype=float)        cell_vecs_y = np.array([0., a2, 0.], dtype=float)        cell_vecs_z = np.array([0., 0., a3], dtype=float)            # For a non-orthorombic cell        else:        print('Non orthorombic cell')        cell_vecs_x = np.array([a1,0.,0.], dtype=float)        cell_vecs_y = np.array([a2*np.cos(th3),a2*np.sin(th3),0.], dtype=float)            cz2 = a3*(np.cos(th1)-np.cos(th2)*np.cos(th3))/np.sin(th3)        cz3 = a3*(1.+(2.*np.cos(th1)*np.cos(th2)*np.cos(th3))-((np.cos(th1))**2-(np.cos(th2))**2-(np.cos(th3))**2))**(1/2)        cz3 = cz3/np.sin(th3)        cell_vecs_z = np.array([a3*np.cos(th2),cz2,cz3], dtype=float)        return(cell_vecs_x, cell_vecs_y, cell_vecs_z)def replica (el, a, b, c, modnre, cell_vec, cell_ang):    """This function replicates the initial coordinates respect to the given unit cell             Parameters:        el: element list        a, b, c : x, y ,z initial coordinates        modnre : 3x1 array of integers containing x, y and z repetition         cell_vec, cell_ang: unit cell vectors and angles                    Returns:        replicated coordinates        """             # Raising error in case number of replicas requested is < 0        if modnre[0] < 1 or modnre[1] < 1 or modnre[2] < 1:        raise CE.NumbersOfReplicas("Numbers of replicas values must be integers greater than one")    # getting cell matrix vectors        cell_vecs_x, cell_vecs_y, cell_vecs_z = cell(cell_vec, cell_ang)        # calculating total number of atoms        nat_iniz = len(el)    M = nat_iniz*modnre[0]*modnre[1]*modnre[2]        # Raising exception if replicated number of atoms is too big        if M > 100000:        raise CE.SystemException("Too many atoms in the final system")         print("Cloning ...")        # initializing new vectors for replicated atoms            a_new = np.zeros(nat_iniz)    b_new = np.zeros(nat_iniz)    c_new = np.zeros(nat_iniz)    el_new = np.zeros(nat_iniz)    # replicating one atom at the time in each direction    for nat in range(len(el)):        for i in range(modnre[0]):            for j in range(modnre[1]):                for k in range(modnre[2]):                                     add_x = i*cell_vecs_x[0] + j*cell_vecs_y[0] + k*cell_vecs_z[0]                    add_y = i*cell_vecs_x[1] + j*cell_vecs_y[1] + k*cell_vecs_z[1]                    add_z = i*cell_vecs_x[2] + j*cell_vecs_y[2] + k*cell_vecs_z[2]                                    # assigning replicated atoms to new  vectors                                    a_new = np.append(a_new, a[nat]+add_x)                    b_new = np.append(b_new, b[nat]+add_y)                    c_new = np.append(c_new, c[nat]+add_z)                    el_new = np.append(el_new, el[nat])                        # Removing original atoms coordinates that were reintroduced         a_new = np.delete(a_new, slice( 0, nat_iniz))    b_new = np.delete(b_new, slice( 0, nat_iniz))    c_new = np.delete(c_new, slice( 0, nat_iniz))    el_new = np.delete(el_new, slice( 0, nat_iniz))                        return(el_new, a_new, b_new, c_new)        