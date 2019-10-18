import fileinput
import os

collections_path = "from ansible_collections.rubrikinc.cdm.plugins.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec"
standard_path = "from ..module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec"

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