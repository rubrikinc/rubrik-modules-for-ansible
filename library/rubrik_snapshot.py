#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from dateutil import parser, tz
    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def get_vsphere_vm_id(module, vsphere_vm_name):

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(vsphere_vm_name)

    response_body = rubrik_get(module, api_version, endpoint)

    # Check if any results are returned
    if not response_body['data']:
        module.fail_json(
            msg=("There is no vSphere VM named {} on the Rubrik Cluster.".format(vsphere_vm_name)))
    else:
        for vm in response_body['data']:
            if vm['name'] == vsphere_vm_name:
                vm_id = vm['id']

    try:
        vm_id
    except NameError:
        module.fail_json(
            msg=("There is no vSphere VM named {} on the Rubrik Cluster.".format(vsphere_vm_name)))

    return vm_id


def get_sla_domain_id(module, sla_domain_name):

    api_version = 'v1' #v1 or internal
    endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(sla_domain_name)

    response_body = rubrik_get(module, api_version, endpoint)

    # Check if any results are returned
    if not response_body['data']:
        module.fail_json(msg=("There is no SLA Domain named {} on the Rubrik Cluster.".format(sla_domain_name)))
    else:
        for sla_domain in response_body['data']:
            if sla_domain['name'] == sla_domain_name:
                sla_id = sla_domain['id']

    return sla_id


def get_vm_snapshot_id(module, vm_id):

    #Get VMs
    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm/{}/snapshot'.format(vm_id)

    response_body = rubrik_get(module, api_version, endpoint)

    snapshot_id = response_body['data'][0]['id']

    return snapshot_id


def live_mount(module, snapshot_id):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params
    results = {}

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm/snapshot/{}/mount'.format(snapshot_id)

    data = {}
    data['disableNetwork'] = ansible['disable_network']
    data['removeNetworkDevices'] = ansible['remove_network_devices']
    data['powerOn'] = ansible['power_on']
    data['keepMacAddresses'] = ansible['keep_mac_addresses']
    response_body = rubrik_post(module, api_version, endpoint, data)

    return response_body


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            sla_domain_name=dict(required=False, aliases=['sla']),
            vsphere_vm_name=dict(required=True, aliases=['vm']),
            action=dict(required=True, choices=['on_demand_snapshot', 'instant_recovery', 'live_mount']),
            restore_host=dict(required=False, aliases=['host']),
            disable_network=dict(required=False, default=False, type='bool'),
            remove_network_devices=dict(required=False, default=False, type='bool'),
            power_on=dict(required=False, default=True, type='bool'),
            keep_mac_addresses=dict(required=False, default=False, type='bool'),

        )
    )

    required_if = [
        ('action', 'on_demand_snapshot', ['sla_domain_name', 'vsphere_vm_name']),
        ('action', 'instant_recovery', ['vsphere_vm_name']),
        ('action', 'live_mount', ['vsphere_vm_name', 'disable_network',
                                  'remove_network_devices', 'power_on', 'keep_mac_addresses'])
    ]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=required_if,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    node = ansible['node']
    username = ansible['username']
    password = ansible['password']
    action = ansible['action']
    vsphere_vm_name = ansible['vsphere_vm_name']

    vm_id = get_vsphere_vm_id(module, vsphere_vm_name)

    if action == "on_demand_snapshot":

        sla_domain_name = ansible['sla_domain_name']

        sla_id = get_sla_domain_id(module, sla_domain_name)

        create_on_demand_snapshot_data_model = {}
        create_on_demand_snapshot_data_model['slaId'] = sla_id

        api_version = 'v1' #v1 or internal
        endpoint = '/vmware/vm/{}/snapshot'.format(vm_id)

        response_body = rubrik_post(module, api_version, endpoint, create_on_demand_snapshot_data_model)

        results['changed'] = True
        results['response_body'] = response_body
        results['job_status_link'] = response_body['links'][0]['href']

    if action == "instant_recovery":

        if HAS_DATEUTIL == False:
            module.fail_json(
                msg='Missing the required dateutil Python Module. Please install (pip install python-dateutil).')

        vm_snapshot_id = get_vm_snapshot_id(module, vm_id)

        instant_recovery_data_model = {}
        instant_recovery_data_model['removeNetworkDevices'] = False
        instant_recovery_data_model['preserveMoid'] = False

        api_version = 'v1' #v1 or internal
        endpoint = '/vmware/vm/snapshot/{}/instant_recover'.format(vm_snapshot_id)

        response_body = rubrik_post(module, api_version, endpoint, instant_recovery_data_model)

        results['changed'] = True
        results['response_body'] = response_body
        results['job_status_link'] = response_body['links'][0]['href']

    if action == "live_mount":

        if HAS_DATEUTIL == False:
            module.fail_json(
                msg='Missing the required dateutil Python Module. Please install (pip install python-dateutil).')

        vm_snapshot_id = get_vm_snapshot_id(module, vm_id)

        response_body = live_mount(module, vm_snapshot_id)

        results['changed'] = True
        results['response_body'] = response_body
        results['job_status_link'] = response_body['links'][0]['href']

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
