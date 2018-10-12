#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

EXAMPLES = '''
- rubrik_assign_physical_host_fileset:
    provider: "{{ credentials }}"
    hostname: 'phyton-physical-demo'
    fileset_name: 'Python SDK'
    sla_name: 'Gold'
    operating_system: 'Linux'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, connect, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            fileset_name=dict(required=True),
            sla_name=dict(required=True, aliases=['sla']),
            operating_system=dict(required=False, choices=['Linux', 'Windows']),
            include=dict(required=False, type='list', default=[]),
            exclude=dict(required=False, type='list', default=[]),
            exclude_exception=dict(required=False, type='list', default=[]),
            follow_network_shares=dict(required=False, type='bool', default=False),
            backup_hidden_folders=dict(required=False, type='bool', default=False),
            timeout=dict(required=False, type='int', default=30),

        )
    )

    required_together = [
        ["include", "exclude", "exclude_exception", "follow_network_shares", "backup_hidden_folders"]
    ]

    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, supports_check_mode=False)

    sdk_present, rubrik_cdm = sdk_validation()

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    results = {}

    load_provider_variables(module)
    ansible = module.params

    rubrik = connect(rubrik_cdm, module)
    if isinstance(rubrik, str):
        module.fail_json(msg=rubrik)

    # If there are multiple Filesets on the cluster with the same name the end use will need to provide more specific information. That only occurs when includes != None
    if bool(ansible['include']) is False:
        api_request = rubrik.assign_physical_host_fileset(
            ansible['hostname'], ansible['fileset_name'], ansible['operating_system'], ansible['sla_name'], timeout=ansible["timeout"])
    else:
        api_request = rubrik.assign_physical_host_fileset(ansible['hostname'], ansible['fileset_name'], ansible['operating_system'], ansible['sla_name'], ansible["include"],
                                                          ansible["exclude"], ansible["exclude_exception"], ansible["follow_network_shares"], ansible["backup_hidden_folders"], ansible["timeout"])

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
