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
from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec

try:
    import rubrik_cdm
    HAS_RUBRIK_SDK = True
except ImportError:
    HAS_RUBRIK_SDK = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            cluster_name=dict(required=False, type='str'),
            admin_email=dict(required=False, type='str'),
            admin_password=dict(required=False, type='str', no_log=True),
            management_gateway=dict(required=False, type='str'),
            management_subnet_mask=dict(required=False, type='str'),
            node_config=dict(required=True, type='dict'),
            enable_encryption=dict(required=False, type='bool', default=True),
            dns_search_domains=dict(required=False, type='list', default=[]),
            dns_nameservers=dict(required=False, type='list', default=['8.8.8.8']),
            ntp_servers=dict(required=False, type='list', default=['pool.ntp.org']),
            wait_for_completion=dict(required=False, type='bool', default=True),
            timeout=dict(required=False, type='int', default=30),
        )
    )
    # End Parameters

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    try:
        node_ip, username, password = credentials(module)
    except ValueError:
        module.fail_json(msg="The Rubrik login credentials are missing. Verify the correct env vars are present or provide them through the `provider` param.")

     try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password)
    except SystemExit as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.setup_cluster(ansible["cluster_name"], ansible["admin_email"], ansible["admin_password"], ansible["management_gateway"], ansible["management_subnet_mask"],
                                           ansible["node_config"], ansible["enable_encryption"], ansible["dns_search_domains"], ansible["dns_nameservers"], ansible["ntp_servers"], ansible["wait_for_completion"], ansible["timeout"])
    except SystemExit as error:
        module.fail_json(msg=str(error))

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
