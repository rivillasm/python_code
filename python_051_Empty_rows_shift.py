import pandas as pd
import os
from datetime import datetime
import numpy as np

#    !!! ADD TIME SAMPLES TO THE SFG CSV
# 1 - Input SFG and FIELD CSVs - Input file names and path.  files in CSV format
# 2 - input the colnames and the start/end time to be used in the shift calculation 
# 3 - A DataFrame is created from the Input CSV SFG file
# 4 - Last two columns are removed from the DataFrame (removes well name and stage name)
# 5 - Empty rows are added into the DataFrame so that every single second has a corresponding row
# 6 - Output file created as CSV format
# 7 - time shift calculated within the given start/end times


# file paths for the input and output csv
# Provide a path and a file name  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ***** input sfg csv file path and name ****
path = 'C:\\Users\\rivil\\Downloads'               
file_name_sfg = 'Bagpipe State 22 G 86H 8.csv'    
full_path_sfg = os.path.join(path,file_name_sfg)  

# ***** input field csv file path and name ****
file_name_field = 'Copy of Occidental Petroleum Corporation_G 86H_Interval_8_DataListing.xlsx'
full_path_field = os.path.join(path,file_name_field)

# 
file_name_sfg_emptyrows = file_name_sfg.split(".")[0]+'_out.'+file_name_sfg.split(".")[-1]
full_path_output = os.path.join(path,file_name_sfg_emptyrows)

# *** finding the shift between  sfg and field datasets
# provide the name of the columns to be used in finding the shift between datasets ****
sfg_colname = 'Slurry Rate'
field_colname = 'SlurryRate'
# provide the times to be used in the shift calculation 
start_time = 8000
end_time = 10000


# Create dataFrames from input file
# The first row of the input file has to have the headers names
df_sfg = pd.read_csv(full_path_sfg, header=0, index_col=None)
df_sfg = df_sfg.iloc[:,:-2]     # removes the last two columns - well and stage name
print('**** Input SFG CSV file Read and two last columns removed ****' )
print("SFG CSV file columns/rows:",df_sfg.shape)
print("")

df_field = pd.read_excel(full_path_field,sheet_name=0,header=0,index_col=False,keep_default_na=True)
#df_field = pd.read_csv(full_path_field, header=0, index_col=None)
df_field = df_field[1:]
print('**** Input FIELD CSV file Read ****' )
print("FIELD CSV file columns/rows:",df_field.shape)
print("")

# transform objt into floating types
for column in df_field.columns[6:]:
    df_field[column] = df_field[column].map(lambda x: float(x))

# Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

def subtract_and_add_empty_rows(df, column_name):
    """ function to subtract subsequent timestamp of adjacent rows and add empty rows where a 
    timestamp is missing"""
    input_min = df.timestamp.min()
    input_max = df.timestamp.max()
    temp_list = []
    counts=0

    for i in range(len(df) - 1):
        temp_list.append(df.at[i, column_name])
        
        diff = int(abs(df.at[i, column_name] - df.at[i + 1, column_name])/1000)
        
        
        if(diff>1.0): 
            for j in range(abs(diff) - 1):
                counts+=1
                temp_list.append(np.nan)  # Adding as many empty rows as the difference

    # Adding the last value from the original DataFrame
    temp_list.append(df.at[len(df) - 1, column_name])

    temp_df = pd.DataFrame({column_name: temp_list})
    temp_df.reset_index(drop=True, inplace=True)
    
   
    temp_merged_df = temp_df.merge(df, how='left', left_on='timestamp', right_on=['timestamp'])
    #result_df.fillna()
    temp_min = temp_merged_df.timestamp.min()
    temp_max = temp_merged_df.timestamp.max()    
    print("Empty rows added ........ ")
    print("input data dimensions rows/columns:", df.shape)
    print("timestamp input values min, max",input_min,input_max)
    print("output data dimensions rows/columns:", temp_merged_df.shape)
    print("timestamp output values min, max",temp_min,temp_max)
    print("Added emtpy rows:", counts)
    print("")

    
    return temp_merged_df


def make_equal_length(series1, series2):
    """ makes the two series of equal length """
    len1 = len(series1)
    len2 = len(series2)
    
    if len1 > len2:
        series2 += [0] * (len1 - len2)
    elif len2 > len1:
        series1 += [0] * (len2 - len1)
    
    return series1, series2


def find_best_shift(series1, series2):
    """  find the shift between two series """
    min_diff = float('inf')
    best_shift = None
    
    # Iterate over possible shift values
    for shift in range(len(series1)):
        # Calculate sum of absolute differences for this shift
        diff_sum = sum(abs(series1[i] - series2[(i + shift) % len(series2)]) for i in range(len(series1)))
        
        # Update best shift if this shift has lower sum of absolute differences
        if diff_sum < min_diff:
            min_diff = diff_sum
            best_shift = shift
    
    return best_shift


# Apply Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
# Apply the function
df_sfg_emtpyrows = subtract_and_add_empty_rows(df_sfg, 'timestamp')
df_sfg_emtpyrows.to_csv(full_path_output, index=False, mode='w+')
print('**** Output SFG with empty rows  - CSV Format ****')
print("The following file has been created: ",full_path_output)
print("")

#  ****  TIME SHIFT calcualtion ****
print("****  TIME SHIFT Calculation ****") 
print("Making sure the series have the same lengtH............. ")
series1 = df_sfg_emtpyrows[start_time:end_time]['Slurry Rate'].interpolate().values.tolist()
series2 = df_field[start_time:end_time]['SlurryRate'].interpolate().values.tolist()
print("SFG csv file before making equal length:", len(series1))
print("FIELD csv file before making equal length:", len(series2))
      
sfg_column, field_column = make_equal_length(series1, series2)
print("SFG csv file after making equal length:", len(sfg_column))
print("FIELD csv file after making equal length:", len(field_column)) 
 

series1 = sfg_column
series2 = field_column
best_shift = find_best_shift(series1, series2)


print("")
print("****  BEST SHIFT CALCUALTION ****")
print("Calculated Best shift value:", best_shift)

