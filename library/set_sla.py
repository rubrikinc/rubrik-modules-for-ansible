#!/usr/bin/python

import sys
import os
import json
import requests
import getopt
import base64
import traceback

import ansible.module_utils.pyRubrik as RubrikClient
from ansible.module_utils.basic import *

def main():
    requests.packages.urllib3.disable_warnings()

    module = AnsibleModule(
        argument_spec = dict(
            node            = dict(required=True, type='str'),
            rubrik_user     = dict(required=True, type='str'),
            rubrik_pass     = dict(required=True, type='str', no_log=True),
            sla_domain      = dict(required=True, type='str'),
            vmware_vm_name  = dict(required=True, type='str')
        )
    )

    debug_output = []

    try:
        rk = RubrikClient.create(module.params['node'], module.params['rubrik_user'], module.params['rubrik_pass'])

    except:
        module.fail_json(msg="Rubrik node connection issues.  Please check Rubrik node IP address or hostname in the YAML configuration file.")

    '''Check to see if VM exists'''
    my_vm = False
    vm_query = rk.query_vm(primary_cluster_id='local', limit=20000, is_relic=False, name=module.params['vmware_vm_name'])
    for vm in vm_query.data:
        if vm.name == module.params['vmware_vm_name']:
            my_vm = vm

    if not my_vm:
        module.fail_json(msg="VMware VM does not exist.  Please check the YAML configuration file.")

    '''Compare current SLA domain to desired one, and update if necessary'''
    if my_vm.effective_sla_domain_name == module.params['sla_domain']:
        debug_output.append('SLA Domain = effective')
        module.exit_json(changed=False, debug_out=debug_output)
    else:
        my_sla = False
        sla_query = rk.query_sla_domain(primary_cluster_id='local', limit=20000, is_relic=False, name=module.params['sla_domain'])
        for sla in sla_query.data:
            if sla.name == module.params['sla_domain']:
                my_sla = sla

        if not my_sla:
            module.fail_json(msg="SLA Domain does not exist.  Please check the YAML configuration file.")

        rk.update_vm(id=my_vm.id, vm_update_properties={"configured_sla_domain_id": my_sla.id})
        debug_output.append('SLA Domain != effective')
        module.exit_json(changed=True, debug_out=debug_output)

    module.exit_json(changed=False, debug_out=debug_output)

if __name__ == '__main__':
    main()
