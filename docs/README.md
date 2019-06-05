# Rubrik Modules for Ansible

## Installation

**Install the Rubrik SDK for Python.**

`pip install rubrik_cdm`

**Clone the GitHub repository to a local directory**

`git clone https://github.com/rubrikinc/rubrik-modules-for-ansible.git`

## Configuration

The cloned repository includes a `ansible.cfg` file that is pre-configured with the correct paramaters to run the Ansible modules from the local directory.

```
[defaults]

library = ./library
module_utils   = ./module_utils
```

## Example

```yaml
- name: Take an On-Demand Snapshot of a vSphere VM
  rubrik_on_demand_snapshot:
    object_name: 'ansible-tower-01'
    object_type: "vmware"
```