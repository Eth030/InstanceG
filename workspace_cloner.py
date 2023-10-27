import os
import csv
import zipfile
import shutil


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
