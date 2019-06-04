#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_end_user_authorization
short_description: Grant an Rubrik End User authorization to the provided object.
description:
    - Grant an End User authorization to the provided object.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  object_name:
    description:
      - The name of the object you wish to grant the I(end_user) authorization to.
    required: True
    type: str
  end_user:
    description:
      - The name of the end user you wish to grant authorization to.
    required: True
    type: str
  object_type:
    description:
      - The Rubrik object type you wish to grant authorization to.
    required: False
    type: str
    default: vmware
    choices: [vmware]
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
- rubrik_end_user_authorization:
    object_name: "ansible-tower"
    end_user: "ansible-user"
'''

RETURN = '''
response:
    description: The full API response for POST /internal/authorization/role/end_user
    returned: on success
    type: dict
    sample:
      {
        "hasMore": true,
        "data": [
            {
            "principal": "string",
            "privileges": {
                "destructiveRestore": [
                "string"
                ],
                "restore": [
                "string"
                ],
                "provisionOnInfra": [
                "string"
                ]
            },
            "organizationId": "string"
            }
        ],
        "total": 0
      }

response:
    description: A "No changed required" message when the end user is already authorized to interface with provided I(objec_name).
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The End User "end_user" is already authorized to interact with the "object_name" VM.
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
        object_name=dict(required=True, type='str'),
        end_user=dict(required=True, type='str'),
        object_type=dict(required=False, type='str', default="vmware", choices=['vmware']),
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

    object_name = ansible["object_name"]
    end_user = ansible["end_user"]
    object_type = ansible["object_type"]
    timeout = ansible["timeout"]

    try:
        api_request = rubrik.end_user_authorization(object_name, end_user, object_type, timeout)
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
