#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def current_hosts(module, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_get(module, api_version, endpoint)

    host_present = False

    for host in response_body['data']:
        if host['hostname'] == hostname:
            host_present = True
            break

    return host_present


def get_fileset_template_id(module, fileset):

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset_template?name={}'.format(fileset)

    response_body = rubrik_get(module, api_version, endpoint)

    if not response_body['data']:
        module.fail_json(msg=("There is no Fileset named '{}' on the Rubrik Cluster.".format(fileset)))
    else:
        for template in response_body['data']:
            if template['name'] == fileset:
                fileset_id = template['id']
                break
    try:
        fileset_id
    except NameError:
        module.fail_json(msg=("There is no Fileset named '{}' on the Rubrik Cluster.".format(fileset)))

    return fileset_id


def get_fileset_id(module, host_id, fileset_template_id):

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&template_id={}'.format(
        host_id, fileset_template_id)

    response_body = rubrik_get(module, api_version, endpoint)

    for key, value in response_body['data'][0].items():
        if key == "id":
            fileset_id = value
            break

    return fileset_id


def get_host_id(module, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/host'

    response_body = rubrik_get(module, api_version, endpoint)

    for host in response_body['data']:
        if host['hostname'] == hostname:
            host_id = host['id']
            break
    try:
        host_id
    except NameError:
        module.fail_json(msg=("The Host '{}' has not been added to the Rubrik Cluster.".format(hostname)))

    return host_id


def current_filesets(module, fileset_template_id, host_id, sla_domain_id):

    fileset_exists = False

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&template_id={}'.format(
        host_id, fileset_template_id)

    response_body = rubrik_get(module, api_version, endpoint)

    if response_body['total'] != 1:
        # create fileset
        fileset_exists = True
        for data in response_body['data']:
            fileset_id = data['id']

    endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&effective_sla_domain_id={}&template_id={}'.format(
        host_id, sla_domain_id, fileset_template_id)

    response_body = rubrik_get(module, api_version, endpoint)

    if response_body['total'] == 1:
        fileset_exists = True
        for data in response_body['data']:
            fileset_id = data['id']

    return fileset_exists, fileset_id


def get_sla_domain_id(module, sla_domain_name):

    api_version = 'v1' #v1 or internal
    endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(sla_domain_name)

    response_body = rubrik_get(module, api_version, endpoint)

    # Check if any results are returned
    if not response_body['data']:
        module.fail_json(msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(sla_domain_name)))
    else:
        for sla_domain in response_body['data']:
            if sla_domain['name'] == sla_domain_name:
                sla_id = sla_domain['id']

    return sla_id


def update_fileset_properties(module, sla_domain_id, fileset_id):

    update_fileset_data_model = {}
    update_fileset_data_model['configuredSlaDomainId'] = sla_domain_id

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset/{}'.format(fileset_id)

    response_body = rubrik_patch(module, api_version, endpoint, update_fileset_data_model)

    return response_body


def create_fileset(module, host_id, fileset_template_id):

    create_fileset_data_model = {}
    create_fileset_data_model['hostId'] = host_id
    create_fileset_data_model['templateId'] = fileset_template_id

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset'

    rubrik_post(module, api_version, endpoint, create_fileset_data_model)


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            fileset=dict(required=False),
            sla_domain_name=dict(required=False, aliases=['sla']),

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
    hostname = ansible['hostname']
    fileset = ansible['fileset']
    sla_domain_name = ansible['sla_domain_name']

    host_present = current_hosts(module, hostname)

    if host_present is False:
        results['changed'] = False
        results['response'] = "'{}' is not present on the Rubrik Cluster.".format(hostname)

    host_id = get_host_id(module, hostname)
    fileset_template_id = get_fileset_template_id(module, fileset)
    sla_domain_id = get_sla_domain_id(module, sla_domain_name)

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&template_id={}'.format(
        host_id, fileset_template_id)

    response_body = rubrik_get(module, api_version, endpoint)

    if response_body['total'] != 1:

        create_fileset(module, host_id, fileset_template_id)

        fileset_id = get_fileset_id(module, host_id, fileset_template_id)

        response = update_fileset_properties(module, sla_domain_id, fileset_id)

        results['changed'] = True
        results['response'] = response
    else:
        endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&effective_sla_domain_id={}&template_id={}'.format(
            host_id, sla_domain_id, fileset_template_id)

        response_body = rubrik_get(module, api_version, endpoint)

        if response_body['total'] != 1:

            fileset_id = get_fileset_id(module, host_id, fileset_template_id)

            response = update_fileset_properties(module, sla_domain_id, fileset_id)

            results['changed'] = True
            results['response'] = response
        else:
            results['changed'] = False
            results['response'] = "The '{}' Host is already configured with the '{}' Fileset.".format(hostname, fileset)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post, rubrik_patch # isort:skip


if __name__ == "__main__":
    main()
