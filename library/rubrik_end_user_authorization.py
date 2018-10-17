#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
version_added: 2.7
author: Rubrik Ranger Team
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
      - The Rubrik object type you wish to backup.
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
- rubrik_assign_sla:
    object_name: "ansible-tower"
    sla_name: "Gold"
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, connect, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            object_name=dict(required=True, type='str'),
            end_user=dict(required=True, type='str'),
            object_type=dict(required=False, type='str', default="vmware", choices=['vmware']),
            timeout=dict(required=False, type='int', default=15),

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

    try:
        api_request = rubrik.end_user_authorization(ansible["object_name"], ansible["end_user"],
                                                    ansible["object_type"], ansible["timeout"])
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
