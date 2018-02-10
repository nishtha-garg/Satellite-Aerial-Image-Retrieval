# Satellite-Aerial-Image-Retrieval
To automatically download aerial imagery (maximum resolution available) given a lat/lon bounding box. 

STEPS:
Convert the input latitude/longitude coordinates (in degrees) into pixel XY coordinates at a specified map size.
Convert pixel XY coordinates into tile XY coordinates of the tile containing the specified pixel.
Validate the tile values for both coordinates.
Proximity of points i.e. must not lie on the same tile.
Transform tiles into main diagonal form for convenience.
Determine the bounding tiles with highest level of detail.
Converts tiles XY into a QuadKey and then download the images corresponding to the QuadKey
Save the bounding image names using hash function and stitch these images based on it. 
Write the final image on to disk.

Setting Up Default Values:
To run the code, you need to change the basefolder’s name to the folder’s name you use.
The license does not have to be changed.

How To Run The Code?
The code could be run as follow:
Type the input coordinates into the main function at the end of AerialImageRetrieval.py file.

By default, we provide three examples of coordintates :
IIT Stuart building
Chicago Navy Pier
Statue of Liberty, NYC.
