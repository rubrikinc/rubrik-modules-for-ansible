#!/usr/bin/python
# (c) 2020 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_refresh_ahv
short_description: Refresh the metadata for the specified AHV cluster
description:
    - Refresh the metadata for the specified AHV cluster
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  nutanix_ahv_cluster:
    description:
      - The name of the AHV cluster you wish to refresh metadata from
    required: True
    type: str
  wait_for_completion:
    description:
      - Flag that determines if the method should wait for the job to complete before exiting.
    required: False
    type: bool
    default: True
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
- name: Refresh the metadata for the specified AHV cluster
  rubrik_refresh_ahv:
    nutanix_ahv_cluster: ahvcluster
    wait_for_completion: true
'''

RETURN = '''
full_response:
    description: The full API response for the API call.
    returned: on success
    type: dict
    sample:
      {
        "endTime": "2020-04-07T00:30:28.448Z",
        "id": "REFRESH_METADATA_01234567-8910-1abc-d435-0abc1234d567_01234567-8910-1abc-d435-0abc1234d567:::0",
        "links": [
            {
                "href": "https://rubrik/api/internal/nutanix/cluster/request/REFRESH_NUTANIX_CLUSTER_01234567:::0",
                "rel": "self"
            }
        ],
        "nodeId": "cluster:::RVM111S000000",
        "startTime": "2020-04-07T00:29:50.585Z",
        "status": "SUCCEEDED"
      }
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
        nutanix_ahv_cluster=dict(required=True, type='str'),
        wait_for_completion=dict(required=False, type='bool', default=True),
        timeout=dict(required=False, type='int', default=15)
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
        api_request = rubrik.refresh_ahv(ansible["nutanix_ahv_cluster"], ansible["wait_for_completion"], ansible["timeout"])
    except Exception as error:
        module.fail_json(msg=str(error))

    results["changed"] = False

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
