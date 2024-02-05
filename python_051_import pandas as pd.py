import pandas as pd

import glob

 

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