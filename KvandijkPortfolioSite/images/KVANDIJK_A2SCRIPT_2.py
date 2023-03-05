# Assignment 2: Script 2
#Created Feb 15, 2023, by Kevin Van Dijk 
#Tested using Python 3.9.11 64-bit

# This script reduces redundancy by creating subtypes, taking individual shapefiles and inserting them into the subtypes of a new single shapefile.
# This eliminates the need for individual shapefiles when each shapefile contains the same datastructure for each location. 
# Create new file GDB with same name as input folder
# Create Feature Class w/ name=input_folder
# Create Add field called TYPECODE to New FC, type= short, set to subtype field of FC.
# Finds all shapefiles in folder.
# Subtype name corresponds to the shapefile name.
# Data is loaded into correct subtypes base on which shapefile in the input_folder they originate from.


# This script assumes there are no GDB/feature datasets/feature class present.
# Script assumes each FC is a Point.
# "arcpy.env.overwriteOutput = True" can be used when testing script, allowing for overwrite of existing files. 
# Script assumes the user can update input_folder file path, and .prj file path to reference appropriate spatial reference.


# import site packages and modules
import arcpy
import os

# Turn on "arcpy.env.overwriteOutput = True" when testing a script.
# arcpy.env.overwriteOutput = True # COMMENT OUT ONCE SCRIPT COMPLETED

# Input folder as workspace
# User needs to update input_folder to file path 
input_folder = r'C:\PythonPro\Assignment2DataPackage\Assignment2DataPackage\ReducingRedundancy\MajorClients'
print("")
arcpy.env.workspace = input_folder
print(f"Current input folder path: {input_folder}")
print("")

# Create new file GDB with same name as input folder
out_folder_path = input_folder
out_name = os.path.basename(input_folder) + ".gdb"
# Turn on "arcpy.env.overwriteOutput = True" when testing a script.
arcpy.env.overwriteOutput = True # COMMENT OUT ONCE SCRIPT COMPLETED
arcpy.CreateFileGDB_management(out_folder_path, out_name)
out_gdb = os.path.join(out_folder_path, out_name)

print(f"New file GDB created: {out_gdb}")

# Create Feature Class w/ name=input_folder|Assume Each FC is a Point.
# Spatial reference taken from existing shapefiles in folder.
# Update prjfile path to reference .prj file in gdb that has the spatial reference you need.
prjfile = r'C:\PythonPro\Assignment2DataPackage\Assignment2DataPackage\ReducingRedundancy\MajorClients\MajorClientsOntario.prj'
sr = arcpy.SpatialReference(prjfile)

out_folder_path = out_gdb
fc_name = os.path.basename(input_folder)
fc_path = os.path.join(out_gdb, fc_name)
# Turn on "arcpy.env.overwriteOutput = True" when testing a script.
arcpy.env.overwriteOutput = True #REMOVE ONCE SCRIPT COMPLETED
arcpy.CreateFeatureclass_management(out_folder_path, fc_name, "POINT", "", "", "", sr)
print(f"New Feature Class Created: {fc_path}")
print("")
# Add field called TYPECODE to New FC, type= short, set to subtype field of FC.

arcpy.management.AddField(fc_path, "TYPECODE", "SHORT")

# Set New Field TYPECODE as subtype field
# subtype_code is a unique integer value to the subtype to be added.
# Add subtype
subtype_code = 0
subtype_descr = "TypeCode"
subtype_field = "TYPECODE"
# Turn on "arcpy.env.overwriteOutput = True" when testing a script.
arcpy.env.overwriteOutput = True # COMMENT OUT ONCE SCRIPT COMPLETED
arcpy.SetSubtypeField_management(fc_path, subtype_field)


# Establish a counter variable, and then for each shapefile in the folder:
# Use ListFields to find all shapefiles in folder.
# Set subtype_code to current value of counter.
# Subtype name corresponds to the shapefile name, scrubbing folder name and extension.
# Using os module to extraxt the filename from the fill path of shapefiles in folder.
# splitext splits filename into tuple containing filename and extension. [0] gets filename without extension.
# replace(fc_name, "") called on filename to remove the feature class name from it. 
# Where fc_name contains the name of the feature class that subtypes are being added to, replacing that name with an empty string "".
# returning just the portion of the filename that corresponds to the subtype name. 

counter = 0
for shp_file in arcpy.ListFiles("*.shp"):
    shp_path = os.path.join(input_folder, shp_file)
    shp_name = os.path.splitext(os.path.basename(shp_file))[0].replace(fc_name, "")
    subtype_code = counter
    subtype_descr = shp_name
    # Turn on "arcpy.env.overwriteOutput = True" when testing a script.
    arcpy.env.overwriteOutput = True # COMMENT OUT ONCE SCRIPT COMPLETED
    arcpy.management.AddSubtype(fc_path, subtype_code, subtype_descr)
    print(f"New subtype added: {fc_path}: {subtype_descr}")
    counter += 1
    with arcpy.da.SearchCursor(shp_path, ["SHAPE@XY"]) as scursor:
        with arcpy.da.InsertCursor(fc_path, ["SHAPE@XY", "TYPECODE"]) as icursor:
            # Loop through each row in the search cursor and insert into feature class with current value of counter variable.
            # XY referencing Geometry token SHAPEXY
            for row in scursor:
                xy = row[0]
                icursor.insertRow([xy, subtype_code])

    # Increment counter for the next shapefile
    counter += 1
    print(f"Records inserted into correct subtype: {fc_path}: {subtype_descr}")
    print("")