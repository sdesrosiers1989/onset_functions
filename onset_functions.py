#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 08:40:51 2018

@author: earsch

Function to do common things with onset data
-find seasons
-combine unimodal and short/long rains
-find and combine
"""

import numpy as np
import numpy.ma as ma

#Locate specific season with cubelist
def find_season(data, name):  
    for cube in data:
        if cube.long_name == name:
            out = cube
    return out

#Apply land sea mask to data
def masking(input_cube, mask, small_mask = False):
    dimensions = input_cube.shape
    out = input_cube.copy()
    
    if small_mask == True:
        if len(dimensions) == 3:
            for i in np.arange(dimensions[1]):
                for j in np.arange(dimensions[2]):
                    if mask.data[i,j]<0.5:
                        out.data[:,i,j] = float('nan')
        if len(dimensions) == 2:
            for i in np.arange(dimensions[0]):
                for j in np.arange(dimensions[1]):
                    if mask.data[i,j]<0.5:
                        out.data[i,j] = float('nan')
                    
    elif small_mask == False:
        if len(dimensions) == 3:
            for i in np.arange(dimensions[1]):
                for j in np.arange(dimensions[2]):
                    if mask.data[0,0,i,j]<0.5:
                        out.data[:,i,j] = float('nan')
        
        if len(dimensions) == 2:
            for i in np.arange(dimensions[0]):
                for j in np.arange(dimensions[1]):
                    if mask.data[0,0,i,j]<0.5:
                        out.data[i,j] = float('nan')
    
    return out

def combine_seasons(unimodal, short, long):
    mask = ma.getmask(unimodal.data)
    us_onset = unimodal.copy() # create copy unimodal onset
    us_onset.data[mask] = short.data[mask] #where unimodal onset is na
    # add data from short rain onset
    ulong_onset = unimodal.copy()
    ulong_onset.data[mask] = long.data[mask]
    return us_onset, ulong_onset

def combine_find_seasons(data, type = 'Onset'):
    if type == 'Onset':
        unimodal = find_season(data, 'Onset Date for Unimodal Regions')
        short = find_season(data, 'Onset Date for Short Rains')
        long = find_season(data, 'Onset Date for Long Rains')
    
        us_onset, ulong_onset = combine_seasons(unimodal, short, long)
    if type == 'Cessation':
        unimodal = find_season(data, 'Cessation Date for Unimodal Regions')
        short = find_season(data, 'Cessation Date for Short Rains')
        long = find_season(data, 'Cessation Date for Long Rains')
    
        us_onset, ulong_onset = combine_seasons(unimodal, short, long)
    if type == 'Duration':
        unimodal = find_season(data, 'Season Length for Unimodal Regions')
        short = find_season(data, 'Season Length for Short Rains')
        long = find_season(data, 'Season Length for Long Rains')
    
        us_onset, ulong_onset = combine_seasons(unimodal, short, long)
    return us_onset, ulong_onset