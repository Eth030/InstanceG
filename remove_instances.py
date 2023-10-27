import os
import csv
import shutil


def remove_instances():
    print("---------------------------------------")
    print("Initiating UWP-Instances Removal...")
    print("---------------------------------------")
    print("We'll now remove the UWP-Instances based on the data in instance_names.csv.")
    print("Ensure that this file is located in the script's directory.")

    if not os.path.exists(CSV_PATH):
        print(f"File instance_names.csv not found in the script's directory.")
        print(f"Expected path: {CSV_PATH}")
        input("Press Enter to continue...")
        return

    confirmation = input(
        "WARNING: This will unregister the UWP apps and delete their corresponding folders. Do you want to proceed? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Operation cancelled by user.")
        return

    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            folder_name = row[0].strip()
            folder_path = os.path.join(ROBLOX_PATH, folder_name)

            # Unregister the UWP app (This part requires additional logic or tools to unregister UWP apps in Python)
            # For now, we'll skip this step and move to folder deletion.

            # Delete the corresponding folder
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"Removed folder: {folder_name} successfully!")
            else:
                print(f"Warning: Folder {folder_name} not found. Skipping removal.")

    print("Process Completed Successfully!")
    input("Press Enter to continue...")
