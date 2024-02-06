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
path = 'C:\\Users\\rivil\\Downloads'
file_name_sfg = 'Bagpipe State 22 G 86H 8.csv' 
full_path_sfg = os.path.join(path,file_name_sfg)
# step (2)
file_name_field = 'Copy of Occidental Petroleum Corporation_G 86H_Interval_8_DataListing.xlsx'
full_path_field = os.path.join(path,file_name_field)
# step (3)
file_name_sfg_output = file_name_sfg.split(".")[0]+'_out.'+file_name_sfg.split(".")[-1]
full_path_output = os.path.join(path,file_name_sfg_output)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# create dataFrames from files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if one file does not have any headers for some reason, remove header=0
df_sfg = pd.read_csv(full_path_sfg, header=0, index_col=None)
df_field = pd.read_excel(full_path_field,sheetname=0,header=0,index_col=False,keep_default_na=True)

 # Function to subtract subsequent rows and add empty rows
def subtract_and_add_empty_rows(df, column_name):
    result_data = []

    for i in range(len(df) - 1):
        result_data.append(df.at[i, column_name])
        print(result_data)

        diff = df.at[i, column_name] - df.at[i + 1, column_name]
        for j in range(abs(diff) - 1):
            result_data.append(np.nan)  # Adding as many empty rows as the difference

    # Adding the last value from the original DataFrame
    result_data.append(df.at[len(df) - 1, column_name])

    result_df = pd.DataFrame({column_name: result_data})

    return result_df

# Apply the function
result_df = subtract_and_add_empty_rows(df_sfg, 'timestamp')

# Reset index for the resulting DataFrame
result_df.reset_index(drop=True, inplace=True)

result_df.to_csv(full_path_output, index=False)

 
 
 
 
 

def add_empty_rows(csv_file_path):

    # Read the CSV file into a pandas DataFrame

    df = pd.read_csv(csv_file_path)

 

    # Find missing sequential numbers in the first column

    max_sequence = df.iloc[:, 0].max()

    print(max_sequence)

    all_numbers = set(range(1, max_sequence + 1))

    existing_numbers = set(df.iloc[:, 0])

    missing_numbers = sorted(all_numbers - existing_numbers)

    print(missing_numbers)

 

    # Insert empty rows for missing sequences

    for missing_number in missing_numbers:

        new_row = [missing_number] + [''] * (df.shape[1] - 1)

        df = pd.concat([df[df.iloc[:, 0] < missing_number], pd.DataFrame([new_row], columns=df.columns), df[df.iloc[:, 0] >= missing_number]])

 

    # Write the modified DataFrame back to the CSV file

    df.to_csv(csv_file_path, index=False)

 

    print(f"Empty rows added for missing sequences: {missing_numbers}")

 

# Example usage:

_directory= 'C:\\Users\\rivil\\OneDrive\\Escritorio\\edits'

file_path = glob.glob(_directory + '\\*.csv')

csv_file_path = file_path[0]

add_empty_rows(csv_file_path)