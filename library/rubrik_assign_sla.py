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
module: rubrik_assign_sla
short_description: Assign a Rubrik object to an SLA Domain.
description:
    - Assign a Rubrik object to an SLA Domain.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  object_name:
    description:
      - The name of the Rubrik object you wish to assign to an SLA Domain. When the I(object_type) is 'volume_group', the I(object_name) can be a list of volumes.
    required: true
    type: raw
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
    choices: [vmware, mssql_host, volume_group]
    type: str
  log_backup_frequency_in_seconds:
    description:
     - The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the I(object_type) is mssql_host.
    required: false
    default: None
    type: int
  log_retention_hours:
    description:
     - The MSSQL Log Retention frequency you'd like to specify with the SLA. Required when the I(object_type) is mssql_host.
    required: false
    default: None
    type: int
  copy_only:
    description:
     - Take Copy Only Backups with MSSQL. Required when the I(object_type) is mssql_host.
    required: false
    default: None
    type: bool
  windows_host:
    description:
      - The name of the Windows host that contains the relevant volume group. Required when the I(object_type) is volume_group.
    required: false
    default: None
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

- rubrik_assign_sla:
    object_name: "sql-host"
    object_type: "mssql_host"
    sla_name: "Gold"
    log_backup_frequency_in_seconds: 120
    log_retention_hours: 12
    copy_only: false

- rubrik_assign_sla:
    object_name: ["C:\\", "D:\\"]
    sla_name: "Gold"
    windows_host: "windows2016.rubrik.com"
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
        object_name=dict(required=True, type='raw'),
        sla_name=dict(required=True, type='str'),
        object_type=dict(
            required=False,
            type='str',
            default="vmware",
            choices=[
                'vmware',
                'mssql_host',
                'volume_group']),
        log_backup_frequency_in_seconds=dict(required=False, default=None, type='int'),
        log_retention_hours=dict(required=False, default=None, type='int'),
        copy_only=dict(required=False, default=None, type='bool'),
        windows_host=dict(required=False, default=None, type='str'),
        timeout=dict(required=False, type='int', default=30),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    object_name = ansible["object_name"]
    sla_name = ansible["sla_name"]
    object_type = ansible["object_type"]
    log_backup_frequency_in_seconds = ansible["log_backup_frequency_in_seconds"]
    log_retention_hours = ansible["log_retention_hours"]
    copy_only = ansible["copy_only"]
    windows_host = ansible["windows_host"]
    timeout = ansible["timeout"]

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    if object_type == "mssql_host":
        if log_backup_frequency_in_seconds is None or log_retention_hours is None or log_retention_hours is None:
            module.fail_json(
                msg="When the object_type is 'mssql_host', the 'log_backup_frequency_in_seconds', 'log_retention_hours', 'copy_only' paramaters must be populated.")

    if object_type == "volume_group":
        if windows_host is None:
            module.fail_json(msg="When the object_type is 'volume_group', 'windows_host' must also be populated.")

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.assign_sla(
            object_name,
            sla_name,
            object_type,
            log_backup_frequency_in_seconds,
            log_retention_hours,
            copy_only,
            windows_host,
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
