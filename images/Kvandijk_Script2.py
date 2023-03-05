##Assignment 1: Script 2
##GEOM73
##Created January 25, by Kevin Van Dijk
##Tested using Python 3.9.11 64-bit
import arcpy
import os

ws = "C:\PythonPro\A1DataPackage\ItalyPictures"
out_name = "ItalyPictures.gdb"
out_fcpoint = "ItalyPictures.gdb\ImagePoint"
arcpy.env.workspace = ws
arcpy.management.CreateFileGDB(ws, out_name)
arcpy.management.GeoTaggedPhotosToPoints(ws, out_fcpoint, "", "ONLY_GEOTAGGED", "ADD_ATTACHMENTS")
print("GeoTagged Photos To Points completed")