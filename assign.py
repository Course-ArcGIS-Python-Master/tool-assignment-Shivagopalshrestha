###The objective of the code is predict precipitation in firestations in RI
### 1. For this a csv of annual precipitation across newengland meterological stations and
### 2.location of firestations  in RI were used tp create a shapefile

### 3.An IDW map was created using the point shapefile
### 4.   Extractvalues to points  was used extract precipitation values to firestations in RI


# Only change the location to my local directory
import arcpy
import csv
import os
import glob
import matplotlib as plt
arcpy.env.overwriteOutput = True  # If you get "already exists error" even when True, ensure file is not open.


# 1. Convert Step_3_NE_Annual_P.csv to a shapefile.
input_directory = "C:\Users\User\Documents\Spring 19\ARCPY\Coding_Challenge_5"
arcpy.env.workspace = r"C:\Users\User\Documents\Spring 19\ARCPY\Coding_Challenge_5"

### Input files precipitation and Fireststation as csv
P = r"NE_Annual_P.csv"
Fire =  r"Fire_Stations.csv"


x_coords = "long"
y_coords = "lat"
out_Layer = "NE"
#saved_Layer = r"NE_Annual_P.shp"
saved_Layer1=str(P[:-4]) +".shp"
raster_out=str(P[:-4]) +".tif"
# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(P, x_coords, y_coords, out_Layer, spRef, "")

# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer1)
if arcpy.Exists(saved_Layer1):
    print " Shapefile Created   successfully!"

##########################################
#   raster using Inverse Distance Weighting (IDW).
# Requirements: Spatial Analyst Extension
from arcpy.sa import *

# Set local variables
inPointFeatures = saved_Layer1 #"NE_P_utm.shp"
zField = "Y2000"
cellSize = 0.022168
power = 2
searchRadius = RadiusVariable(25, 2.2)

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Execute IDW
outIDW = Idw(inPointFeatures, zField, cellSize, power, searchRadius)
# Save the output
#raster_out =r"NE0211.tif"
outIDW.save(raster_out)

if arcpy.Exists(raster_out):
    print " IDW  Created   successfully!"


#######

# 1. Convert Fire_Stations.csv to a shapefile.
#arcpy.env.workspace = r"C:\Users\User\Documents\Spring 19\ARCPY\Coding_Challenge_5"

#in_Table =Fire# r"Fire_Stations.csv"
#x_coords = "long"
#y_coords = "lat"
out_Layer = "Fire"
saved_Layer2 =str(P[:-4]) +"extracted.shp" # r"Fire_Stations1.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(Fire, x_coords, y_coords, out_Layer, spRef, "")

arcpy.CopyFeatures_management(lyr, saved_Layer2)
if arcpy.Exists(saved_Layer2):
    print "Created shapefile successfully!"

######
#### Extract raster values from IDW file to the point shapefiles.


# Set local variables
inPointFeatures = saved_Layer2#"saved_Layer"
inRaster = raster_out
outPointFeatures = "P_Extracted.shp"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute ExtractValuesToPoints
ExtractValuesToPoints(inPointFeatures, inRaster, outPointFeatures,
                      "INTERPOLATE", "VALUE_ONLY")

if arcpy.Exists(outPointFeatures):
    print "Extracted values successfully!"



###Delete unncessary stuffs
arcpy.Delete_management(raster_out)
arcpy.Delete_management(saved_Layer1)
arcpy.Delete_management(saved_Layer2)

