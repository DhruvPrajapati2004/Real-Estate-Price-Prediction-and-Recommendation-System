# Define the path to your project directory
project_dir = r'C:\Users\Data_Gathering'

# Define the subdirectories
subdirectories = ['Data', f'Data/{City}', f'Data/{City}/Flats', f'Data/{City}/Residential', f'Data/{City}/Independent House']

# Create the directory structure
for subdir in subdirectories:
    dir_path = os.path.join(project_dir, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

# Now, your directory structure is created.
