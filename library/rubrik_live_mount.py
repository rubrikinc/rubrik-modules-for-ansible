#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


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


def get_snapshot_id(module, vm_id):
    ''' '''

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm/{}/snapshot?sort_by=date'.format(vm_id)

    response_body = rubrik_get(module, api_version, endpoint)

    snapshot_id = response_body['data'][0]['id']

    return snapshot_id


def get_host_id(module):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/host'

    response_body = rubrik_get(module, api_version, endpoint)

    for data in response_body['data']:
        if data['name'] == ansible['restore_host']:
            host_id = data['id']

    return host_id


def live_mount(module, snapshot_id, host_id):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params
    results = {}

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm/snapshot/{}/mount'.format(snapshot_id)

    data = {}
    data['vmName'] = '{} Ansible'.format(ansible['vsphere_vm_name'])
    data['disableNetwork'] = ansible['disable_network']
    data['removeNetworkDevices'] = ansible['remove_network_devices']
    data['powerOn'] = ansible['power_on']
    data['keepMacAddresses'] = ansible['keep_mac_addresses']
    data['hostId'] = host_id

    response_body = rubrik_post(module, api_version, endpoint, jsonify(data))

    results['changed'] = True
    results['response_body'] = response_body
    results['status'] = response_body['links'][0]['href']

    return results


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            vsphere_vm_name=dict(required=True, aliases=['vm']),
            restore_host=dict(required=True, aliases=['host']),
            disable_network=dict(required=False, default=False, type='bool'),
            remove_network_devices=dict(required=False, default=False, type='bool'),
            power_on=dict(required=False, default=True, type='bool'),
            keep_mac_addresses=dict(required=False, default=False, type='bool'),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    load_provider_variables(module)

    vm_id = get_vm_id(module)
    host_id = get_host_id(module)
    snapshot_id = get_snapshot_id(module, vm_id)

    results = live_mount(module, snapshot_id, host_id)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule, jsonify # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
