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
module: rubrik_add_organization_protectable_object_sql_server_availability_group
short_description: Add a MSSQL Availability Group to an organization as a protectable object.
description:
    - Add a MSSQL Availability Group to an organization as a protectable object.
version_added: '2.9'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  organization_name:
    description:
      - The name of the organization you wish to add the protectable object to.
    required: True
    type: str
  mssql_availability_group:
    description:
      - The name of the MSSQL Availability Group to add to the organization as a protectable object.
    required: True
    type: str
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 15

extends_documentation_fragment: rubrikinc.cdm.credentials
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_add_organization_protectable_object_sql_server_availability_group:
    organization_name: "Ansible"
    mssql_availability_group: "demo-ag"
'''


RETURN = '''
full_response:
    description:
      - The full API response for `POST /internal/role/{}/authorization`.
    returned: on success
    type: dict

idempotent_response:
    description: A "No changed required" message when the MSSQL host has already been added to the organization.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The MSSQL Availability Group `mssql_availability_group` is already assigned to the `organization_name` organization.
'''

from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule

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
        organization_name=dict(required=True, type='str'),
        mssql_availability_group=dict(required=True, type='str'),
        timeout=dict(required=False, type='int', default=15),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    organization_name = ansible["organization_name"]
    mssql_availability_group = ansible["mssql_availability_group"]
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
        api_request = rubrik.add_organization_protectable_object_sql_server_availability_group(organization_name, mssql_availability_group, timeout)
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
