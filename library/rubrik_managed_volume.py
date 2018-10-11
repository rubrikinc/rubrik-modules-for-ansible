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
from ansible.module_utils.rubrikcdm import HAS_RUBRIKCDM, load_provider_variables, rubrik_argument_spec

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

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if HAS_RUBRIKCDM is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    results = {}

    load_provider_variables(module)
    ansible = module.params

    rubrik = rubrik_cdm.Connect(ansible['node'], ansible['username'], ansible['password'])

    if ansible["action"] == "begin":
        api_request = rubrik.begin_managed_volume_snapshot(ansible["managed_volume_name"], ansible["timeout"])

        if "No change required" in api_request:
            results["changed"] = False
        else:
            results["changed"] = True
        results["response"] = api_request

    else:
        api_request = rubrik.end_managed_volume_snapshot(
            ansible["managed_volume_name"], ansible["sla_name"], ansible["timeout"])

        if "No change required" in api_request:
            results["changed"] = False
        else:
            results["changed"] = True
        results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
