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


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True, aliases=['ip_address']),
            action=dict(required=False, default='add',
                        choices=['add', 'delete']),
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

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
