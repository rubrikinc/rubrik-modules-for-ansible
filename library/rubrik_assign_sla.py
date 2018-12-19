#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_assign_sla
short_description: Assign a Rubrik object to an SLA Domain.
description:
    - Assign a Rubrik object to an SLA Domain.
version_added: 2.8
author: 'Rubrik Ranger Team'
options:
  object_name:
    description:
      - The name of the Rubrik object you wish to assign to an SLA Domain.
    required: true
    type: str
  sla_name:
    description:
      - The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use do not
        protect as the sla_name. To assign the selected object to the SLA of the next higher level object use clear as the sla_name
    required: true
    type: str
  object_type:
    description:
      - The Rubrik object type you want to assign to the SLA Domain.
    required: false
    default: vmware
    choices: [vmware]
    type: str
  timeout:
    description:
    - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    default: 30
    type: int

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
    description: The full API reponse for POST /internal/sla_domain/{sla_id}/assign.
    returned: on success
    type: dict
    sample: {"status_code": "204"}

response:
    description: A "No changed required" message when the Rubrik object is already assigned to the SLA Domain.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The vSphere VM 'object_name' is already assigned to the 'sla_name' SLA Domain.
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrik_cdm import load_provider_variables, rubrik_argument_spec

try:
    import rubrik_cdm
    sdk_present = True
except BaseException:
    sdk_present = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            object_name=dict(required=True, type='str'),
            sla_name=dict(required=True, type='str'),
            object_type=dict(required=False, type='str', default="vmware", choices=['vmware']),
            timeout=dict(required=False, type='int', default=30),

        )
    )
    # End Parameters

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    load_provider_variables(module)
    ansible = module.params

    try:
        rubrik = rubrik_cdm.Connect()
    except SystemExit as error:
        if "has not been provided" in str(error):
            try:
                ansible["node_ip"]
                ansible["username"]
                ansible["password"]
            except KeyError:
                module.fail_json(
                    msg="Error: The Rubrik login credentials are missing. Verify the correct env vars are present or provide them through the provider param.")
        else:
            module.fail_json(msg=str(error))

        try:
            rubrik = rubrik_cdm.Connect(ansible['node_ip'], ansible['username'], ansible['password'])
        except SystemExit as error:
            module.fail_json(msg=str(error))

    try:
        api_request = rubrik.assign_sla(ansible["object_name"], ansible["sla_name"],
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
