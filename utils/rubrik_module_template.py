#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

EXAMPLES = '''
- rubrik_module_name
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrikcdm import sdk_validation, connect, load_provider_variables, rubrik_argument_spec


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
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

    rubrik = connect(rubrik_cdm, module)
    if isinstance(rubrik, str):
        module.fail_json(msg=rubrik)

    ##################################
    ######### Code Block #############
    ##################################
    ##################################

    try:
        api_request = rubrik.
    except SystemExit as error:
        module.fail_json(msg=error)

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
