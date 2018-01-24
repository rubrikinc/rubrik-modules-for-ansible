#!/usr/bin/python


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    node = ansible['node']
    username = ansible['username']
    password = ansible['password']

    rubrik = connect_to_cluster(node, username, password, module)

    public_cluster_information = rubrik.get_public_cluster_info()

    version = public_cluster_information.version
    cluster_id = public_cluster_information.id
    api_version = public_cluster_information.api_version

    results['version'] = version
    results['id'] = cluster_id
    results['api_version'] = api_version

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule  # isort:skip
from ansible.module_utils.rubrik import (
    connect_to_cluster, load_provider_variables, rubrik_argument_spec)  # isort:skip


if __name__ == "__main__":
    main()
