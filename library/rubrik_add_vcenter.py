#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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
module: rubrik_add_vcenter
short_description: Add a new vCenter to the Rubrik cluster.
description:
    - Add a new vCenter to the Rubrik cluster.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  vcenter_ip:
    description:
      - The IP address or FQDN of the vCenter you wish to add
    required: True
    type: str
  vcenter_username:
    description:
      - The vCenter username used for authentication.
    required: True
    type: str
  vcenter_password:
    description:
      - The vCenter password used for authentication.
    required: True
    type: str
  vm_linking:
    description:
      - Automatically link discovered virtual machines (i.e VM Linking).
    required: False
    Default: True
    type: bool
  ca_certificate:
    description:
      - CA certificiate used to perform TLS certificate validation
    required: False
    Default: None
    type: str
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 30

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_add_vcenter:
    vcenter_ip: "demo-vcsa.python.demo
    vcenter_username: "ansible_user"
    vcenter_password: "ansible_password"
'''


RETURN = '''
response:
    description: The full API response for `POST /v1/vmware/vcenter` and the job status URL which can be used to monitor progress of the adding the vCenter to the Rubrik cluster. (api_response, job_status_url)
    returned: on success
    type: tuple

response:
    description: A "No changed required" message when the vCenter has already been added to the Rubrik cluster
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The vCenter '`vcenter_ip`' has already been added to the Rubrik cluster.
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
        vcenter_ip=dict(required=True, type='str'),
        vcenter_username=dict(required=True, type='str'),
        vcenter_password=dict(required=True, type='str'),
        vm_linking=dict(required=False, default=True, type='bool'),
        ca_certificate=dict(required=False, default=None, type='str'),
        timeout=dict(required=False, type='int', default=30),

    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    vcenter_ip = ansible["vcenter_ip"]
    vcenter_username = ansible["vcenter_username"]
    vcenter_password = ansible["vcenter_password"]
    vm_linking = ansible["vm_linking"]
    ca_certificate = ansible["ca_certificate"]
    timeout = ansible["timeout"]

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.add_vcenter(
            vcenter_ip,
            vcenter_username,
            vcenter_password,
            vm_linking,
            ca_certificate,
            timeout)
    except Exception as error:
        module.fail_json(msg=str(error))

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
