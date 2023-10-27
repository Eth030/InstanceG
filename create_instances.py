import os
import csv
import zipfile
import xml.etree.ElementTree as ET
import subprocess


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
