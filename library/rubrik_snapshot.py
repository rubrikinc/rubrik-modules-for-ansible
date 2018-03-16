#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

HAS_DATEUTIL = True
try:
    from dateutil import parser, tz
except ImportError:
    HAS_DATEUTIL = False

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rubrik_snapshot
requirements: dateutil
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Take an On Demand Snapshot or initiate an Instant Recovery of a VM.
description:
    - Take an On Demand Snapshot of a vSphere VM and assign an SLA Domain or initiate an Instant Recovery of a VM.
author:
    - Drew Russell (t. @drusse11)
options:
    sla_domain_name:
        description:
            - Then name of the SLA Domain to assign to Snapshot. Required if I(action=on_demand_snapshot).
        required: false
        aliases: sla
        default: null
    vsphere_vm_name:
        description:
            - The name of the VM to take a Snapshot of.
        required: true
        aliases: vm
        default: null
    snapshot_date:
        description:
            - The date the Snapshot was taken that you wish to initiate the Instant Recovery on.  Required if I(action=instant_recovery).
        required: False
        default: null
    snapshot_date:
        description:
            - The date the Snapshot was taken that you wish to initiate the Instant Recovery on. Format should be MM-DD-YYYY (01-26-2018).  Required if I(action=instant_recovery).
        required: False
        default: null
    action:
        description:
            - Whether to take an OnDemand Snapshot or initiate a Instant Recovery
        choices: ['on_demand_snapshot', 'instant_recovery']
        required: False
        default: null

'''

EXAMPLES = '''
- name: Take a On Demand vSphere VM Snapshot
  rubrik_snapshot:
    provider={{ credentials }}
    sla_domain_name={{ sla_domain_name }}
    vsphere_vm_name={{ vsphere_vm_name }}

- name: Instantly Recovery a vSphere VM
  rubrik_snapshot:
    provider={{ credentials }}
    vsphere_vm_name={{ vsphere_vm_name }}
    snapshot_date={{ snapshot_date }}
    snapshot_time={{ snapshot_time }}
    action=instant_recovery
'''

RETURN = '''
response:
    description: Human readable description of the results of the module execution.
    returned: success
    type: dict
    sample: {"response": "Successfully created a On Demand Snapshot for 'Ansible-Tower'}
'''


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


def convert_timezone(utc_time, cluster_timezone):

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(cluster_timezone)

    time_in_utz = parser.parse(utc_time)

    converted_date_time = time_in_utz.replace(tzinfo=to_zone)
    converted_date = converted_date_time.date().strftime('%m-%d-%Y')
    converted_time = converted_date_time.time().strftime("%I:%M %p")

    # # Remove a leading 0 if it is present in the time
    if converted_time[:1] == "0":
        converted_time = converted_time[1:]

    return converted_date, converted_time


def get_vm_snapshot_id(module, vm_id, snapshot_date, snapshot_time):

    snapshot_data = {}
    snapshot_present = False

    # Get the Current Cluster Timezone
    api_version = 'internal' #v1 or internal
    endpoint = '/cluster/me/timezone'

    response_body = rubrik_get(module, api_version, endpoint)

    cluster_timezone = response_body['timezone']

    #Get VMs
    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm/{}'.format(vm_id)

    response_body = rubrik_get(module, api_version, endpoint)

    snapshots = response_body['snapshots']

    for snapshot in snapshots:
        # Convert the Snapshot Data to a Dictionary for processing
        snapshot_id = snapshot['id']

        # Convert the Datetime UTC data into the current Cluster Timezone
        snapshot_date, snapshot_time = convert_timezone(snapshot['date'], cluster_timezone)

        # Populate the snapshot_data dictionary with a "id: [date, time]" format
        snapshot_data.setdefault(snapshot_id, [])
        snapshot_data[snapshot_id].append(snapshot_date)
        snapshot_data[snapshot_id].append(snapshot_time)

        for snapshot_id, snapshot_datetime in snapshot_data.items():
            if snapshot_datetime[0] == snapshot_date and snapshot_datetime[1] == snapshot_time:
                vm_snapshot_id = snapshot_id
                snapshot_present = True
                break

        if snapshot_present == False:
            module.fail_json(
                msg=("No Snapshot found that was taken on {} at {} on the VM.".format(snapshot_date, snapshot_time)))

    return vm_snapshot_id


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

    response_body = rubrik_post(module, api_version, endpoint, data)

    results['changed'] = True
    results['response_body'] = response_body
    results['status'] = response_body['links'][0]['href']

    return results


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            sla_domain_name=dict(required=False, aliases=['sla']),
            vsphere_vm_name=dict(required=True, aliases=['vm']),
            snapshot_date=dict(required=False, aliases=['date']),
            snapshot_time=dict(required=False, aliases=['time']),
            action=dict(required=True, choices=['on_demand_snapshot', 'instant_recovery', 'live_mount']),
            restore_host=dict(required=True, aliases=['host']),
            disable_network=dict(required=False, default=False, type='bool'),
            remove_network_devices=dict(required=False, default=False, type='bool'),
            power_on=dict(required=False, default=True, type='bool'),
            keep_mac_addresses=dict(required=False, default=False, type='bool'),

        )
    )

    required_if = [
        ('action', 'on_demand_snapshot', ['sla_domain_name', 'vsphere_vm_name']),
        ('action', 'instant_recovery', ['snapshot_date', 'snapshot_time', 'vsphere_vm_name']),
        ('action', 'live_mount', ['snapshot_date', 'snapshot_time', 'vsphere_vm_name', 'restore_host',
                                  'disable_network', 'remove_network_devices', 'power_on', 'keep_mac_addresses'])
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
    results['vm'] = vm_id

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
        results['status'] = "Successfully created a On Demand Snapshot for '{}'.".format(vsphere_vm_name)

    if action == "instant_recovery":

        if HAS_DATEUTIL == False:
            module.fail_json(
                msg='Missing the required dateutil Python Module. Please install (pip install python-dateutil).')

        snapshot_date = ansible['snapshot_date']
        snapshot_time = ansible['snapshot_time']

        vm_snapshot_id = get_vm_snapshot_id(module, vm_id, snapshot_date, snapshot_time)

        instant_recovery_data_model = {}
        instant_recovery_data_model['removeNetworkDevices'] = False
        instant_recovery_data_model['preserveMoid'] = False

        api_version = 'v1' #v1 or internal
        endpoint = '/vmware/vm/snapshot/{}/instant_recover'.format(vm_snapshot_id)

        response_body = rubrik_post(module, api_version, endpoint, instant_recovery_data_model)

        results['response_body'] = response_body
        results['status'] = "Successfully initiated a Instant Restore for the {} Snapshot taken on {} at {}.".format(
            vsphere_vm_name, snapshot_date, snapshot_time)

    if action == "live_mount":

        if HAS_DATEUTIL == False:
            module.fail_json(
                msg='Missing the required dateutil Python Module. Please install (pip install python-dateutil).')

        snapshot_date = ansible['snapshot_date']
        snapshot_time = ansible['snapshot_time']

        host_id = get_host_id(module)
        vm_snapshot_id = get_vm_snapshot_id(module, vm_id, snapshot_date, snapshot_time)

        results = live_mount(module, vm_snapshot_id, host_id)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
