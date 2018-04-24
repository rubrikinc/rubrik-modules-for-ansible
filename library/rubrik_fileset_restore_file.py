#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def get_host_id(module):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    api_version = 'v1' #v1 or internal
    endpoint = '/vmware/host'

    response_body = rubrik_get(module, api_version, endpoint)

    for data in response_body['data']:
        if data['name'] == ansible['restore_host']:
            host_id = data['id']

    return host_id


def get_fileset(module, fileset_name, hostname):

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset?name={}&host_name={}'.format(fileset_name, hostname)

    response_body = rubrik_get(module, api_version, endpoint)

    #Check if any results are returned
    if not response_body['data']:
        module.fail_json(
            msg=("The host '{}' associated with the Fileset '{}' was not found on the Rubrik Cluster".format(hostname, fileset_name)))
    else:
        for data in response_body['data']:
            if data['hostName'] == hostname and data['templateName'] == fileset_name:
                fileset_id = data['id']

    return fileset_id


def get_fileset_snapshot(module, fileset_id):

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset/{}'.format(fileset_id)

    response_body = rubrik_get(module, api_version, endpoint)

    snapshot_id = response_body['snapshots'][0]['id']

    return snapshot_id


def restore_file(module, snapshot_id, file_name):

    destination = file_name.rsplit('/', 1)[0]

    data = {}
    data['sourceDir'] = file_name
    data['destinationDir'] = destination
    data['ignoreErrors'] = False

    api_version = 'v1' #v1 or internal
    endpoint = '/fileset/snapshot/{}/restore_file'.format(snapshot_id)

    response_body = rubrik_post(module, api_version, endpoint, data)

    return data


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            hostname=dict(required=True),
            fileset_name=dict(required=True),
            file_name=dict(required=True),

        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    hostname = ansible['hostname']
    fileset_name = ansible['fileset_name']
    file_name = ansible['file_name']

    fileset_id = get_fileset(module, fileset_name, hostname)
    snapshot_id = get_fileset_snapshot(module, fileset_id)

    response_body = restore_file(module, snapshot_id, file_name)

    results['changed'] = True
    results['response_body'] = response_body

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post  # isort:skip


if __name__ == "__main__":
    main()
