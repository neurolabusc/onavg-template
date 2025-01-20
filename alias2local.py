import os
import subprocess
import shutil

# Define the root folder
root_folder = '/Users/chris/src/core/onavg-ico32'
parent_folder = os.path.dirname(root_folder)  # Parent directory of the root folder

# Walk through the directory tree to find .npy files
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.npy'):
            full_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, root_folder)  # Relative path from the root folder
            subfolder_names = relative_path.replace(os.sep, '_')  # Replace folder separators with '_'
            new_filename = f"{os.path.basename(root_folder)}_{subfolder_names}_{filename}"  # New filename
            new_file_path = os.path.join(parent_folder, new_filename)  # Full path for the new file

            try:
                # Run the git annex commands
                print(f"Processing: {full_path}")
                subprocess.run(['git', 'annex', 'get', full_path], check=True)
                subprocess.run(['git', 'annex', 'unlock', full_path], check=True)

                # Copy the file to the parent folder with the new name
                print(f"Copying to: {new_file_path}")
                shutil.copy(full_path, new_file_path)

            except subprocess.CalledProcessError as e:
                print(f"Error processing {full_path}: {e}")
            except OSError as e:
                print(f"Error copying {full_path} to {new_file_path}: {e}")
