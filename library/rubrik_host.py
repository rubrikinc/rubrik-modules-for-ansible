def current_hosts(rubrik, hostname):

    host_present = False
    hosts = rubrik.query_host()
    for host in hosts.data:
        if host.hostname == hostname:
            host_present = True
            break

    return host_present


def add_host(rubrik, hostname):

    add_host_data_model = {
        "hostname": hostname,
        "hasAgent": "true"
    }

    rubrik.register_host(add_host_data_model)


def delete_host(rubrik, hostname):

    hosts = rubrik.query_host()
    for host in hosts.data:
        if host.hostname == hostname:
            host_id = host.id
            break

    rubrik.delete_host(host_id)


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
            msg=("There is no SLA Domain named '{}' on the Rubrik Cluster.".format(name)))
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


def create_fileset(rubrik, host_id, fileset_template_id, sla_domain_id):

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
            action=dict(required=False, default='add',
                        choices=['add', 'delete', 'manage_protection']),
        )
    )

    required_if = [('action', 'manage_protection', [
                    'fileset', 'sla_domain_name'])]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=required_if,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    node = ansible['node']
    username = ansible['username']
    password = ansible['password']
    hostname = ansible['hostname']
    action = ansible['action']

    rubrik = connect_to_cluster(node, username, password, module)

    host_present = current_hosts(rubrik, hostname)

    # Add a new host to the Rubrik Cluster
    if host_present is False and action == 'add':
        add_host(rubrik, hostname)
        results['changed'] = True
        results['response'] = "'{}' has successfully been added to the Rubrik Cluster.".format(
            hostname)
    else:
        results['changed'] = False
        results['response'] = "'{}' is already connected to the Rubrik Cluster.".format(
            hostname)

    # Delete a host to the Rubrik Cluster
    if host_present is True and action == 'delete':
        delete_host(rubrik, hostname)
        results['changed'] = True
        results['response'] = "'{}' has successfully been deleted from the Rubrik Cluster.".format(
            hostname)
    else:
        results['changed'] = False
        results['response'] = "'{}' is not present on the Rubrik Cluster.".format(
            hostname)

    # Manage the Protect (Fileset) of a Host
    if host_present is True and action == 'manage_protection':

        fileset = ansible['fileset']
        sla_domain_name = ansible['sla_domain_name']

        host_id = get_host_id(rubrik, hostname)
        fileset_template_id = get_fileset_template_id(rubrik, fileset, module)
        sla_domain_id = get_sla_domain_id(rubrik, sla_domain_name, module)

        fileset_query = rubrik.query_fileset(
            primary_cluster_id='local', host_id=host_id, template_id=fileset_template_id, is_relic=False)

        if fileset_query.total != 1:

            create_fileset(rubrik, host_id, fileset_template_id, sla_domain_id)

            fileset_id = get_fileset_id(rubrik, host_id, fileset_template_id)

            update_fileset_properties(rubrik, sla_domain_id, fileset_id)

            results['changed'] = True
            results['response'] = "Successfully associted Host '{}' with the '{}' Fileset.".format(
                hostname, fileset)

        else:
            fileset_query = rubrik.query_fileset(
                primary_cluster_id='local', host_id=host_id, template_id=fileset_template_id, effective_sla_domain_id=sla_domain_id, is_relic=False)

            if fileset_query.total != 1:

                fileset_id = get_fileset_id(
                    rubrik, host_id, fileset_template_id)

                update_fileset_properties(rubrik, sla_domain_id, fileset_id)

                results['changed'] = True
                results['response'] = "Successfully updated the Host '{}' with the '{}' Fileset.".format(
                    hostname, fileset)
            else:
                results['changed'] = False
                results['response'] = "The '{}' Host is already configured with the '{}' Fileset.".format(
                    hostname, fileset)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
