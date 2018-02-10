# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:52:44 2017
AerialImageRetrieval.py
@author: Nishtha
"""

import urllib
import os
import sys
import shutil
import matplotlib.pyplot as plt
import numpy as np
import HelperFunc
import ImageStitchFunc

# Global parameters
license_key = 'As3IiCiRRCJf9nbxYnjMQQ6kW6Dkd1keZept6i96kkKNGyw-5NKJD3MugdjKJoDC'
basefolder = '/Users/nish/Downloads/roy/'
folder = basefolder + 'temp/'

# Create temp folder for storing images
shutil.rmtree(folder, ignore_errors=True)
os.mkdir(folder, 0777)
print("Temp folder created")

# Download desired image from web server
def downloadImage(quadKey, name): 
    img = os.path.join(folder, name)
    url = 'http://h0.ortho.tiles.virtualearth.net/tiles/h' + quadKey + '.jpeg?g=131&key=' + license_key
    try:
        page = urllib.urlretrieve(url, img)
    except Exception, e:
        return 0, e
    #urllib.urlretrieve(url, img) 
    print("Image Download Complete...")
    return 1, 'success'
    
def displayImage(name):
    print("Displaying Image...")
    img = os.path.join(folder, name)
    ob = plt.imread(img)    
    plt.imshow(ob)
    plt.show()

def loadNullImage():
    img = os.path.join(basefolder, 'null.jpg')
    nullObj = plt.imread(img)
    return nullObj    


####################################################
##              Cumulative functions              ##
####################################################
   
# This function will get neighbouring tiles,
# download them in a folder, renaming using hash function,
# and display them
def getBoundingTileImages(tx1, ty1, tx2, ty2, LoD):
    tup = []
    for y in xrange(ty1, ty2+1):
        col = [] 
        for x in xrange(tx1, tx2+1):
                    print ("\nBounding tiles: %s, %s " % (x, y))
                    quadKey = HelperFunc.tileXYToQuadKey(x, y, LoD)
                    # Hash the file name for convenience in stitching
                    name = str(x % tx1) + str(y % ty1) + '.jpg' ; print(name)
                    val, msg = downloadImage(quadKey, name)
                    
                    if val == 0:
                        print('Could not download image...')
                        print(msg)
                        return tup, 1
                    
                    # Check if the image has been downloaded properly
                    if np.all((plt.imread(os.path.join(folder, name))) == loadNullImage()) == True:    
                        print("Could not download Image...")
                        print("Either a connection problem or image doesn't exist at level...")
                        return tup, 1
                    #displayImage(name)
                    col.append(str(x % tx1) + str(y % ty1))
        tup.append(col)
    print(tup)
    return tup, 0

#getBoundingTileImages(67262, 97469, 67264, 97470, 18)

# Transform to new tile coordinates
# Performs coordinate validation and picks diagonal tiles for convenience
def validateCoordinates(lat1, lon1, lat2, lon2, maxLoD):
    for i in xrange(maxLoD, 0, -1):        
        tx1, ty1 = HelperFunc.latLongToTiles(lat1, lon1, i)
        tx2, ty2 = HelperFunc.latLongToTiles(lat2, lon2, i)
        
        if ty1 > ty2:
            ty1, ty2 = ty2, ty1            
            
        if tx1 > tx2:
            tx1, tx2 = tx2, tx1 
            
        if (tx2 - tx1 >= 1) and (ty2 - ty1 >= 1):
            print ("Best detail found at Level: %s" % (i))
            print ("Transformed Tiles: %s, %s, %s, %s " % (tx1, ty1, tx2, ty2)) 
            return tx1, ty1, tx2, ty2, i

    print ("Error: The coordinates are on same tile...")
    print ("Program will abort without downloading anything...\n")
    sys.exit()

	
def main(lat1, lon1, lat2, lon2):
    maxLoD = 23
    found = 1

    while (found == 1):
        tx1, ty1, tx2, ty2, LoD = validateCoordinates(lat1, lon1, lat2, lon2, maxLoD)
        tup, found = getBoundingTileImages(tx1, ty1, tx2, ty2, LoD)
        maxLoD = maxLoD -1
        if maxLoD < 0:
            break    

    # Stitch from directory
    fs = ImageStitchFunc.startStitch(tup, folder)
    print("Stiching complete. Displaying image...")

    plt.imshow(fs)
    plt.show()


#main(41.838928, -87.628503, 41.838244, -87.626847) # IIT Stuart Building Coordinates
main(41.892026, -87.608168, 41.891387, -87.606156) # Chicago Navy Pier
#main(40.690135, -74.046679 , 40.688524, -74.042366) # Statue of Liberty, NY
