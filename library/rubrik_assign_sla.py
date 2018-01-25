#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rubrik_assign_sla
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Assign an SLA to a vSphere VM.
description:
    - Assign an SLA to a vSphere VM.
author:
    - Drew Russell (t. @drusse11)
options:
    sla_domain_name:
        description:
            - Then name of the SLA Domain to assign to the VM.
        required: true
        aliases: sla
        default: null
    vsphere_vm_name:
        description:
            - The name of the VM that the SLA Domain should be assigned to.
        required: true
        aliases: vm
        default: null

'''

EXAMPLES = '''
- name: Assign a SLA Domain to a vSphere VM
  rubrik_assign_sla:
    provider={{ credentials }}
    sla_domain_name={{ sla_domain_name }}
    vsphere_vm_name={{ vsphere_vm_name }}
'''

RETURN = '''
response:
    description: Human readable description of the results of the module execution.
    returned: success
    type: dict
    sample: {"response": "Successfully configured the vSphere VM 'Ansible-Tower' with the 'Gold' SLA Domain."}
'''


def get_vsphere_vm_data(rubrik, vsphere_vm_name, module):

    name = vsphere_vm_name

    query_vm = rubrik.query_vm(
        primary_cluster_id='local', name=name, is_relic=False)

    # Check if any results are returned
    if not query_vm.data:
        module.fail_json(
            msg=("There is no vSphere VM named '{}' on the Rubrik Cluster.".format(name)))
    else:
        for vm in query_vm.data:
            if vm.name == name:
                vm_id = vm.id
                sla_domain_id = vm.effective_sla_domain_id
                break

    return vm_id, sla_domain_id


def get_sla_domain_id(rubrik, sla_domain_name, module):

    name = sla_domain_name

    query_sla_domain = rubrik.query_sla_domain(
        primary_cluster_id='local', name=name, is_relic=False)

    # Check if any results are returned
    if not query_sla_domain.data:
        module.fail_json(
            msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(name)))
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

    vm_id, current_sla_id = get_vsphere_vm_data(
        rubrik, vsphere_vm_name, module)
    proposed_sla_id = get_sla_domain_id(rubrik, sla_domain_name, module)

    if current_sla_id == proposed_sla_id:
        results['changed'] = False
        results['response'] = "The vSphere VM '{}' is already configured with the '{}' SLA Domain.".format(
            vsphere_vm_name, sla_domain_name)
    else:

        update_vm_data_model = {
            "configured_sla_domain_id": proposed_sla_id
        }

        rubrik.update_vm(id=vm_id, vm_update_properties=update_vm_data_model)
        results['changed'] = True
        results['response'] = "Successfully configured the vSphere VM '{}' with the '{}' SLA Domain.".format(
            vsphere_vm_name, sla_domain_name)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
