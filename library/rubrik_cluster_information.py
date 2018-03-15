#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rubrik_cluster_information
requirements: pyRubrik
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Retrieve public information about the Rubrik Cluster.
description:
    - Retrieve the Rubrik Cluster Version, ID, and API Version
author:
    - Drew Russell (t. @drusse11)
'''

EXAMPLES = '''
- name: Retrieve public information about the Rubrik cluster
  rubrik_cluster_information:
    provider={{ credentials }}
'''

RETURN = '''
version:
    description: Software version running on the Rubrik Cluster
    returned: always
    type: dict
    sample: {"version": "4.0.4-568",}
id:
    description:
        - ID of the Rubrik Cluster
    returned: always
    type: dict
    sample: {"id": "89qc0e87-6f2c-4652-a2fa-3797baOe6229",}
api_version:
    description: API version of the Rubrik cluster
    returned: always
    type: dict
    sample: {"version": "1"}

'''


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


from ansible.module_utils.basic import AnsibleModule, jsonify # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
