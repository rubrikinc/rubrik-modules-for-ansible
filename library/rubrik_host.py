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
module: rubrik_host
requirements: pyRubrik
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Manage a Physical Host.
description:
    - Add or Delete a Physical Host from Rubrik Cluster.
author:
    - Drew Russell (t. @drusse11)
options:
    hostname:
        description:
            - The DNS hostname or IP address of the Physical Host you wish to take an I(action) on.
        required: true
        aliases: ip_address
        default: null
    action:
        description:
            - Whether to add or delete the Physical Host.
        required: true
        choices: [add, delete]
        default: add
'''

EXAMPLES = '''
- name: Add a Physical Host to the Rubrik Cluster
  rubrik_host:
    provider={{ credentials }}
    hostname={{ hostname }}
    action=add

- name: Delete a Physical Host from the Rubrik Cluster
  rubrik_host:
    provider={{ credentials }}
    hostname={{ hostname }}
    action=delete
'''

RETURN = '''
response:
    description: Human readable description of the results of the module execution.
    returned: success
    type: dict
    sample: {"response": "'Linux-Physical' has successfully added to the Rubrik Cluster.}
'''


def current_hosts(module, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_get(module, api_version, endpoint)

    host_present = False

    for host in response_body['data']:
        if host['hostname'] == hostname:
            host_present = True
            break

    return host_present


def add_host(module, hostname):

    add_host_data_model = {}
    add_host_data_model['hostname'] = hostname
    add_host_data_model['hasAgent'] = True

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_post(module, api_version, endpoint, add_host_data_model)

    return response_body


def delete_host(module, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_get(module, api_version, endpoint)

    for host in response_body['data']:
        if host['hostname'] == hostname:
            host_id = host['id']
            break

    endpoint = '/host/{}'.format(host_id)

    rubrik_delete(module, api_version, endpoint)


def get_host_id(module, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_get(module, api_version, endpoint)

    for host in response_body['data']:
        if host['hostname'] == hostname:
            host_id = host['id']
            break

    return host_id


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            action=dict(required=True, choices=['add', 'delete']),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    node = ansible['node']
    username = ansible['username']
    password = ansible['password']
    hostname = ansible['hostname']
    action = ansible['action']

    host_present = current_hosts(module, hostname)

    # Add a new host to the Rubrik Cluster
    if host_present is False and action == 'add':
        response_body = add_host(module, hostname)
        results['changed'] = True
        results['response'] = response_body
    elif host_present is True and action == 'add':
        results['changed'] = False
        results['response'] = "The host '{}' is already connected to the Rubrik Cluster.".format(
            hostname)
    elif host_present is True and action == 'delete':
        delete_host(module, hostname)
        results['changed'] = True
        results['response'] = "The host '{}' has successfully been deleted from the Rubrik Cluster.".format(
            hostname)
    elif host_present is False and action == 'delete':
        results['changed'] = False
        results['response'] = "The host '{}' is not present on the Rubrik Cluster.".format(
            hostname)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post, rubrik_delete  # isort:skip


if __name__ == "__main__":
    main()
