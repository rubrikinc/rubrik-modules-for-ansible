# Rubrik Ansible Module

## Overview

Contains the module for managing Rubrik services for managed Ansible nodes.

## Installation

1. Clone repo to destination host
1. cd to `module-utils/RubrikLib`, run `sudo -H python setup.py install`
1. cd to `module-utils/RubrikLib_Int`, run `sudo -H python setup.py install`
1. cp `module-utils/pyRubrik.py` to your Ansible module_utils path (in my case it was `/usr/local/lib/python2.7/dist-packages/ansible/module_utils`)

### Playbooks

#### test_conn

Tests the connection to the Rubrik cluster, throwing an error if the connection cannot be made.

```yaml
---
- hosts: localhost
  tasks:
    - name: Test connection to Rubrik 
      test_conn:
        node: "rubrik.demo.com"
        rubrik_user: "foo"
        rubrik_pass: "bar"
```

Example output:

```
tim@th-ubu-chef-client:~/ansible$ ansible-playbook test_conn.yml

PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [Test connection to Rubrik] ***************************************************************
ok: [localhost]

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   
```

#### set_sla

This playbook takes the list of VMware VMs presented in the `with_items` list, and sets their SLA domain to match the value provided in `sla_domain`.

```yaml
---
- hosts: localhost
  tasks:
    - name: Test connection to Rubrik 
      test_conn:
        node: "rubrik.demo.com"
        rubrik_user: "foo"
        rubrik_pass: "bar"
        vmware_vm_name: "{{ item.vmware_vm_name }}"
        sla_domain: "Bronze"
    with_items:
      - { vmware_vm_name: 'th-ubu-chef-client' }
```

Example output:

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook set_sla.yml

PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [Set SLA for VMware Virtual Machine] ******************************************************
ok: [localhost] => (item={u'vmware_vm_name': u'th-ubu-chef-client'})

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0                                   
```