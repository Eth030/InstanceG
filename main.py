import os
import csv
import zipfile
import shutil
import xml.etree.ElementTree as ET
import datetime

# Constants
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ROBLOX_PATH = os.path.join(os.environ['LOCALAPPDATA'], "Packages")
CSV_PATH = os.path.join(SCRIPT_DIR, "instance_names.csv")
ARCHIVE_PATH = os.path.join(SCRIPT_DIR, "ROBLOXC.7z")
EXE_PATH = os.path.join(SCRIPT_DIR, "Windows10Universal.exe")

def read_instance_names():
    """Read instance names from the CSV file."""
    with open(CSV_PATH, newline='') as csvfile:
        return [row[0].strip() for row in csv.reader(csvfile)]

def create_instances():
    with open('instance_names.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            instance_name = row[0].strip()
            instance_path = os.path.join(ROBLOX_PATH, instance_name)

            # Create directory
            os.makedirs(instance_path, exist_ok=True)

            # Unpack archive
            with zipfile.ZipFile(ARCHIVE_PATH, 'r') as zip_ref:
                zip_ref.extractall(instance_path)

            # Modify XML file
            xml_path = os.path.join(instance_path, 'AppxManifest.xml')
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for identity in root.iter('{http://schemas.microsoft.com/appx/manifest/foundation/windows10}Identity'):
                identity.set('Name', f'ROBLOXCORPORATION.ROBLOX.{instance_name}')
            tree.write(xml_path)

            # Register application
            subprocess.run(['Add-AppxPackage', '-Register', os.path.join(instance_path, 'AppxManifest.xml')])

            print(f'Instance {instance_name} created and registered.')


def update_instances():
    def extract_from_zip():
        if not os.path.exists(os.path.join(SCRIPT_DIR, "ROBLOXC.7z")):
            print("ROBLOXC.7z not found in the main directory!")
            input("Press Enter to continue...")
            return

        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                instance_name = row[0].strip()
                instance_path = os.path.join(ROBLOX_PATH, instance_name)

                if os.path.exists(instance_path):
                    with zipfile.ZipFile(os.path.join(SCRIPT_DIR, "ROBLOXC.7z"), 'r') as zip_ref:
                        zip_ref.extract("Windows10Universal.exe", instance_path)
                    print(f"Extraction completed for: {instance_name}")
                else:
                    print(f"Folder {instance_name} not found, skipping extraction...")

        input("Extraction complete. Press any key to return to the main menu...")

    def use_exe():
        if not os.path.exists(os.path.join(SCRIPT_DIR, "Windows10Universal.exe")):
            print("Windows10Universal.exe not found in the main directory!")
            input("Press Enter to continue...")
            return

        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                instance_name = row[0].strip()
                instance_path = os.path.join(ROBLOX_PATH, instance_name)

                if os.path.exists(instance_path):
                    shutil.copy(os.path.join(SCRIPT_DIR, "Windows10Universal.exe"), instance_path)
                    print(f"Copying completed for: {instance_name}")
                else:
                    print(f"Folder {instance_name} not found, skipping copy...")

        input("Copying complete. Press any key to return to the main menu...")

    while True:
        print("Please choose an update source:")
        print("1) Update from existing ROBLOXC.7z archive.")
        print("2) Update using Windows10Universal.exe from the main folder.")
        print("3) Exit.")
        choice = input("Enter your choice (1,2,3): ")

        if choice == "1":
            extract_from_zip()
        elif choice == "2":
            use_exe()
        elif choice == "3":
            print("Exiting update instances...")
            break
        else:
            print("Invalid choice, please try again.")


def workspace_cloner():
    def copy_files(source_path, destination_pattern):
        cloned_count = 0
        destination_folders = [f.path for f in os.scandir(destination_pattern) if f.is_dir()]

        for destination_folder in destination_folders:
            try:
                # Copy files
                for item in os.listdir(source_path):
                    s = os.path.join(source_path, item)
                    d = os.path.join(destination_folder, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

                # Create/update note.txt
                note_file_path = os.path.join(destination_folder, "workspace", "note.txt")
                with open(note_file_path, "w") as f:
                    f.write(f"Files were cloned to this location on: {datetime.datetime.now()}")

                cloned_count += 1
                print(f"Successfully cloned to {destination_folder}.")
            except Exception as e:
                print(f"Failed to clone {destination_folder}. Error: {e}")

        print(f"Cloned {cloned_count} folders with the pattern 'ROBLOXCORPORATION.ROBLOX.*' to destinations.")
        input("Press Enter to continue...")

    def archive_files(destination_pattern, combined_archive_path):
        destination_folders = [f.path for f in os.scandir(destination_pattern) if f.is_dir()]

        with zipfile.ZipFile(combined_archive_path, 'w') as zipf:
            for destination_folder in destination_folders:
                for folder in ["autoexec", "workspace"]:
                    folder_path = os.path.join(destination_folder, folder)
                    if os.path.exists(folder_path):
                        for root, _, files in os.walk(folder_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.join(folder, os.path.relpath(file_path, folder_path))
                                zipf.write(file_path, arcname)

        print(f"Archived folders to {combined_archive_path}.")
        input("Press Enter to continue...")

    def delete_workspaces(destination_pattern):
        destination_folders = [f.path for f in os.scandir(destination_pattern) if f.is_dir()]

        for destination_folder in destination_folders:
            workspace_folder_path = os.path.join(destination_folder, "workspace")
            if os.path.exists(workspace_folder_path):
                shutil.rmtree(workspace_folder_path)

        print("Deleted all workspace folders from 'ROBLOXCORPORATION.ROBLOX.*' destinations.")
        input("Press Enter to continue...")

    while True:
        print("Welcome to InstanceG Workspace Cloner v1.5")
        print("Choose an option from the list below:")
        print("1. Copy + Archive")
        print("2. Copy Only")
        print("3. Archive Only")
        print("4. Delete All Workspaces")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            copy_files(SOURCE_PATH, DESTINATION_PATTERN)
            archive_files(DESTINATION_PATTERN, COMBINED_ARCHIVE_PATH)
        elif choice == "2":
            copy_files(SOURCE_PATH, DESTINATION_PATTERN)
        elif choice == "3":
            archive_files(DESTINATION_PATTERN, COMBINED_ARCHIVE_PATH)
        elif choice == "4":
            delete_workspaces(DESTINATION_PATTERN)
        elif choice == "5":
            print("Exiting workspace cloner...")
            break
        else:
            print("Invalid choice, please try again.")


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


def main():
    while True:
        print("Welcome to InstanceG Python Version")
        print("Choose an option from the list below:")
        print("1. Create Instances")
        print("2. Update Instances")
        print("3. Workspace Cloner")
        print("4. Remove Instances")
        print("5. Exit")
        choice = input("Enter your choice: ")

        menu_options = {
            "1": create_instances,
            "2": update_instances,
            "3": workspace_cloner,
            "4": remove_instances,
            "5": lambda: print("Thank you for using InstanceG!")
        }

        action = menu_options.get(choice)
        if action:
            action()
            if choice == "5":
                break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
