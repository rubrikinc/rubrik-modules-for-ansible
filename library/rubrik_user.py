#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def get_username_id(module):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    api_version = 'internal' #v1 or internal
    endpoint = '/user?username={}'.format(ansible['end_user'])

    response_body = rubrik_get(module, api_version, endpoint)

    if not response_body:
        module.fail_json(msg='The Rubrik Cluster does not contain a End User Account named "{}"'.format(
            ansible['end_user']))
    else:
        username_id = response_body[0]['id']

    return username_id


def get_vm_id(module):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm?name={}'.format(ansible['vsphere_vm_name'])

    response_body = rubrik_get(module, api_version, endpoint)

    total_number_of_results = int(response_body['total'])

    if total_number_of_results == 0:
        module.fail_json(msg='The Rubrik Cluster does not contain a VM named "{}"'.format(
            ansible['vsphere_vm_name']))
    elif total_number_of_results == 1:
        vm_id = response_body['data'][0]['id']
    elif total_number_of_results > 1:
        for data in response_body['data']:
            if response_body['data'][0]['name'] == ansible['vsphere_vm_name']:
                vm_id = response_body['data'][0]['id']

    # If vm_id has not been assigned (aka the VM was not found) send a fail message
    if 'vm_id' not in locals():
        module.fail_json(msg='VM ID Not Assignd')
        # module.fail_json(msg='The Rubrik Cluster does not contain a VM named "{}"'.format(
        #     ansible['vsphere_vm_name']))

    return vm_id


def end_user_authorization(module, username_id, vm_id):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params
    results = {}

    api_version = 'internal' #v1 or internal
    endpoint = '/authorization/role/end_user'

    data = {}
    data['principals'] = [username_id]
    data['privileges'] = {"restore": [vm_id]}

    response_body = rubrik_post(module, api_version, endpoint, data)

    results['changed'] = True
    results['response_body'] = response_body['data']

    return results


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            vsphere_vm_name=dict(required=True, aliases=['vm']),
            end_user=dict(required=True),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    load_provider_variables(module)

    username_id = get_username_id(module)
    vm_id = get_vm_id(module)

    results = end_user_authorization(module, username_id, vm_id)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
