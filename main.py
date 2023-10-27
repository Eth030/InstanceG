import os
import csv
import zipfile
import shutil
import xml.etree.ElementTree as ET
import datetime

# Paths and Constants
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ROBLOX_PATH = os.path.join(os.environ['LOCALAPPDATA'], "Packages")
CSV_PATH = os.path.join(SCRIPT_DIR, "instance_names.csv")
ARCHIVE_PATH = os.path.join(SCRIPT_DIR, "ROBLOXC.7z")
EXE_PATH = os.path.join(SCRIPT_DIR, "Windows10Universal.exe")

def create_instances():
    # ... [Same as before]

def update_instances():
    # ... [Same as before]

def workspace_cloner():
    # ... [Same as before]

def remove_instances():
    # ... [Same as before]

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

        if choice == "1":
            create_instances()
        elif choice == "2":
            update_instances()
        elif choice == "3":
            workspace_cloner()
        elif choice == "4":
            remove_instances()
        elif choice == "5":
            print("Thank you for using InstanceG!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
