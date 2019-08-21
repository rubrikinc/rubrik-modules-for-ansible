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
module: rubrik_configure_ntp
short_description: Configure connection information for the NTP servers used by the Rubrik cluster for time synchronization.
description:
    - Configure connection information for the NTP servers used by the Rubrik cluster for time synchronization.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  ntp_server:
    description:
      - A list of the NTP server(s) you wish to configure the Rubrik cluster to use.
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
- rubrik_configure_ntp:
    ntp_server: ["192.168.10.121", "192.168.10.122"]
'''


RETURN = '''
response:
    description: A 204 status code success message.
    returned: on success
    type: dict

response:
    description: A "No changed required" message when the cluster is already configured with the provided I(ntp_servers).
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The NTP server(s) I(ntp_server) has already been added to the Rubrik cluster.
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
        ntp_servers=dict(required=True, type='list'),
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
        api_request = rubrik.configure_ntp(ansible["ntp_servers"], ansible["timeout"])
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
