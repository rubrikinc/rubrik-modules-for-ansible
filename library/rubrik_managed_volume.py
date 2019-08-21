#!/usr/bin/python
# (c) 2018 Rubrik, Inc
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
module: rubrik_managed_volume
short_description: Begin or end snapshots on a Rubrik Managed Volume.
description:
    - Begin or end snapshots on a Rubrik Managed Volume.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  managed_volume_name:
    description:
      - The name of the Managed Volume to begin or end the snapshot on.
    required: True
    aliases: ["name"]
  sla_name:
    description:
      - The SLA Domain name you want to assign the snapshot to. By default, the currently assigned SLA Domain will be used.
        This parameter is only required when the I(action) is end.
    required: False
    type: str
    default: current
  action:
    description:
      - Specify whether or not you wish to begin or end a snapshot.
    required: True
    choices: [begin, end]
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
# Begin a new managed volume snapshot.
- rubrik_managed_volume:
    name: MV1
    action: begin

# End the managed volume snapshot
- rubrik_managed_volume:
    provider: "{{ credentials }}"
    name: MV1
    action: end
'''

RETURN = '''
response:
    description: The full API response for POST /internal/managed_volume/{id}/begin_snapshot
    returned: on success when action is begin
    type: dict
    sample: {"status_code": "204"}

response:
    description: The full API response for POST /internal/managed_volume/{id}/end_snapshot
    returned: on success when action is end
    type: dict
    sample: {"status_code": "204"}

response:
    description: A "No changed require" message when the managed volume is already in a writable state.
    returned: When the module idempotent check is succesful and action is begin.
    type: str
    sample: No change required. The Managed Volume 'I(managed_volume_name)' is already assigned in a writeable state.

response:
    description: A "No changed required" message when the managed volume is already in a read only state.
    returned: When the module idempotent check is succesful and action is begin.
    type: str
    sample: No change required. The Managed Volume 'I(managed_volume_name)' is already assigned in a read only state.
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
        managed_volume_name=dict(required=True, aliases=['name']),
        sla_name=dict(required=False, type='str', default="current"),
        action=dict(required=True, choices=['begin', 'end']),
        timeout=dict(required=False, type='int', default=15),
    )

    argument_spec.update(rubrik_argument_spec)

    required_if = [
        ('action', 'end', ['sla_name'])
    ]

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

    if ansible["action"] == "begin":
        try:
            api_request = rubrik.begin_managed_volume_snapshot(ansible["managed_volume_name"], ansible["timeout"])
        except Exception as error:
            module.fail_json(msg=str(error))

    else:
        try:
            api_request = rubrik.end_managed_volume_snapshot(
                ansible["managed_volume_name"], ansible["sla_name"], ansible["timeout"])
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
