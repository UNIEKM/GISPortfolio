# Assignment 2: Script 1
#Created Feb 14, 2023, by Kevin Van Dijk 
#Tested using Python 3.9.11 64-bit

# This script converts GPS .txt files.
# Creates GDB, Feature Dataset with spatial reference, reads/writes .txt files to usable format (comma separtated values).
# Creates Feature Class inside Feature Dataset
# Inserts points using GPS Coordinates

# This script assumes there are no GDB/feature datasets/feature class present.
# Script assumes current .txt file format is separated by spaces, replaces with ",", and the first line in .txt files is a string ("Field Labels").
# "arcpy.env.overwriteOutput = True" can be used when testing script, allowing for overwrite of existing files. 
# Current projection NAD UTM ZONE 12N| Can be modified using ESRI Documentation on Spatial Reference if needed.

# import site packages and modules
import arcpy
import os

# Turn on "arcpy.env.overwriteOutput = True" when testing a script.
# arcpy.env.overwriteOutput = True # COMMENT OUT ONCE SCRIPT COMPLETED


# Input folder as workspace
# User needs to update input_folder to file path 
input_folder = r'C:\PythonPro\Assignment2DataPackage\Assignment2DataPackage\SpatialRealtors'
print("")
arcpy.env.workspace = input_folder
print(f"Current input folder path: {input_folder}")
print("")

# Create new file GDB
out_folder_path = input_folder
out_name = "Realtor_Tracks.gdb"
arcpy.env.overwriteOutput = True 
arcpy.CreateFileGDB_management(out_folder_path,out_name)
print(f"New file GDB Created: {out_name}")

# Create Feature Dataset with required Spatial Reference
out_dataset_path = os.path.join(out_folder_path, out_name)
out_name = "Realtors"

sr = arcpy.SpatialReference(26912)
arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, sr)
print(f"Feature Dataset Created: {out_name}")
print("")

# Loop through the .text files, setting fc name from txt_files
# Create new fc with names from .txt files
# path.splitext(.txt), splits example.txt -> tuple ["example":".txt"],[0]=file name|[1]=file extension 
# Create Feature Class  
for file in arcpy.ListFiles("*.txt"):
    fc_name = os.path.splitext(file)[0] 
    fc_path = os.path.join(out_dataset_path, fc_name)
    # arcpy.env.overwriteOutput = True #REMOVE ONCE SCRIPT COMPLETED
    sr = arcpy.SpatialReference(26912)
    arcpy.CreateFeatureclass_management(out_dataset_path, fc_name, "POINT", "", "", "", sr)
    print(f"New Feature Class Created: {fc_path}")
    # Read .txt files, reformat and write into comma separated values, overwriting .txt files
    with open(os.path.join(input_folder, file), 'r') as input_file:
        lines = input_file.readlines()
        input_file.close()
    with open(os.path.join(input_folder, file), 'w') as output_file:
        for line in lines[1:]:
            values = line.split()
            output_file.write(','.join(values) + '\n')
        output_file.close()
    # Open and read ('r') .txt files containing coordinates downloaded from GPS
    # Insert points into the new feature classes 
    with open(os.path.join(input_folder, file), 'r') as f:
        for line in f:
            parts = line.split(',')
            str_part = parts[0]
            float_part1 = float(parts[1])
            float_part2 = float(parts[2])
            # Get the X and Y coordinates from each line in the text file
            x, y = map(float, parts[1:])
            pnt = arcpy.Point(x, y)

            cursor = arcpy.da.InsertCursor(fc_path, ["SHAPE@"])
            cursor.insertRow([pnt])
            del cursor

    print(f"GPS Coordinates Added to Feature Class: {fc_path}")