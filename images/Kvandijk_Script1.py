##Assignment 1: Script 1
##GEOM73|C61|10034371
##Created January 25, by Kevin Van Dijk
##Tested using Python 3.9.11 64-bit
#Assuming the user knows this script is to be run outside of ArcGIS Pro.
import os
import arcpy
import openpyxl

print("")
print("------------------------------------------------------------------------------")
print("This script is used to complete a quick inventory on a folder in the database.")
print("------------------------------------------------------------------------------")
print("")
#---------START Input Folder---------------------------------------------------------------------------------------
while True:
    
    # User sets the workspace by inputing the path to a specified input folder
    in_folder = input("Enter the path to the input folder: ")
    print("")
    arcpy.env.workspace = in_folder
    
    # Print the name of the input folder so we can identify correct path was entered.
    #.basename grabs folder name from input folder path
    # normpath function within os.path to normalized file path name, e.g convert forward slashes to backslashes in Windows. Not sure if this is needed.
    folder_name = os.path.basename(os.path.normpath(in_folder))
    print("Input folder name: " + folder_name)
    print("")

    # Check/confirm if the input folder is correct.
    # If folder is not correct enter new input folder. This will loop until user confirms it is the correct input.
    confirm = input("Is the folder name correct? (yes/no): ")
    if confirm.lower() == "yes":
        break
    else:
        print("--------------------------------------------")
        print("Please enter a new path to the input folder.")
        print("")
print("-----------------------------------------------------")            
print("Processing......")
print("Creating inventory......")
print("-----------------------------------------------------") 
print("Excel/Shapefile Inventory for folder: " + folder_name) 
print("-----------------------------------------------------") 
print("")
#-------END Input Folder---------------------------------------------------------------------------------------------------
#-------START os.walk Function---------------------------------------------------------------------------------------------
# Using the os.walk function to get all the files in the folder
# Top-level workspace is in_folder.
# Took this os.walk setup from: https://pro.arcgis.com/en/pro-app/latest/arcpy/data-access/walk.htm
# Yields a tuple of three that includes the workspace, directory names, and file names.
# dirpath is the path to the workspace as a string.
# dirnames is a list of names of subdirectories and other workspaces in dirpath.
# filenames is a list of names of nonworkspace contents in dirpath.


shp_list = []
xl_list = []
for dirpath, dirnames, filenames in os.walk(in_folder):
    for filename in filenames:
        # check if the file is a .xlsx or .xls
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            xl_list.append(os.path.join(dirpath, filename))
        # check if the file is a shapefile .shp
        elif filename.endswith(".shp"):
            shp_list.append(os.path.join(dirpath, filename)) 
count_xl = len(xl_list)
count_shp = len(shp_list)        
# Print the total number of Excel/Shape files
print("Total number of Excel files (.xlsx/.xls): " + str(count_xl))
print("Total number of shapefiles (.shp): " + str(count_shp))
print("")
print("----------------------------------------------------")
#-------END os.walk Function--------------------------------------------------------------------------------------------- 
#-------START Cursor funtion--------------------------------------------------------------------------------------------- 
# Assuming that total number of features means total number of rows/entries in attribute table.
for shp in shp_list:
    cursor = arcpy.da.SearchCursor(shp, "*")
    row_count = 0
    for row in cursor:
        row_count += 1
    print(f"The total feature count for", shp, "is: ", row_count)
    
#-------END Cursor funtion--------------------------------------------------------------------------------------------- 
#-------START openpyxl funtion-----------------------------------------------------------------------------------------
# Modified a script I found online from: https://gis.stackexchange.com/questions/65035/reading-excel-sheet-in-arcpy-script
# Used some of this code to help figure out openpyxl: https://community.esri.com/t5/python-questions/how-to-update-existing-excel-xlsx-file-using/m-p/1065848
for xl in xl_list:
    workbook = openpyxl.load_workbook(xl)
    sheet = workbook.active
    row_count = sheet.max_row
    print("----------------------------------------------------")
    print(f"The total row count for {xl} is {row_count}")
    print("----------------------------------------------------")
    print("Calculating field names for all .shp where shapeType = Point")
    print("")
#-------END openpyxl funtion-----------------------------------------------------------------------------------------
#-------START ListFields funtion-------------------------------------------------------------------------------------
# Modified from: https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/listfields.htm
if arcpy.da.Describe(shp_list[0])["shapeType"] == "Point":
        ListFields = arcpy.ListFields(shp_list[0])
        for fields in ListFields:
            print(f"Field Name for {shp_list[0]} is: {fields.name}")
#-------END ListFields funtion-------------------------------------------------------------------------------------
print("")
print("------END OF DATABASE INVENTORY------")
print("")


