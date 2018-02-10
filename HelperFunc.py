# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:52:44 2017
HelperFunc.py
@authors: Nishtha
"""

import math

EarthRadius = 6378137
MinLatitude = -85.05112878
MaxLatitude = 85.05112878
MinLongitude = -180
MaxLongitude = 180
screenDpi = 1024

# Clips a number to the specified minimum and maximum values.
# Returns the clipped value.
def clip(n, minValue, maxValue):
    return min(max(n, minValue), maxValue)

# Determines the map width and height (in pixels) at a specified level of detail.
# Returns the map width and height in pixels.
def mapSize(levelOfDetail):
    return 256 << levelOfDetail

# Determine the ground resolution (in meters per pixel) at a specified latitude and 
# level of detail.
# Returns the ground resolution, in meters per pixel.
def groundResolution(lat, levelOfDetail):
    latitude = clip(lat, MinLatitude, MaxLatitude)
    return math.Cos(latitude * math.PI / 180) * 2 * math.PI * EarthRadius / mapSize(levelOfDetail);

# Determines the map scale at a specified latitude, level of detail, and screen resolution.
# Returns the map scale, expressed as the denominator N of the ratio 1 : N.
def mapScale(latitude, levelOfDetail, screenDpi):
    return groundResolution(latitude, levelOfDetail) * screenDpi / 0.0254

# Converts a point from latitude/longitude WGS-84 coordinates (in degrees) 
# into pixel XY coordinates at a specified level of detail.
def latLongToPixelXY(latitude, longitude, levelOfDetail):
    latitude = clip(latitude, MinLatitude, MaxLatitude)
    longitude = clip(longitude, MinLongitude, MaxLongitude)
        
    x = (longitude + 180) / 360
    sinLatitude = math.sin(latitude * math.pi / 180)
    y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)
        
    mapsize = mapSize(levelOfDetail)
    pixelX = clip(x * mapsize + 0.5, 0, mapsize - 1)
    pixelY = clip(y * mapsize + 0.5, 0, mapsize - 1)
    
    return pixelX, pixelY

# Converts a pixel from pixel XY coordinates at a specified level of detail
# into latitude/longitude WGS-84 coordinates (in degrees).
def pixelXYToLatLong(pixelX, pixelY, levelOfDetail):
    
    mapsize = mapSize(levelOfDetail)
    x = (clip(pixelX, 0, mapsize -1) / mapsize) - 0.5
    y = 0.5 - (clip(pixelY, 0, mapsize - 1) / mapsize)

    latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
    longitude = 360 * x

    return latitude, longitude
    
# Converts pixel XY coordinates into tile XY coordinates of the tile containing the 
# specified pixel.
def pixelXYToTileXY(pixelX, pixelY):
    tileX = int(pixelX / 256)
    tileY = int(pixelY / 256) 
    
    return tileX, tileY

# Converts pixel XY coordinates into tile XY coordinates of the tile containing the 
# specified pixel.
def tileXYToPixelXY(tileX, tileY):
    pixelX = tileX * 256
    pixelY = tileY * 256
    
    return pixelX, pixelY

# Converts tile XY coordinates into a QuadKey at a specified level of detail.
# Returns a string containing the QuadKey.
def tileXYToQuadKey(tileX, tileY, levelOfDetail):
    quad = ""
    for i in range(levelOfDetail, 0, -1):
        digit='0'
        mask = (1 << (i - 1))

        if (tileX & mask) != 0:
            digit = chr(ord(digit) + 1)
            
        if (tileY & mask) != 0:
            digit = chr(ord(digit) + 1)
            digit = chr(ord(digit) + 1)
        quad += digit
    return quad

####################################################
##              Cumulative functions              ##
####################################################


# Given lat/long this function will generate a quad key    
def latLongToQuad(latitude, longitude, levelOfDetail):
    print ("\n")
    print ("LevelofDetail : %s" % (levelOfDetail))
    print ("Latitude, Longitude: %s, %s " % (latitude, longitude))    
    
    # Convert lat, long to Quad Key
    pixelX, pixelY = latLongToPixelXY(latitude, longitude, levelOfDetail)
    print ("Pixels: %s, %s " % (pixelX, pixelY))
    
    tileX, tileY = pixelXYToTileXY(pixelX, pixelY)
    print ("Tiles: %s, %s " % (tileX, tileY))
    
    quadKey = tileXYToQuadKey(tileX, tileY, levelOfDetail)
    print ("Generated Quad: %s " % (quadKey))    
    
    return str(quadKey)

# Given lat/long this function will generate a tiles    
def latLongToTiles(latitude, longitude, levelOfDetail):
    print ("\n")
    print ("LevelofDetail : %s" % (levelOfDetail))
    print ("Latitude, Longitude: %s, %s " % (latitude, longitude))    
    
    # Convert lat, long to Quad Key
    pixelX, pixelY = latLongToPixelXY(latitude, longitude, levelOfDetail)
    print ("Pixels: %s, %s " % (pixelX, pixelY))
    
    tileX, tileY = pixelXYToTileXY(pixelX, pixelY)
    print ("Tiles: %s, %s " % (tileX, tileY))   
    
    return tileX, tileY


