# Rubrik Modules for Ansible

## Installation

**Install the Rubrik SDK for Python.**

`pip install rubrik_cdm`

**Clone the GitHub repository to a local directory**

`git clone https://github.com/rubrikinc/rubrik-modules-for-ansible.git`

## Configuration

After cloning the GitHub repository to your local machine you will need to update your `ansible.cfg` file with the path to the `library` and `module_utiils`.

```
[defaults]

library = <path to ucsm-ansible clone>/library
module_utils   = <path to ucsm-ansible clone>/module_utils
```

## Example

```yaml
- name: Take an On-Demand Snapshot of a vSphere VM
  rubrik_on_demand_snapshot:
    object_name: 'ansible-tower-01'
    object_type: "vmware"
```