#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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

    argument_spec.update(
        dict(
            object_name=dict(required=True, type='str'),
            object_type=dict(required=False, default="vmware"),
            sla_name=dict(required=False, type='str', default='current'),
            fileset=dict(required=False, type='str', default='None'),
            host_os=dict(required=False, type='str', default='None'),
        )
    )

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
        module.fail_json(msg=error)

    results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
