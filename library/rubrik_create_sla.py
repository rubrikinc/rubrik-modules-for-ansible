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
module: rubrik_create_sla
short_description: Create a new SLA Domain.
description:
    - Create a new SLA Domain.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  name:
    description:
      - The name of the new SLA Domain.
    required: true
    type: str
  hourly_frequency:
    description:
      - Hourly frequency to take backups.
    required: false
    type: int
  hourly_retention:
    description:
      - Number of hours to retain the hourly backups.
    required: false
    type: int
  daily_frequency:
    description:
      - Daily frequency to take backups.
    required: false
    type: int
  daily_retention:
    description:
      - Number of hours to retain the daily backups.
    required: false
    type: int
  monthly_frequency:
    description:
      - Monthly frequency to take backups.
    required: false
    type: int
  monthly_retention:
    description:
      - Number of hours to retain the monthly backups.
    required: false
    type: int
  yearly_frequency:
    description:
      - Yearly frequency to take backups.
    required: false
    type: int
  yearly_retention:
    description:
      - Number of hours to retain the yearly backups.
    required: false
    type: int
  archive_name:
    description:
      - The optional archive location you wish to configure on the SLA Domain. When populated, you must also provide a I(retention_on_brik_in_days).
    required: false
    default: None
    type: int
  retention_on_brik_in_days:
    description:
      - The number of days you wish to keep the backups on the Rubrik cluster. When populated, you must also provide a I(archive_name).
    required: false
    default: None
    type: int
  instant_archive:
    description:
      - Flag that determines whether or not to enable instant archive. Set to true to enable.
    required: false
    default: False
    type: bool
  timeout:
    description:
    - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    default: 15
    type: int

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_create_sla:
    name: Ansible-SLA
    hourly_frequency: 1
    hourly_retention: 24
    daily_frequency: 1
    daily_retention: 30
    monthly_frequency: 1
    monthly_retention: 12
    yearly_frequency: 1
    yearly_retention: 5
    archive_name: AWS-S3-Bucket
    retention_on_brik_in_days: 30
    instant_archive: True
'''

RETURN = '''
response:
    description: The full API response for POST /v1/sla_domain.
    returned: on success when connected to a CDM v4.x or lower cluster
    type: dict

response:
    description: The full API response for POST /v2/sla_domain.
    returned: on success when connected to a CDM v5.0 or greater cluster
    type: dict

response:
    description: A "No changed required" message when the Rubrik SLA is already present on the cluster.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The 'name' SLA Domain is already configured with the provided configuration.
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
        name=dict(required=True, type='str'),
        hourly_frequency=dict(required=False, default=None, type='int'),
        hourly_retention=dict(required=False, default=None, type='int'),
        daily_frequency=dict(required=False, default=None, type='int'),
        daily_retention=dict(required=False, default=None, type='int'),
        monthly_frequency=dict(required=False, default=None, type='int'),
        monthly_retention=dict(required=False, default=None, type='int'),
        yearly_frequency=dict(required=False, default=None, type='int'),
        yearly_retention=dict(required=False, default=None, type='int'),
        archive_name=dict(required=False, default=None, type='str'),
        retention_on_brik_in_days=dict(required=False, default=None, type='int'),
        instant_archive=dict(required=False, default=False, type='bool'),
        timeout=dict(required=False, type='int', default=15),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    name = ansible["name"]
    hourly_frequency = ansible["hourly_frequency"]
    hourly_retention = ansible["hourly_retention"]
    daily_frequency = ansible["daily_frequency"]
    daily_retention = ansible["daily_retention"]
    monthly_frequency = ansible["monthly_frequency"]
    monthly_retention = ansible["monthly_retention"]
    yearly_frequency = ansible["yearly_frequency"]
    yearly_retention = ansible["yearly_retention"]
    archive_name = ansible["archive_name"]
    retention_on_brik_in_days = ansible["retention_on_brik_in_days"]
    instant_archive = ansible["instant_archive"]
    timeout = ansible["timeout"]

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.create_sla(
            name,
            hourly_frequency,
            hourly_retention,
            daily_frequency,
            daily_retention,
            monthly_frequency,
            monthly_retention,
            yearly_frequency,
            yearly_retention,
            archive_name,
            retention_on_brik_in_days,
            instant_archive,
            timeout)
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
