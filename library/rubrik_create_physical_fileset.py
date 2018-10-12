#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

EXAMPLES = '''
- rubrik_create_physical_fileset:
    provider: "{{ credentials }}"
    name: 'AnsibleDemo'
    include: '/usr/local'
    operating_system: 'Linux'
    exclude: '/usr/local/temp,*.mp3,*.mp4,*mp5'
    exclude_exception: '/company*.mp4'
    follow_network_shares: False
    backup_hidden_folders: False
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            fileset_name=dict(required=False, aliases=['name']),
            operating_system=dict(required=False, choices=['Linux', 'Windows']),
            include=dict(required=False, type='list'),
            exclude=dict(required=False, type='list', default=[]),
            exclude_exception=dict(required=False, type='list', default=[]),
            follow_network_shares=dict(required=False, type='bool', default=False),
            backup_hidden_folders=dict(required=False, type='bool', default=False),
            timeout=dict(required=False, type='int', default=15),
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

    api_request = rubrik.create_physical_fileset(ansible["fileset_name"], ansible["operating_system"], ansible["include"], ansible["exclude"],
                                                 ansible["exclude_exception"], ansible["follow_network_shares"], ansible["backup_hidden_folders"], ansible["timeout"])

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
