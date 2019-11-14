# Quick Start Guide: Rubrik Modules for Ansible

## Introduction to the Rubrik Modules for Ansible

Rubrik's API first architecture enables organizations to embrace and integrate
Rubrik functionality into their existing automation processes. While Rubrik APIs can be consumed natively,
companies are at various stages in their automation journey with different levels of knowledge on staff.
The Rubrik Modules for Ansible extends upon the RubrikPython SDK, transforming Rubrik API functionality
into easy to consume Ansible modules which eliminates the need to create inidividual automation scripts and extends
upon one of Rubrik's main design centers - simplicity.

## Authentication Mechanisms

The Rubrik Modules for Ansible provides two mechanisms for supplying credentials to the Ansible modules. Credentials may be accessed through the use of environment variables or manually passed into the each module task as variables.

### Authenticating with Environment Variables

Storing credentials in environment variables is a more secure process than directly hard coding them into Playbooks and ensures that your credentials are not accidentally shared if your code is uploaded to an internal or public version control system such as GitHub. If no arguments are manually passed to the Ansible module, it will attempt to read the Rubrik cluster credentials from the following environment variables:

* **`rubrik_cdm_node_ip`** (Contains the IP/FQDN of a Rubrik node)
* **`rubrik_cdm_username`** (Contains a username with configured access to the Rubrik cluster)
* **`rubrik_cdm_password`** (Contains the password for the above user)
* **`rubrik_cdm_token`** (Contains the the API token used for authentication)


#### Setting Environment Variables in macOS and \*nix

For macOS and \*nix based operating systems the environment variables can be set utilizing the export command as follows:

```
export rubrik_cdm_node_ip=192.168.0.100
export rubrik_cdm_username=user@domain.com
export rubrik_cdm_password=SecretPassword
```

```
export rubrik_cdm_node_ip=192.168.0.100
export rubrik_cdm_token=82jfjam920a
```

In order for the environment variables to persist across terminal sessions, add the above three export commands to the `~\.bash_profile` or `~\.profile` file and then run `source ~\.bash_profile` or `source ~\.profile` to ensure the environment variables are present in your current terminal session..


Once set, the Ansible modules will automatically utilize the data within the environment variables to perform its connection unless credentials are specifically passed in the arguments of the module.

### Authenticate by Providing Username and Password or API Token

There may be scenarios where directly sending credentials to the Ansible module as variables makes sense. For example, when utilizing [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) functionality. When arguments are provided, any environment variable information, populated or unpopulated, is ignored. To manually pass connection and credential information, you may use the helper `provider` variable which is a convenience paramater that allows all connection variables to be passed as a single dictionary object.

```yaml
---

- hosts: localhost
  connection: local
  gather_facts: false
  vars:
    credentials:
      node_ip: 10.255.0.2
      username: ansibledemo@rubrik.com
      password: ansiblepasswordexample

  tasks:

    - name: Rubrik Cluster Version
      rubrik_cluster_version:
        provider: "{{ credentials }}"
```

```yaml
---

- name: Rubrik Modules
  hosts: local
  connection: local
  gather_facts: false
  vars:
    credentials:
      node_ip: 10.255.0.2
      api_token: 82jfjam920a

  tasks:

    - rubrik_cluster_version:
        provider: "{{ credentials }}"
```

## Rubrik Modules for Ansible Quick Start

The following section outlines how to get started using the Rubrik Modules for Ansible, including installation, configuration, as well as sample code.

### Prerequisites

The following are the prerequisites in order to successfully install and run the sample code included in this quickstart guide:

