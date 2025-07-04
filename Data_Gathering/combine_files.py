# Function to combine multiple csv file is one file.
def combine_csv_files(folder_path, combined_file_path):
    combined_data = pd.DataFrame()  # Create an empty DataFrame to hold the combined data

    # Iterate through all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            print(f'Processing: {file_path}')

            # Check if the file is empty
            if os.stat(file_path).st_size == 0:
                print(f"Warning: Skipping empty file - {file_name}")
                continue
            
            try :
                # Read the data from the current CSV file
                df = pd.read_csv(file_path)
                # Append the data to the combined DataFrame
                combined_data = pd.concat([combined_data,df],ignore_index=True)
                # Delete the original CSV file
                os.remove(file_path)
            except pd.errors.EmptyDataError:
                print(f"Error: EmptyDataError for file - {file_name}, skipping.")
                continue
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue
