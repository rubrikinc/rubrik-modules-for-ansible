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
module: rubrik_fileset
requirements: pyRubrik
extends_documentation_fragment: rubrik
version_added: "2.5"
short_description: Manage a Physical Host Fileset.
description:
    - Add, Delete, or Manage Protection of a Physical Host.
author:
    - Drew Russell (t. @drusse11)
options:
    hostname:
        description:
            - The DNS hostname or IP address of the Physical Host.
        required: true
        aliases: ip_address
        default: null
    fileset:
        description:
            - The name of the Fileset to associate with the Host.
        required: false
        default: null
    sla_domain_name:
        description:
            - The name of the SLA Domain to associate with the I(Fileset).
        required: false
        aliases: sla
        default: null
'''

EXAMPLES = '''
- name: Configure a Hosts Fileset
  rubrik_fileset:
    provider={{ credentials }}
    hostname={{ hostname }}
    fileset={{ fileset }}
    sla_domain_name={{ sla_domain_name }}
'''

RETURN = '''
response:
    description: Human readable description of the results of the module execution.
    returned: success
    type: dict
    sample: {"response": "'Linux-Physical' has successfully added to the Rubrik Cluster.}
'''


def current_hosts(rubrik, hostname):

    host_present = False
    hosts = rubrik.query_host()
    for host in hosts.data:
        if host.hostname == hostname:
            host_present = True
            break

    return host_present


def get_fileset_template_id(rubrik, fileset, module):

    fileset_query = rubrik.query_fileset_template(
        primary_cluster_id='local', name=fileset)

    if not fileset_query.data:
        module.fail_json(
            msg=("There is no Fileset named '{}' on the Rubrik Cluster.".format(fileset)))
    else:
        for template in fileset_query.data:
            if template.name == fileset:
                fileset_id = template.id
                break

    return fileset_id


def get_fileset_id(rubrik, host_id, fileset_template_id):
    fileset_query = rubrik.query_fileset(
        primary_cluster_id='local', host_id=host_id, template_id=fileset_template_id, is_relic=False)

    data = fileset_query.data[0].__dict__
    for key, value in data.items():
        if key == "id":
            fileset_id = value
            break

    return fileset_id


def get_host_id(rubrik, hostname):

    hosts = rubrik.query_host()
    for host in hosts.data:
        if host.hostname == hostname:
            host_id = host.id
            break

    return host_id


def current_filesets(rubrik, fileset_template_id, host_id, sla_domain_id):

    fileset_exists = False

    # Determine if the basic Fileset (host + template) exsits
    fileset_query = rubrik.query_fileset(
        primary_cluster_id='local', host_id=host_id, template_id=fileset_template_id, is_relic=False, )

    if fileset_query.total != 1:
        # create fileset
        fileset_exists = True
        for data in fileset_query:
            fileset_id = data.id

    fileset_query = rubrik.query_fileset(
        primary_cluster_id='local', host_id=host_id, effective_sla_domain_id=sla_domain_id, template_id=fileset_template_id, is_relic=False, )

    if fileset_query.total == 1:
        fileset_exists = True
        for data in fileset_query:
            fileset_id = data.id

    return fileset_exists, fileset_id


def get_sla_domain_id(rubrik, sla_domain_name, module):

    query_sla_domain = rubrik.query_sla_domain(
        primary_cluster_id='local', name=sla_domain_name, is_relic=False)

    # Check if any results are returned
    if not query_sla_domain.data:
        module.fail_json(
            msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(sla_domain_name)))
    else:
        for sla_domain in query_sla_domain.data:
            if sla_domain.name == sla_domain_name:
                sla_id = sla_domain.id

    return sla_id


def update_fileset_properties(rubrik, sla_domain_id, fileset_id):

    update_fileset_data_model = {
        "configuredSlaDomainId": sla_domain_id,
    }

    rubrik.update_fileset(
        id=fileset_id, fileset_update_properties=update_fileset_data_model)


def create_fileset(rubrik, host_id, fileset_template_id):

    create_fileset_data_model = {
        'hostId': host_id,
        'templateId': fileset_template_id,
    }

    rubrik.create_fileset(definition=create_fileset_data_model)


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

    rubrik = connect_to_cluster(node, username, password, module)

    host_present = current_hosts(rubrik, hostname)

    if host_present is False:
        results['changed'] = False
        results['response'] = "'{}' is not present on the Rubrik Cluster.".format(hostname)

    host_id = get_host_id(rubrik, hostname)
    fileset_template_id = get_fileset_template_id(rubrik, fileset, module)
    sla_domain_id = get_sla_domain_id(rubrik, sla_domain_name, module)

    fileset_query = rubrik.query_fileset(primary_cluster_id='local', host_id=host_id,
                                         template_id=fileset_template_id, is_relic=False)

    if fileset_query.total != 1:

        create_fileset(rubrik, host_id, fileset_template_id)

        fileset_id = get_fileset_id(rubrik, host_id, fileset_template_id)

        update_fileset_properties(rubrik, sla_domain_id, fileset_id)

        results['changed'] = True
        results['response'] = "Successfully associted Host '{}' with the '{}' Fileset.".format(
            hostname, fileset)

    else:
        fileset_query = rubrik.query_fileset(primary_cluster_id='local', host_id=host_id,
                                             template_id=fileset_template_id, effective_sla_domain_id=sla_domain_id, is_relic=False)

        if fileset_query.total != 1:

            fileset_id = get_fileset_id(rubrik, host_id, fileset_template_id)

            update_fileset_properties(rubrik, sla_domain_id, fileset_id)

            results['changed'] = True
            results['response'] = "Successfully updated the Host '{}' with the '{}' Fileset.".format(hostname, fileset)
        else:
            results['changed'] = False
            results['response'] = "The '{}' Host is already configured with the '{}' Fileset.".format(hostname, fileset)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
