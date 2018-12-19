#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
# Should be auto-generated and pasted here.
'''

EXAMPLES = '''
- rubrik_module_name:
'''

RETURN = '''
response:
    description: The full API response for .
    returned: on success
    type: dict
    sample:
      {

    }

response:
    description: A "No changed required" message when
    returned: When the module idempotent check is succesful.
    type: str
    sample:
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrik_cdm import load_provider_variables, rubrik_argument_spec

try:
    import rubrik_cdm
    sdk_present = True
except BaseException:
    sdk_present = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = rubrik_argument_spece

    # Start Parameters
    argument_spec.update(
        dict(
            timeout=dict(required=False, type='int', default=15),

        )
    )
    # End Parameters

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False)

    if sdk_present is False:
        module.fail_json(
            msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    load_provider_variables(module)
    ansible = module.params

    try:
        rubrik = rubrik_cdm.Connect()
    except SystemExit as error:
        if "has not been provided" in str(error):
            try:
                ansible["node_ip"]
                ansible["username"]
                ansible["password"]
            except KeyError:
                module.fail_json(
                    msg="Error: The Rubrik login credentials are missing. Verify the correct env vars are present or provide them through the provider param.")
        else:
            module.fail_json(msg=str(error))

        try:
            rubrik = rubrik_cdm.Connect(
                ansible['node_ip'],
                ansible['username'],
                ansible['password'])
        except SystemExit as error:
            module.fail_json(msg=str(error))

    ##################################
    ######### Code Block #############
    ##################################
    ##################################

    try:
        api_request = rubrik.
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
