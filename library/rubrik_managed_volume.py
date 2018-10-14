#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

EXAMPLES = '''
# Begin a new managed volume snapshot.
- rubrik_managed_volume:
    provider: "{{ credentials }}"
    name: MV1
    action: begin

# End the managed volume snapshot
- rubrik_managed_volume:
    provider: "{{ credentials }}"
    name: MV1
    action: end
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, connect, load_provider_variables, rubrik_argument_spec

import rubrik_cdm


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            managed_volume_name=dict(required=True, aliases=['name']),
            sla_name=dict(required=False, type='str', default="current"),
            action=dict(required=True, choices=['begin', 'end']),
            timeout=dict(required=False, type='int', default=15),
        )
    )

    required_if = [
        ('action', 'end', ['sla_name'])
    ]

    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=False)

    sdk_present, rubrik_cdm = sdk_validation()

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    results = {}

    load_provider_variables(module)
    ansible = module.params

    rubrik = connect(rubrik_cdm, module)
    if isinstance(rubrik, str):
        module.fail_json(msg=rubrik)

    if ansible["action"] == "begin":
        try:
            api_request = rubrik.begin_managed_volume_snapshot(ansible["managed_volume_name"], ansible["timeout"])
        except SystemExit as error:
            module.fail_json(msg=str(error))

    else:
        try:
            api_request = rubrik.end_managed_volume_snapshot(
                ansible["managed_volume_name"], ansible["sla_name"], ansible["timeout"])

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
