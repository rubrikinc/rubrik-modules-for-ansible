#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_get_vsphere_live_mount
short_description: Get existing Live Mounts for a vSphere VM.
description:
    - Get existing Live Mounts for a vSphere VM.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  vm_name:
    description:
      - The name of the mounted vSphere VM.
    required: True
    type: str
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 15

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''


EXAMPLES = '''
- rubrik_get_vsphere_live_mount:
    vm_name: 'ansible-tower'

'''

RETURN = '''
version:
    description: The full response of `GET /v1/vmware/vm/snapshot/mount?vm_id={vm_id}`.
    returned: success
    type: dict
'''


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
        vm_name=dict(required=True, type='str'),
        timeout=dict(required=False, type='int', default=15),

    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.get_vsphere_live_mount(
            ansible["vm_name"],
            ansible["timeout"])
    except Exception as error:
        module.fail_json(msg=str(error))

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
