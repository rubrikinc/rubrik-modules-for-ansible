#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

EXAMPLES = '''
- rubrik_physical_host:
    provider: "{{ credentials }}"
    hostname: 'ubuntu-physical-demo'
    action: 'add'

- rubrik_physical_host:
    provider: "{{ credentials }}"
    hostname: 'ubuntu-physical-demo'
    action: 'delete'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            action=dict(required=True, choices=['add', 'delete']),
            timeout=dict(required=False, type='int', default=120),

        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    sdk_present, rubrik_cdm = sdk_validation()

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    results = {}

    load_provider_variables(module)
    ansible = module.params

    rubrik = rubrik_cdm.Connect(ansible['node'], ansible['username'], ansible['password'])

    if ansible["action"] == "add":
        api_request = rubrik.add_physical_host(ansible["hostname"], ansible["timeout"])
    else:
        api_request = rubrik.delete_physical_host(ansible["hostname"], ansible["timeout"])

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
