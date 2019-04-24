#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_vcenter_refresh
short_description: Refreshes the vcenter environment that you specify.
description:
    - Retrieves the software version of the Rubrik cluster.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>


extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- name: Retrieve the software version of the Rubrik cluster
  vmware_vcenter_refresh:
'''

RETURN = '''
version:
    description: The version of the Rubrik cluster.
    returned: success
    type: str
    sample: 4.1.3-2510
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec

try:
    import rubrik_cdm
    HAS_RUBRIK_SDK = True
except ImportError:
    HAS_RUBRIK_SDK = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = dict(
        vcenter_ip=dict(required=True, type='str'),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    wait_for_completion=False

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password)
    except SystemExit as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.refresh_vcenter(ansible["vcenter_ip"], wait_for_completion)
    except SystemExit as error:
        module.fail_json(msg=str(error))
    #fixed
    module.exit_json(**api_request)


if __name__ == '__main__':
    main()
