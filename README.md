# Rubrik Ansible Module

##  Overview

Contains the module for managing Rubrik services for managed Ansible nodes.

## Installation

1. Clone repo to destination host
1. cd to `module-utils/RubrikLib`, run `sudo -H python setup.py install`
1. cd to `module-utils/RubrikLib_Int`, run `sudo -H python setup.py install`
1. cp `module-utils/pyRubrik.py` to your Ansible module_utils path (in my case it was `/usr/local/lib/python2.7/dist-packages/ansible/module_utils`)

## Playbooks

#### cluster_info

Tests the connection to the Rubrik cluster, returns info about the cluster throwing an error if the connection cannot be made.

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

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook cluster_info.yml -v
PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [Test connection to Rubrik] ***************************************************************
ok: [localhost] => {"changed": false, "debug_out": [], "failed": false, "message": {"api_version": "1", "id": "89fc0d86-6f1c-4652-aefa-37b7ba0e6229", "version": "4.0.3-474"}}

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=
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

#### od_backup

This playbook takes an on-demand snapshot of the object specified in the confiugration.

```yaml
---
- hosts: localhost
  tasks:
    - name: On-demand VMware backup of list of VMs 
      od_backup:
        node: "rubrik.demo.com"
        rubrik_user: "foo"
        rubrik_pass: "bar"
        object_type: "vmware_vm"
        vmware_vm_name: "{{ item.vmware_vm_name }}"
      with_items:
      - { vmware_vm_name: 'th-ubu-chef-client' }
```

Example output:

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook od_backup.yml -v

PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [On-demand VMware backup of list of VMs] **************************************************
changed: [localhost] => (item={u'vmware_vm_name': u'th-ubu-chef-client'}) => {"changed": true, "debug_out": [], "failed": false, "item": {"vmware_vm_name": "th-ubu-chef-client"}}

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0
```

#### register_host

Registers the given hosts with the Rubrik cluster. NOTE: the hosts will need to be resolvable via DNS by the Rubrik cluster, or IP addresses used instead of hostnames, and Rubrik Connector should have already been installed.

```yaml
---
- hosts: localhost
  tasks:
    - name: Register host with Rubrik cluster 
      register_host:
        node: "rubrik.demo.com"
        rubrik_user: "foo"
        rubrik_pass: "bar"
        host_name: "{{ item.host_name }}"
      with_items:
      - { host_name: '172.21.11.119' }
```

Example output:

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook register_host.yml -v
PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [Register host with Rubrik cluster] *******************************************************
changed: [localhost] => (item={u'host_name': u'172.21.11.119'}) => {"changed": true, "debug_out": [], "failed": false, "item": {"host_name": "172.21.11.119"}}

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0
```

#### fileset

Creates or updates a fileset, or filesets for the list of hosts and fileset templates given in the configuration.

```yaml
---
- hosts: localhost
  tasks:
    - name: Create or modify a fileset
      fileset:
        node: "rubrik.demo.com"
        rubrik_user: "foo"
        rubrik_pass: "bar"
        host_name: "{{ item.host_name }}"
        fileset_template: "{{ item.fileset_template }}"
        sla_domain: "Bronze"
      with_items:
      - { host_name: '172.21.11.119', fileset_template: 'th-allthethings' }
      - { host_name: '172.21.11.119', fileset_template: 'th-test-fileset' }
```

Example output:

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook fileset.yml -v

PLAY [localhost] *******************************************************************************

TASK [Gathering Facts] *************************************************************************
ok: [localhost]

TASK [Create or modify a fileset] **************************************************************
ok: [localhost] => (item={u'fileset_template': u'th-allthethings', u'host_name': u'172.21.11.119'}) => {"changed": false, "debug_out": ["Fileset already exists, with id Fileset:::a967f2f2-6ec9-443d-8192-85670398d361", "Fileset is already configured with the correct SLA domain"], "failed": false, "item": {"fileset_template": "th-allthethings", "host_name": "172.21.11.119"}}
ok: [localhost] => (item={u'fileset_template': u'th-test-fileset', u'host_name': u'172.21.11.119'}) => {"changed": false, "debug_out": ["Fileset already exists, with id Fileset:::5c061039-b9cb-49b8-a3ca-398546de672c", "Fileset is already configured with the correct SLA domain"], "failed": false, "item": {"fileset_template": "th-test-fileset", "host_name": "172.21.11.119"}}

PLAY RECAP *************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0
```
#### connector_win

Installs the Rubrik Connector Service on a Windows machine, and configures the service to start with the provided service account.

```yaml
---
- hosts: windows
  vars:
    rubrik_cluster: "rubrik.demo.com"
    service_user: "sa_rubrik@demo.com"
    service_pass: "Password123!"
  tasks:
    - name: Create temp folder, if it doesn't exist
      win_file:
        path: C:\Temp
        state: directory
    - name: Download Rubrik connector
      win_get_url:
        url: "https://{{ node }}/connector/RubrikBackupService.zip"
        dest: C:\Temp\RubrikBackupService.zip
        validate_certs: no
        force: no
    - name: Unzip connector archive
      win_unzip:
        src: C:\Temp\RubrikBackupService.zip
        dest: C:\Temp\
    - name: Install connector software
      win_package:
        path: C:\Temp\RubrikBackupService.msi
        state: present
        creates_service: 'Rubrik Backup Service'
        wait: yes
    - name: Set logon for service
      win_service:
        username: "{{ service_user }}"
        password: "{{ service_pass }}"
        name: 'Rubrik Backup Service'
```

Example output:

```none
tim@th-ubu-chef-client:~/ansible$ ansible-playbook connector_win.yml 

PLAY [windows] ************************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [172.17.60.179]
ok: [172.17.60.229]

TASK [Create temp folder, if it doesn't exist] ****************************************
ok: [172.17.60.229]
ok: [172.17.60.179]

TASK [Download Rubrik connector] ******************************************************
ok: [172.17.60.179]
ok: [172.17.60.229]

TASK [Unzip connector archive] ********************************************************
changed: [172.17.60.179]
changed: [172.17.60.229]

TASK [Install connector software] *****************************************************
ok: [172.17.60.179]
ok: [172.17.60.229]

TASK [Set logon for service] **********************************************************
ok: [172.17.60.179]
ok: [172.17.60.229]

PLAY RECAP ****************************************************************************
172.17.60.179              : ok=6    changed=1    unreachable=0    failed=0   
172.17.60.229              : ok=6    changed=1    unreachable=0    failed=0   
```

## Disclaimer

CODE HERE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
