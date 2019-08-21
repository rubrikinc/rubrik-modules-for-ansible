#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
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
module: rubrik_sql_live_mount
short_description: Live Mount a mssql database from a specified recovery point i.e. data and time.
description:
    - Live Mount a mssql database from a specified recovery point i.e. data and time.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  db_name:
    description:
      - The name of the database to Live Mount.
    required: True
    type: str
  date:
    description:
      - The recovery_point date you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014).
    required: True
    type: str
    default: None
  time:
    description:
      - The recovery_point time you wish to Live Mount formated as `Hour:Minute AM/PM` (ex: 1:30 AM).
    required: True
    type: str
    default: None
  sql_instance:
    description:
      - The SQL instance name with the database you wish to Live Mount.
    required: True
    type: str
    default: None
  sql_host:
    description:
      - The SQL Host of the database/instance to Live Mount.
    required: True
    type: str
    default: None
  mount_name:
    description:
      - The name given to the Live Mounted database i.e. AdventureWorks_Clone.
    required: True
    type: str
    default: None
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 30

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''


EXAMPLES = '''
- rubrik_sql_live_mount:
    db_name: 'AdventureWorks2016'
    date: '08-26-2018'
    time: '12:11 AM'
    sql_instance: 'MSSQLSERVER'
    sql_host: 'sql.rubrikdemo.com'
    mount_name: 'AdventureWorksClone'
'''


RETURN = '''
version:
    description: The full response of `POST /v1/mssql/db/{id}/mount`.
    returned: success
    type: dict
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
        db_name=dict(required=True, type='str'),
        date=dict(required=True, type='str'),
        time=dict(required=True, type='str'),
        sql_instance=dict(required=True, type='str', default=None),
        sql_host=dict(required=True, type='str', default=None),
        mount_name=dict(required=True, type='str', default=None),
        timeout=dict(required=False, type='int', default=30),

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
        api_request = rubrik.sql_live_mount(
            ansible["db_name"],
            ansible["date"],
            ansible["time"],
            ansible["sql_instance"],
            ansible["sql_host"],
            ansible["mount_name"],
            ansible["timeout"])
    except Exception as error:
        module.fail_json(msg=str(error))

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