* Ansible (tested agains v2.7.6)
* Python (Tested against v2.7.6 and v3.7.4)
* The [pip package management tool](https://pip.pypa.io/en/stable/)
* Rubrik CDM

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


### Sample Syntax - vSphere Virtual Machine On-Demand Snapshot

The following code will walk through a number of real-world examples of taking an on-demand snapshot of a vSphere VM. For a full listing of available modules see the complete [Rubrik Modules for Ansible documentation](https://rubrik.gitbook.io/rubrik-modules-for-ansible).

#### Setting up the Sample Workflow

Create a file named `rubrik.yml` in your working directory and copy in the following code:

```yaml
---

- hosts: localhost
  connection: local
  gather_facts: false
  vars:
       vm_name: ansible-node01

  tasks:

    - name: On-Demand Snapshot
      rubrik_on_demand_snapshot:
        object_name: "{{ vm_name }}"

```

#### Breaking Down the Sample Workflow

This section of code represents generic "Ansible" related configurations:

```yaml
hosts: localhost
connection: local
gather_facts: false
```

* `hosts:` corresponds to the inventory you wish to run the Ansible module against. In this case, we are providing that information through environment variables so we only need to define `localhost` in this field.
* `connection:` corresponds to the connection plugin you wish to use in your module. Since we want to execute the Playbook on the local machine we want to use the `local` connection.
* `gather_facts:` can be used to gather facts about remote hosts. Since we're running the Ansible Module on the local machine we do not need to gather this information. Setting this value to `false` is optional but recommended.

Once the Ansible specific configurations are in place we need to define the name of the vSphere VM we wish to take a on-demand snapshot of.

```yaml
vars:
       vm_name: ansible-node01
```

For the sake of simplicy we have included this variable directly in the Playbook. For production environments you can create an external variable file, with the same information, and [import that file into the Playbook](https://docs.ansible.com/ansible/latest/modules/include_vars_module.html) to keep Playbook itself more generic.

The final section in the example is the on-demand snapshot task.

```yaml
tasks:   

    - name: On-Demand Snapshot
        rubrik_on_demand_snapshot:
        object_name: "{{ vm_name }}"
```

In this example, we are automatically importing the Rubrik cluster credentials through pre-defined environment variables so there is no need to define them in the task.

* `rubrik_on_demand_snapshot` is the specific Ansible module we wish to use
* `object_name` is one of the define paramagters of the `rubrik_on_demand_snapshot` module and is referencing the previously defined `vm_name` variable.

#### Running the Sample Workflow

Once `rubrik.yml` is saved within the working directory, execute the Playbook with the following statement:

```
ansible-playbook rubrik.yml
```


## Contributing to the Rubrik Modules for Ansible

The Rubrik Modules for Ansible is hosted on a public repository on GitHub. If you would like to get involved and contribute to the Ansible Modules please follow the below guidelines.

### Common Environment Setup

1. Clone the Rubrik Modules for Ansible repository

```
git clone https://github.com/rubrikinc/rubrik-modules-for-ansible.git
```

2. Change to the repository root directory

```
cd rubrik-modules-for-ansible
```

3. Switch to the devel branch

```
git checkout devel
```


### New Module Development

The `/rubrik-modules-for-ansible/library` directory contains all of the Rubrik Ansible modules. You can also utilize the following file as a template for all new modules:

[`/rubrik-modules-for-ansible/docs/rubrik_module_template.py`](https://github.com/rubrikinc/rubrik-modules-for-ansible/blob/master/docs/rubrik_module_template.py)

To add paramters specific to the new module you can update the following section which starts on `line 60`:

```python
argument_spec.update(
        dict(
            timeout=dict(required=False, type='int', default=15),

        )
    )
```

After the new variables have been defined you can start adding any new required logic after the code block section.

```python
##################################
######### Code Block #############
##################################
##################################
```

Your final Rubrik Python SDK call should be added to `Line 93`.

```python
api_request = rubrik.
```

For example, if you wanted to call the `cluster_version()` function the line would look like:

```python
api_request = rubrik.cluster_version()
```

Once the module has been fully coded you can use the following script to automatically generate the module `DOCUMENTATION` block:


[`/rubrik-modules-for-ansible/docs/create_documentation_block.py`](https://github.com/rubrikinc/rubrik-modules-for-ansible/blob/master/docs/create_documentation_block.py)


To use the script, update the `filename = ` variable and then run `python create_documentation_block.py`



## Further Reading

* [Rubrik Modules for Ansible GitHub Repository](https://github.com/rubrikinc/rubrik-modules-for-ansible)
* [Rubrik Modules for Ansible Official Documentation](https://rubrik.gitbook.io/rubrik-modules-for-ansible)
* [Rubrik CDM API Documentation](https://github.com/rubrikinc/api-documentation)
