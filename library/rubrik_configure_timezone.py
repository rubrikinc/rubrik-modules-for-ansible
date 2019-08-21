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
module: rubrik_configure_timezone
short_description: Configure the Rubrik cluster timezone.
description:
    - Configure the Rubrik cluster timezone.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  timezone:
    description:
      - The timezone you wish the Rubrik cluster to use.
    required: True
    choices: [America/Anchorage, America/Araguaina, America/Barbados, America/Chicago, America/Denver, America/Los_Angeles, America/Mexico_City, America/New_York, America/Noronha, America/Phoenix, America/Toronto, America/Vancouver, Asia/Bangkok, Asia/Dhaka, Asia/Dubai, Asia/Hong_Kong, Asia/Karachi, Asia/Kathmandu, Asia/Kolkata, Asia/Magadan, Asia/Singapore, Asia/Tokyo, Atlantic/Cape_Verde, Australia/Perth, Australia/Sydney, Europe/Amsterdam, Europe/Athens, Europe/London, Europe/Moscow, Pacific/Auckland, Pacific/Honolulu, Pacific/Midway, UTC]
    type: str
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
- rubrik_configure_timezone:
    timezone: America/Chicago
'''


RETURN = '''
response:
    description: The full API response for PATCH /v1/cluster/me
    returned: on success
    type: dict

response:
    description: A "No changed required" message when the timezone is already configured on the cluster.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The Rubrik cluster is already configured with I(timezone) as it's timezone.
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
        timezone=dict(required=True, type='str', choices=[
            'America/Anchorage',
            'America/Araguaina',
            'America/Barbados',
            'America/Chicago',
            'America/Denver',
            'America/Los_Angeles',
            'America/Mexico_City',
            'America/New_York',
            'America/Noronha',
            'America/Phoenix',
            'America/Toronto',
            'America/Vancouver',
            'Asia/Bangkok',
            'Asia/Dhaka',
            'Asia/Dubai',
            'Asia/Hong_Kong',
            'Asia/Karachi',
            'Asia/Kathmandu',
            'Asia/Kolkata',
            'Asia/Magadan',
            'Asia/Singapore',
            'Asia/Tokyo',
            'Atlantic/Cape_Verde',
            'Australia/Perth',
            'Australia/Sydney',
            'Europe/Amsterdam',
            'Europe/Athens',
            'Europe/London',
            'Europe/Moscow',
            'Pacific/Auckland',
            'Pacific/Honolulu',
            'Pacific/Midway',
            'UTC']),
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
        api_request = rubrik.configure_timezone(ansible["timezone"], ansible["timeout"])
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
