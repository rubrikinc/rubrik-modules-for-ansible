# Rubrik Ansible Modules
 
Ansible Modules that utilize the Rubrik RESTful API to manage the Rubrik Cloud Data Management Platform.

# Installation

**Install the Rubrik SDK for Python.**

`pip install rubrik_cdm`

**Clone the GitHub repository to a local directory**

`git clone https://github.com/rubrikinc/rubrik-modules-for-ansible.git`

# Example

```yaml
- rubrik_on_demand_snapshot:
    object_name: 'ansible-node01'
    object_type: "vmware"
```

# Documentation

Here are some resources to get you started! If you find any challenges from this project are not properly documented or are unclear, please [raise an issue](https://github.com/rubrikinc/rubrik-modules-for-ansible/issues/new/choose) and let us know! This is a fun, safe environment - don't worry if you're a GitHub newbie!

* [Quick Start Guide](https://github.com/rubrikinc/rubrik-modules-for-ansible/blob/master/docs/quick-start.md)
* [Module Documentation](https://rubrik.gitbook.io/rubrik-modules-for-ansible/)
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)
* [VIDEO: Getting Started with the Rubrik Modules for Ansible](https://www.youtube.com/watch?v=B5MGkiJyIeI&t=1s)
* [BLOG: Using Ansible with Rubrik Just Got Easier!](https://www.rubrik.com/blog/rubrik-modules-redhat-ansible/)

# How You Can Help

We glady welcome contributions from the community. From updating the documentation to adding more functions for Ansible, all ideas are welcome. Thank you in advance for all of your issues, pull requests, and comments! :star:

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

# License

* [MIT License](LICENSE)

# About Rubrik Build

We encourage all contributors to become members. We aim to grow an active, healthy community of contributors, reviewers, and code owners. Learn more in our [Welcome to the Rubrik Build Community](https://github.com/rubrikinc/welcome-to-rubrik-build) page.

We'd  love to hear from you! Email us: build@rubrik.com
