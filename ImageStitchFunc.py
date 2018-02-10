# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:52:44 2017
ImageStitchFunc.py
@authors: Nishtha
"""
import matplotlib.pyplot as plt
import numpy as np
import os

baseDim = 256

def startStitch(tup, folder):
    # Create empty numpy array based on number and tile arrangements
    h, w = np.shape(tup)
    fs = np.zeros((h * baseDim, w * baseDim, 3), np.uint8)
    
    # Below will stitch images based on coordinates and display it
    for i in range(len(tup)):
        hs = np.zeros((1 * baseDim, w * baseDim, 3), np.uint8)
        for j in tup[i]:
            img = plt.imread(folder + j + '.jpg')
            hs = np.hstack((hs, img))
            
        hs = hs[:, w * baseDim:, :3]
        fs = np.vstack((fs, hs)) 
    fs = fs[h * baseDim : ,: , :3]
    baseFolder = os.path.split(os.path.abspath(folder))[0]
    plt.imsave(baseFolder + '/final.jpg', fs)
    return fs    