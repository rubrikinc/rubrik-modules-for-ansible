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
module: rubrik_on_demand_snapshot
requirements: pyRubrik
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Take an On Demand Snapshot.
description:
    - Take an On Demand Snapshot of a vSphere VM and assign an SLA Domain.
author:
    - Drew Russell (t. @drusse11)
options:
    sla_domain_name:
        description:
            - Then name of the SLA Domain to assign to Snapshot.
        required: true
        aliases: sla
        default: null
    vsphere_vm_name:
        description:
            - The name of the VM to take a Snapshot of.
        required: true
        aliases: vm
        default: null

'''

EXAMPLES = '''
- name: Take a On Demand vSphere VM Snapshot
  rubrik_on_demand_snapshot:
    provider={{ credentials }}
    sla_domain_name={{ sla_domain_name }}
    vsphere_vm_name={{ vsphere_vm_name }}
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

    query_sla_domain = rubrik.query_sla_domain(
        primary_cluster_id='local', name=name, is_relic=False)

    # Check if any results are returned
    if not query_sla_domain.data:
        module.fail_json(
            msg=("There is no SLA Domain named {} on the Rubrik Cluster.".format(name)))
    else:
        for sla_domain in query_sla_domain.data:
            if sla_domain.name == name:
                sla_id = sla_domain.id

    return sla_id


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            sla_domain_name=dict(required=True, aliases=['sla']),
            vsphere_vm_name=dict(required=True, aliases=['vm']),

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
    sla_domain_name = ansible['sla_domain_name']
    vsphere_vm_name = ansible['vsphere_vm_name']

    rubrik = connect_to_cluster(node, username, password, module)

    vm_id = get_vsphere_vm_id(rubrik, vsphere_vm_name, module)
    sla_id = get_sla_domain_id(rubrik, sla_domain_name, module)

    create_on_demand_snapshot_data_model = {
        "slaId": sla_id
    }

    rubrik.create_on_demand_backup(
        vm_id, config=create_on_demand_snapshot_data_model)

    results['response'] = "Successfully created a On Demand Snapshot for '{}'.".format(
        vsphere_vm_name)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
