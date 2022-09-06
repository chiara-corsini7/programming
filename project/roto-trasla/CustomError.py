#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 09:50:25 2022

@author: chiaracorsini
"""

class SystemTooBig(ValueError):
    """ ValueError for too many atoms in the system """
    
class NumbersOfReplicas(ValueError):
    """ ValueError for number of replicas """

class CellAngle(ValueError):
    """ ValueError for cell angle """