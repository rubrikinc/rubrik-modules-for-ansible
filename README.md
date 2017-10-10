# Rubrik Ansible Module

## Overview

Contains the module for managing Rubrik services for managed Ansible nodes.

## Installation

1. Clone repo to destination host
1. cd to `module-utils/RubrikLib`, run `sudo -H python setup.py install`
1. cd to `module-utils/RubrikLib_Int`, run `sudo -H python setup.py install`
1. cp `module-utils/pyRubrik.py` to your Ansible module_utils path (in my case it was `/usr/local/lib/python2.7/dist-packages/ansible/module_utils`)
1. Replace the following in `test_conn.yml`:
    * `node` - the IP/FQDN of the Rubrik cluster
    * `rubrik_user` - the username for the Rubrik cluster
    * `rubrik_pass` - the password for the Rubrik cluster
1. Run `ansible-playbook test_conn.yml`

Output should be similar to:
```
tim@th-ubu-chef-client:~/ansible$ ansible-playbook test_conn.yml
 [WARNING]: Unable to parse /etc/ansible/hosts as an inventory source

 [WARNING]: No inventory was parsed, only implicit localhost is available

 [WARNING]: Could not match supplied host pattern, ignoring: all

 [WARNING]: provided hosts list is empty, only localhost is available


PLAY [localhost] **************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************
ok: [localhost]

TASK [Test connection to Rubrik] **********************************************************************************
ok: [localhost]

PLAY RECAP ********************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   
```