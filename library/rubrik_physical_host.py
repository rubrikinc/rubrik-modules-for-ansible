#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_physical_host
short_description: Add or delete a physical host from a Rubrik cluster.
description: Add or delete a physical host from a Rubrik cluster.
    -
version_added: 2.7
author: Rubrik Ranger Team
options:
  hostname:
    description:
      - The hostname or IP Address of the physical host you want to add or delete from the Rubrik cluster.
    required: True
    aliases: ip_address
  action:
    description:
      - Specify whether or not you wish to add or delete the physical host from the Rubrik cluster.
    required: True
    choices: [add, delete]
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 120


extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_physical_host:
    provider: "{{ credentials }}"
    hostname: 'ubuntu-physical-demo'
    action: 'add'

- rubrik_physical_host:
    provider: "{{ credentials }}"
    hostname: 'ubuntu-physical-demo'
    action: 'delete'
'''

RETURN = '''
response:
    description: The full API response for POST /v1/host
    returned: on success when action is add
    type: dict
    sample: 
        {
            "id": "string",
            "hostname": "string",
            "primaryClusterId": "string",
            "operatingSystem": "string",
            "operatingSystemType": "string",
            "status": "string",
            "agentId": "string",
            "compressionEnabled": true
        }

response:
    description: The full API response for DELETE /v1/host/{id}
    returned: on success when action is delete
    type: dict
    sample: {"status_code": 204}

response:
    description: A "No changed required" message when the host has already been added to the Rubrik cluster.
    returned: When the module idempotent check is succesful and action is add.
    type: str
    sample: No change requird. The host 'hostname' is already connected to the Rubrik cluster.

response:
    description: A "No changed required" message when the host is not present on the Rubrik cluster.
    returned: When the module idempotent check is succesful and action is delete.
    type: str
    sample: No change required. The host 'hostname' is not connected to the Rubrik cluster.
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, connect, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            action=dict(required=True, choices=['add', 'delete']),
            timeout=dict(required=False, type='int', default=120),

        )
    )
    # End Parameters

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    sdk_present, rubrik_cdm = sdk_validation()

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    results = {}

    load_provider_variables(module)
    ansible = module.params

    rubrik = connect(rubrik_cdm, module)
    if isinstance(rubrik, str):
        module.fail_json(msg=rubrik)

    if ansible["action"] == "add":
        try:
            api_request = rubrik.add_physical_host(ansible["hostname"], ansible["timeout"])
        except SystemExit as error:
            module.fail_json(msg=str(error))
    else:
        try:
            api_request = rubrik.delete_physical_host(ansible["hostname"], ansible["timeout"])
        except SystemExit as error:
            module.fail_json(msg=str(error))

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()