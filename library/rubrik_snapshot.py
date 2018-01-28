#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytz

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rubrik_snapshot
requirements: pyRubrik, pytz
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
  rubrik_on_demand_snapshot:
    provider={{ credentials }}
    sla_domain_name={{ sla_domain_name }}
    vsphere_vm_name={{ vsphere_vm_name }}

- name: Instantly Recovery a vSphere VM
  rubrik_on_demand_snapshot:
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


def get_vsphere_vm_id(rubrik, vsphere_vm_name, module):

    name = vsphere_vm_name

    query_vm = rubrik.query_vm(
        primary_cluster_id='local', name=name, is_relic=False)

    # Check if any results are returned
    if not query_vm.data:
        module.fail_json(
            msg=("There is no vSphere VM named {} on the Rubrik Cluster.".format(name)))
    else:
        for vm in query_vm.data:
            if vm.name == name:
                vm_id = vm.id

    return vm_id


def get_sla_domain_id(rubrik,  sla_domain_name, module):

    name = sla_domain_name

    query_sla_domain = rubrik.query_sla_domain(primary_cluster_id='local', name=name, is_relic=False)

    # Check if any results are returned
    if not query_sla_domain.data:
        module.fail_json(msg=("There is no SLA Domain named {} on the Rubrik Cluster.".format(name)))
    else:
        for sla_domain in query_sla_domain.data:
            if sla_domain.name == name:
                sla_id = sla_domain.id

    return sla_id


def convert_timezone(utc_time, cluster_timezone):

    # Snapshot Datetime data in UTC
    datetime_in_utc = utc_time

    # Define the configured Cluster Timezone
    current_cluster_timezone = pytz.timezone(cluster_timezone)

    # Update the Datatime object with the configured Cluster Timezone
    converted_date_time = datetime_in_utc.astimezone(current_cluster_timezone)

    # Pull the Data and Time values from the Datatime object to preserve formating
    converted_date = converted_date_time.date().strftime('%m-%d-%Y')
    converted_time = converted_date_time.time().strftime("%I:%M %p")

    # Remove a leading 0 if it is present in the time
    if converted_time[:1] == "0":
        converted_time = converted_time[1:]

    return converted_date, converted_time


def get_vm_snapshot_id(rubrik, vm_id, snapshot_date, snapshot_time, module):

    snapshot_data = {}
    snapshot_present = False

    cluster_timezone = rubrik.get_cluster_timezone().__dict__['timezone']

    get_vm = rubrik.get_vm(vm_id).__dict__

    # Pull the Snapshot related values from the get_vm call
    for key, value in get_vm.items():
        if key == "snapshots":
            snapshots = value

    for data in snapshots:
        # Convert the Snapshot Data to a Dictionary for processing
        snapshot = data.__dict__

        snapshot_id = snapshot['id']
        # Convert the Datetime UTC data into the current Cluster Timezone
        snapshot_date, snapshot_time = convert_timezone(snapshot['date_property'], cluster_timezone)

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


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            sla_domain_name=dict(required=False, aliases=['sla']),
            vsphere_vm_name=dict(required=True, aliases=['vm']),
            snapshot_date=dict(required=False, aliases=['date']),
            snapshot_time=dict(required=False, aliases=['time']),
            action=dict(required=True, choices=['on_demand_snapshot', 'instant_recovery']),

        )
    )

    required_if = [
        ('action', 'on_demand_snapshot', ['sla_domain_name', 'vsphere_vm_name']),
        ('action', 'instant_recovery', ['snapshot_date', 'snapshot_time', 'vsphere_vm_name'])
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

    rubrik = connect_to_cluster(node, username, password, module)

    vm_id = get_vsphere_vm_id(rubrik, vsphere_vm_name, module)

    if action == "on_demand_snapshot":

        sla_domain_name = ansible['sla_domain_name']

        sla_id = get_sla_domain_id(rubrik, sla_domain_name, module)

        create_on_demand_snapshot_data_model = {
            "slaId": sla_id
        }

        rubrik.create_on_demand_backup(vm_id, config=create_on_demand_snapshot_data_model)

        results['response'] = "Successfully created a On Demand Snapshot for '{}'.".format(vsphere_vm_name)

    if action == "instant_recovery":

        snapshot_date = ansible['snapshot_date']
        snapshot_time = ansible['snapshot_time']

        vm_snapshot_id = get_vm_snapshot_id(rubrik, vm_id, snapshot_date, snapshot_time, module)

        instant_recovery_data_model = {
            "removeNetworkDevices": False,
            "preserveMoid": False
        }

        rubrik.create_instant_recovery(vm_snapshot_id, config=instant_recovery_data_model)

        results['response'] = "Successfully initiated a Instant Restore for the {} Snapshot taken on {} at {}.".format(
            vsphere_vm_name, snapshot_date, snapshot_time)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
