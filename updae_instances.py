import os
import csv
import zipfile
import shutil


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
