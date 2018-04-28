#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    node = ansible['node']
    username = ansible['username']
    password = ansible['password']

    api_version = 'v1' #v1 or internal
    endpoint = '/cluster/me'

    response_body = rubrik_get(module, api_version, endpoint)

    results['version'] = response_body['version']
    results['id'] = response_body['id']
    results['api_version'] = response_body['apiVersion']

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get  # isort:skip


if __name__ == "__main__":
    main()
