# This file will update the module_utils import path in all modules to support Ansible Collections and then create the collection .tar

import fileinput
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', choices=['build', 'update_path'], required=True, help='Specify which action (build or test) you wish to use.')
parser.add_argument('-p', '--platform', choices=['vscode', 'circleci'], default="vscode", required=False, help='The platform you wish to run the script against.')

arguments = parser.parse_args()

collections_path = "from ansible_collections.rubrikinc.cdm.plugins.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec"
standard_path = "from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec"




if arguments.action == 'build':
    # Create a list of all modules for processing
    modules = []
    for dir_path, _, file_name in os.walk('./rubrikinc/cdm/plugins/modules'):
        for file in file_name:
            modules.append(os.path.join(dir_path, file))

    # Update import path to support Ansible Collections
    for m in modules:
        with fileinput.FileInput(m, inplace=True) as file:
            for line in file:
                print(line.replace(standard_path, collections_path), end='')


    # Switch to the Collection directory and build the collection
    os.chdir('./rubrikinc/cdm')
    os.system('ansible-galaxy collection build')


    # Switch back to the root dir
    os.chdir('../..')


    # Revert changes to the import paths
    for m in modules:
        with fileinput.FileInput(m, inplace=True) as file:
            for line in file:
                print(line.replace(collections_path, standard_path), end='')
else:
    # Create a list of all modules for processing
    modules = []

    if arguments.platform == 'circleci':
        search_directory = os.walk("/home/circleci/.ansible/collections/ansible_collections/rubrikinc/cdm")
    else:
        search_directory = os.walk("/root/.ansible/collections/ansible_collections/rubrikinc/cdm/plugins/modules")
        print("VS Code")
    for dir_path, _, file_name in search_directory:
        for file in file_name:
            if '__pycache__' not in dir_path:
                modules.append(os.path.join(dir_path, file))
    # Update import path to support Ansible Collections
    for m in modules:
        print(m)
        with fileinput.FileInput(m, inplace=True) as file:
            for line in file:
                print(line.replace(standard_path, collections_path), end='')
    
    

