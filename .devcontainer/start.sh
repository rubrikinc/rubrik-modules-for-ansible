#!/usr/bin/env bash

# Install Ansible
echo "source /workspaces/ansible/hacking/env-setup" >> ~/.zshrc

# Alias to run Ansible Collection Centric Sanity Check
# TODO - Add script to update and then revert import path
echo "alias sanityc='rm -rf /workspaces/ansible/lib/ansible/modules/cloud/rubrikinc/ && rm -f /workspaces/ansible/lib/ansible/module_utils/rubrik_cdm.py && rm -f /workspaces/ansible/lib/ansible/plugins/doc_fragments/credentials.py && cp -a /workspaces/rubrik-modules-for-ansible/rubrikinc/cdm/. /root/.ansible/collections/ansible_collections/rubrikinc/cdm && /root/.ansible/collections/ansible_collections/rubrikinc/cdm && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/rubrik_module_template.py && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/create_documentation_block.py && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/quick-start.md && python /workspaces/rubrik-modules-for-ansible/collection_dev.py -a test && ansible-test sanity && cd -'" >> ~/.zshrc

# Alias to run "Traditional" Centric Sanity Check
echo "alias sanityt='cp -a /workspaces/rubrik-modules-for-ansible/rubrikinc/cdm/plugins/modules/. /workspaces/ansible/lib/ansible/modules/cloud/rubrikinc && cp -a /workspaces/rubrik-modules-for-ansible/rubrikinc/cdm/plugins/module_utils/. /workspaces/ansible/lib/ansible/module_utils && cp -a /workspaces/rubrik-modules-for-ansible/rubrikinc/cdm/plugins/doc_fragments/. /workspaces/ansible/lib/ansible/plugins/doc_fragments && cd /workspaces/ansible/lib/ansible/modules/cloud/rubrikinc && ansible-test sanity && cd -'" >> ~/.zshrc


# This script will automatically run after the container has been created.
# To untrack this file in git, run git update-index --skip-worktree .devcontainer/start.sh

# Set environment variables template
# echo "export rubrik_cdm_username="" >> ~/.zshrc
# echo "export rubrik_cdm_password="" >> ~/.zshrc
# echo "export rubrik_cdm_token="" >> ~/.zshrc 
