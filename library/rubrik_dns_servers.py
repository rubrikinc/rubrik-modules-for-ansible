#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_dns_servers
short_description: Configure the DNS Servers on the Rubrik cluster.
description:
    - Configure the DNS Servers on the Rubrik cluster.
version_added: 2.8
author: Rubrik Ranger Team
options:
  server_ip:
    description:
      - The DNS Server IPs you wish to add to the Rubrik cluster.
    required: True
    type: list
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
- rubrik_configure_dns_servers:
    server_ip: ["192.168.100.20", "192.168.100.21"]
'''


RETURN = '''
response:
    description: The full API response for POST /internal/cluster/me/dns_nameserver.
    returned: on success
    type: dict
  

response:
    description: A "No changed required" message when
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The Rubrik cluster is already configured with the provided DNS servers.
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

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            server_ip=dict(required=True, type='list'),
            timeout=dict(required=False, type='int', default=15),

        )
    )
    # End Parameters

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    try:
        node_ip, username, password = credentials(module)
    except ValueError:
        module.fail_json(msg="The Rubrik login credentials are missing. Verify the correct env vars are present or provide them through the `provider` param.")

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password)
    except SystemExit as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.configure_dns_servers(ansible["server_ip"], ansible["timeout"])
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
