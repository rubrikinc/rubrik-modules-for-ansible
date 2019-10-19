#!/usr/bin/env bash

echo "source /workspaces/ansible/hacking/env-setup" >> ~/.zshrc
echo "source /workspaces/ansible/hacking/env-setup" >> ~/.zshrc

echo "alias sanity='cp -a /workspaces/rubrik-modules-for-ansible/rubrikinc/cdm/. /root/.ansible/collections/ansible_collections/rubrikinc/cdm && /root/.ansible/collections/ansible_collections/rubrikinc/cdm && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/rubrik_module_template.py && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/create_documentation_block.py && rm /root/.ansible/collections/ansible_collections/rubrikinc/cdm/docs/quick-start.md && ansible-test sanity && cd -'" >> ~/.zshrc

 






# This script will automatically run after the container has been created.
# To untrack this file in git, run git update-index --skip-worktree .devcontainer/start.sh

# Set environment variables template
# echo "export rubrik_cdm_username="" >> ~/.zshrc
# echo "export rubrik_cdm_password="" >> ~/.zshrc
# echo "export rubrik_cdm_token="" >> ~/.zshrc 
