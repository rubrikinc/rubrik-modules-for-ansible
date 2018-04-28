#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def get_vsphere_vm_data(module, vsphere_vm_name):

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(vsphere_vm_name)

    response_body = rubrik_get(module, api_version, endpoint)

    # Check if any results are returned
    if not response_body['data']:
        module.fail_json(
            msg=("There is no vSphere VM named '{}' on the Rubrik Cluster.".format(vsphere_vm_name)))
    else:
        for vm in response_body['data']:
            if vm['name'] == vsphere_vm_name:
                vm_id = vm['id']
                sla_domain_id = vm['effectiveSlaDomainId']

    try:
        vm_id
    except NameError:
        module.fail_json(
            msg=("There is no vSphere VM named '{}' on the Rubrik Cluster.".format(vsphere_vm_name)))

    return vm_id, sla_domain_id


def get_sla_domain_id(module, sla_domain_name):

    api_version = 'v1' #v1 or internal
    endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(sla_domain_name)
    # endpoint = '/sla_domain?primary_cluster_id=local&name=Instant%20Recovery%20Demo'

    response_body = rubrik_get(module, api_version, endpoint)

    # Check if any results are returned
    if not response_body['data']:
        module.fail_json(msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(sla_domain_name)))
    else:
        for sla_domain in response_body['data']:
            if sla_domain['name'] == sla_domain_name:
                sla_id = sla_domain['id']

    try:
        sla_id
    except NameError:
        module.fail_json(msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(sla_domain_name)))

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

    vm_id, current_sla_id = get_vsphere_vm_data(module, vsphere_vm_name)

    proposed_sla_id = get_sla_domain_id(module, sla_domain_name)

    if current_sla_id == proposed_sla_id:
        results['changed'] = False
        results['response'] = "The vSphere VM '{}' is already configured with the '{}' SLA Domain.".format(
            vsphere_vm_name, sla_domain_name)
    else:

        update_vm_data_model = {}
        update_vm_data_model['configuredSlaDomainId'] = proposed_sla_id

        api_version = 'v1' #v1 or internal
        endpoint = '/vmware/vm/{}'.format(vm_id)

        response_body = rubrik_patch(module, api_version, endpoint, update_vm_data_model)

        results['changed'] = True
        results['response'] = response_body

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post, rubrik_patch  # isort:skip


if __name__ == "__main__":
    main()
