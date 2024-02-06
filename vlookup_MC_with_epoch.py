import pandas as pd
import os
from datetime import datetime

#                               !!!INPUT FILES NEED TO BE CSV FORMAT!!!
#           As usual make sure to format any timestamps in the input files as number,
#           or else this script will read all timestamps as '#.###E+12'

#                                   Changes/input needed to run this script:
#                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   1. file path for the csv with all timestamps, probably fracBRAIN stage download (sfg.csv).
#   2. file path for the csv with list of timestamps you want to match, i.e. field csv (field.csv)
#   3. file path for the output csv that will be the two files above, merged via vlookup (output.csv)
#   4. make sure both input files have the same header name for timestamp column. Best to use 'timestamp'
#      as the header name.
#   5. select if you want to add an epoch timestamp column to field csv - add_timestamp = "y"
#   6. select if you want to delete the unit row (extra row below headers) - delete_unit_row = "y"
#   7. select a time_offset, if needed, to shift the field csv by x amount of seconds.
#   8. (OPTIONAL) save the file you just added to timestamps to. saves to a new file, does not overwrite.

#   


# file paths for the input and output csv~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# step (1)
file_path_sfg = r'C:\\Users\\MitchellCollett\\OneDrive - shearfrac.com\\Desktop\\FB Code\V-Look_up\\Bagpipe State 22 G 86H 16.csv'
# step (2)
file_path_field = r'C:\\Users\\MitchellCollett\\OneDrive - shearfrac.com\\Desktop\\FB Code\V-Look_up\\oxy_G_stage16_Field.csv' 
# step (3)
file_path_output = r'C:\\Users\\MitchellCollett\\OneDrive - shearfrac.com\\Desktop\\FB Code\V-Look_up\\oxy_G86H_16_output.csv' 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# create dataFrames from files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if one file does not have any headers for some reason, remove header=0
df_sfg = pd.read_csv(file_path_sfg, header=0, index_col=None)
df_field = pd.read_csv(file_path_field, header=0, index_col=None)
#df_field = pd.read_csv(file_path_field, index_col = None)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# enter header name for the timestamp columns. Make sure these are the same in both files ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if adding a timestamp column with this script, the header will default to timestamp ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# step (4)
timestamp_header = 'timestamp'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# do you want this script to insert a timestamp column into the field csv?
# if you do, set add_timestamp = "y".
# if your field csv already has timestamp in EPOCH time, set add_timestamp = "n"
# step (5)
add_timestamp = "y"
#add_timestamp = "n"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#does the field csv have a row for units that you want to delete?
#set unit_row = "y" if it does. If not, set unit_row = "n"
# step (6)
delete_unit_row = "y"
#unit_row = "n"

if delete_unit_row == "y":
    df_field = df_field.iloc[1:]
    print ("unit row has now been deleted")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# START of ADD TIMESTAMP BLOCK - this block will add a timestamp column as the first column of the field.csv
# Comment this WHOLE BLOCK out if you do not want a timestamp column added, and just want to merge via vlookup.


# Use time_offset to shift the field csv data. Enter the value in seconds.
# If you want to push the field csv curves FORWARD, use a positive value. Negative to push the curves backward
# for no shift, set to 0.

# step (7)
time_offset = 70
#time_offset = 0

if add_timestamp == "y":
    
    converted_timestamp_list = []
    for index, row in df_field.iterrows():

        #enter the column name(s) of the date and time.
        #Common header names are included here.
        #datatimestamp = str(row['Date']) + str(" ") + str(row['Time'])
        #datatimestamp = str(row['Job Time'])
        #datatimestamp = str(row['Date'])
        datatimestamp = str(row['PumpTime'])

        #enter the format of the date and time you want to convert into epoch timestamp
        #Common date/time formats are included here, note the use of / and - to separate day/month/year (d-m-y)
        #timestampformat = '%m-%d-%Y %H:%M:%S'
        #timestampformat = '%m/%d/%Y %H:%M:%S'
        #timestampformat = '%d/%m/%Y %H:%M:%S'
        timestampformat = '%Y-%m-%d %H:%M:%S'
        #timestampformat = '%m/%d/%Y %I:%M:%S %p'

        utc_time = datetime.strptime(datatimestamp, timestampformat)               
        epoch = (utc_time - datetime(1970, 1, 1)).total_seconds()
        epoch = int(epoch*1000)+int(time_offset*1000)
        converted_timestamp_list.append(epoch)
        
    df_field.insert(0,'timestamp', converted_timestamp_list)  

    # OPTIONAL BLOCK ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # use this section to save the csv you've just added a timestamp to, to an output file that will be in the
    # same location as the input, with the file name ending in "_with_timestamp.csv"
    # step (8 optional) - uncommment following 4 lines to save new csv with timestamp

    #output = str(file_path_field) + str("_with_timestamp.csv")  
    #print("Exporting ", output)
    #export_csv = df_field.to_csv(output, index = None, header=True)
    #print(output, " exported.")

    #END OF OPTIOINAL BLOCK
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# END OF ADD TIMESTAMP BLOCK ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# VLOOKUP BLOCK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

merged_df = pd.merge(df_sfg, df_field, on='timestamp', how='left')
merged_df = merged_df.fillna('nan')
merged_df.to_csv(file_path_output, index=False)

# VLOOKUP BLOCK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~