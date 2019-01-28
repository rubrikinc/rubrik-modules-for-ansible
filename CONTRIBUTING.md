<<<<<<< HEAD
# Rubrik Modules for Ansible Development Guide

Contributions via GitHub pull requests are gladly accepted from their original author. Along with any pull requests, please state that the contribution is your original work and that you license the work to the project under the project's open source license. Whether or not you state this explicitly, by submitting any copyrighted material via pull request, email, or other means you agree to license the material under the project's open source license and warrant that you have the legal authority to do so.

## Common Environment Setup

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


## New module Development

The `/rubrik-modules-for-ansible/library` directory contains all of the Rubrik Ansible modules. You can also utilize the following file as a template for all new modules:

`/rubrik-modules-for-ansible/docs/rubrik_module_template.py`

To add paramters specific to the new module you can can update the following section which starts on `line 60`:

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

``/rubrik-modules-for-ansible/docs/create_documentation_block.py`

To use the script, update the `filename = ` variable and then run `python create_documentation_block.py`
=======
Contributions via GitHub pull requests are gladly accepted from their original author. Along with any pull requests, please state that the contribution is your original work and that you license the work to the project under the project's open source license. Whether or not you state this explicitly, by submitting any copyrighted material via pull request, email, or other means you agree to license the material under the project's open source license and warrant that you have the legal authority to do so.
>>>>>>> 15a2b4b0cf4b50dfa428e6bfc3a6eb3a273ce8ff
