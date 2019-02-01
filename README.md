#  Rubrik Ansible Modules
 
Ansible Modules that utilize the Rubrik RESTful API to manage the Rubrik Cloud Data Management Platform.

## Installation

**Install the Rubrik SDK for Python.**

`pip install rubrik_cdm`

**Clone the GitHub repository to a local directory**

`git clone https://github.com/rubrikinc/rubrik-modules-for-ansible.git`

## Quick Start

[Quick Start Guide](https://github.com/rubrikinc/rubrik-modules-for-ansible/blob/master/docs/quick-start.md)


## Documentation

[Module Documentation](https://rubrik.gitbook.io/rubrik-modules-for-ansible/)

[Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)

## Ansible Galaxy

[Galaxy Roles](https://galaxy.ansible.com/rubrik-devops)



## Example

```yaml
- rubrik_on_demand_snapshot:
    object_name: 'ansible-node01'
    object_type: "vmware"
```


