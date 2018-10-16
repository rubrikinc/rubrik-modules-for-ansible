#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_on_demand_snapshot
short_description:
description:
    -
version_added: 2.7
author: Rubrik Ranger Team
options:

  object_name:
    description:
      - The name of the Rubrik object to take a on-demand snapshot of.
    required = True
    type = str

  object_type:
    description:
      - The Rubrik object type you want to backup.
    required = False
    type = str
    default = vmware
    choices = [vmware, physical_host]

  sla_name:
    description:
      - The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used.
    required = False
    type = str
    default = current

  fileset:
    description:
      - The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host.
    required = False
    type = str
    default = None

  host_os:
    description:
      - The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host.
    required = False
    type = str
    default = None
    choices = [None, Linux, Windows]


extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_on_demand_snapshot:
    object_name: 'ansible-node01'
    object_type: "vmware"
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
            object_type=dict(required=False, type='str', default="vmware", choices=["vmware", "physical_host"]),
            sla_name=dict(required=False, type='str', default='current'),
            fileset=dict(required=False, type='str', default='None'),
            host_os=dict(required=False, type='str', default='None', choices=["None", "Linux", "Windows"]),
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

    if ansible["fileset"] == "None":
        ansible["fileset"] = None

    if ansible["host_os"] == "None":
        ansible["host_os"] = None

    try:
        api_request = rubrik.on_demand_snapshot(
            ansible["object_name"], ansible["object_type"], ansible["sla_name"], ansible["fileset"], ansible["host_os"])

    except SystemExit as error:
        module.fail_json(msg=str(error))

    results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
