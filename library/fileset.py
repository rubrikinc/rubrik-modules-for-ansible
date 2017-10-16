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
            node                = dict(required=True, type='str'),
            rubrik_user         = dict(required=True, type='str'),
            rubrik_pass         = dict(required=True, type='str', no_log=True),
            sla_domain          = dict(required=True, type='str'),
            host_name           = dict(required=True, type='str'),
            fileset_template    = dict(required=True, type='str')
        )
    )

    debug_output = []

    try:
        rk = RubrikClient.create(module.params['node'], module.params['rubrik_user'], module.params['rubrik_pass'])

    except:
        module.fail_json(msg="Rubrik node connection issues.  Please check Rubrik node IP address or hostname in the YAML configuration file.")

    '''Check to see if host exists'''
    my_host = False
    host_query = rk.query_host(primary_cluster_id='local', limit=20000, is_relic=False, hostname=module.params['host_name'])
    for host in host_query.data:
        if host.hostname == module.params['host_name']:
            my_host = host

    if not my_host:
        module.fail_json(msg="Host does not exist.  Please check the YAML configuration file.")

    '''Figure out the SLA Domain ID'''
    my_sla = False
    sla_query = rk.query_sla_domain(primary_cluster_id='local', limit=20000, is_relic=False, name=module.params['sla_domain'])
    for sla in sla_query.data:
        if sla.name == module.params['sla_domain']:
            my_sla = sla

    if not my_sla:
        module.fail_json(msg="SLA Domain does not exist.  Please check the YAML configuration file.")

    '''Get the fileset template ID'''
    my_template = False
    fileset_template_query = rk.query_fileset_template(primary_cluster_id='local', name=module.params['fileset_template'])
    for fileset_template in fileset_template_query.data:
        if fileset_template.name == module.params['fileset_template']:
            my_template = fileset_template

    if not my_sla:
        module.fail_json(msg="Fileset Template does not exist.  Please check the YAML configuration file.")

    '''Check if the fileset already exists'''
    fileset_exists = False
    fileset_query = rk.query_fileset(primary_cluster_id='local', host_id=my_host.id, is_relic=False, template_id=my_template.id)
    if fileset_query.total == 1:
        my_fileset = fileset_query.data[0]
        debug_output.append('Fileset already exists, with id '+my_fileset.id)
        fileset_exists = True

    '''Create the fileset'''
    if not fileset_exists:
        debug_output.append('Creating fileset for host '+my_host.id+' and template '+my_template.id)
        my_fileset = rk.create_fileset(definition={'host_id':my_host.id, 'template_id':my_template.id})

    '''Apply the SLA domain to the fileset'''
    if my_fileset.effective_sla_domain_id == my_sla.id:
        debug_output.append('Fileset is already configured with the correct SLA domain')
    else:
        debug_output.append('Reconfiguring fileset with the correct SLA domain')
        rk.update_fileset(id=my_fileset.id, fileset_update_properties={'configured_sla_domain_id':my_sla.id})
        module.exit_json(changed=True, debug_out=debug_output)

    module.exit_json(changed=False, debug_out=debug_output)

if __name__ == '__main__':
    main()
