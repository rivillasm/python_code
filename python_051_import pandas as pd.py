import pandas as pd
import os
from datetime import datetime

#    !!! ADD TIME SAMPLES TO THE SFG CSV
# 1 - Input SFG CSV - Input file must be CSV format
# 2 - A DataFrame is created from the Input CSV SFG file
# 3 - Last two columns are removed from the DataFrame (removes well name and stage name)
# 4 - Empty rows are added into the DataFrame so that every single second has a corresponding row
# 5 - 
#   


# file paths for the input and output csv
# Provide a path and a file name  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
path = 'C:\\Users\\rivil\\Downloads'
file_name_sfg = 'Bagpipe State 22 G 86H 8.csv' 
full_path_sfg = os.path.join(path,file_name_sfg)
# Prepares an output file path/name
file_name_sfg_output = file_name_sfg.split(".")[0]+'_out.'+file_name_sfg.split(".")[-1]
full_path_output = os.path.join(path,file_name_sfg_output)


# create dataFrames from input file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The first row of the input file has to have the headers names
df_sfg = pd.read_csv(full_path_sfg, header=0, index_col=None)
df_sfg = df_sfg.iloc[:,:-2]     # removes the last two columns - well and stage name
print('**** Input file Read and two last columns removed ****' )


 # Function to subtract subsequent rows and add empty rows
 # this function adds an empty row for every single time stamp missing in the input SFG CSV file
 # the function requires the input dataframe and the header to be used (TIMESTAMP)
def subtract_and_add_empty_rows(df, column_name):
    input_min = df.timestamp.min()
    input_max = df.timestamp.max()
    result_data = []
    counts=0

    for i in range(len(df) - 1):
        result_data.append(df.at[i, column_name])   
        diff = int(abs(df.at[i, column_name] - df.at[i + 1, column_name])/1000)
        
        if(diff>1.0): 
            for j in range(abs(diff) - 1):
                counts+=1
                result_data.append(np.nan)  # Adding as many empty rows as the difference
                
                
    # Adding the last value from the original DataFrame
    result_data.append(df.at[len(df) - 1, column_name])

    temp_df = pd.DataFrame({column_name: result_data})
    temp_df.reset_index(drop=True, inplace=True)
    
   
    result_df = temp_df.merge(df, how='left', left_on='timestamp', right_on=['timestamp'])
    print('**** DataFrame with empty rows on missing sample times has been created ****')
    temp_min = result_df.timestamp.min()
    temp_max = result_df.timestamp.max()    
    
    print(" **** Statistics **** ")
    print("input data dimensions:", df.shape)
    print("timestamp min/max values - Input Dataset:",input_min,input_max)
    print("output data dimensions:", result_df.shape)
    print("timestamp min/max values - Output Dataset:",input_min,input_max)
    print("Added emtpy rows:", counts)
    
    return result_df


# Apply the function
df_sfg_output = subtract_and_add_empty_rows(df_sfg, 'timestamp')
df_sfg_output.to_csv(full_path_output, index=False)
print('**** Output DataFrame with empty rows created - CSV Format ****')

 
 
 
 
