# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2017 Rubrik Inc.
# Author: Drew Russell (@drusse11)
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import json
from ansible.module_utils.six import iteritems
from ansible.module_utils.urls import open_url, basic_auth_header
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError  # isort:skip


login_credentials_spec = {
    'node': dict(),
    'username': dict(),
    'password': dict(no_log=True),
}

rubrik_argument_spec = {
    'provider': dict(type='dict', options=login_credentials_spec),
}


def load_provider_variables(module):
    '''Pull the node, username, and password arguments from the provider
    variable '''

    provider = module.params.get('provider') or dict()
    for key, value in iteritems(provider):
        if key in login_credentials_spec:
            if module.params.get(key) is None and value is not None:
                module.params[key] = value


def rubrik_get(module, api_version, endpoint, timeout=20):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    url = 'https://{}/api/{}{}'.format(ansible['node'], api_version, endpoint)

    headers = {
        'Accept': "application/json",
        'Authorization': basic_auth_header(ansible['username'], ansible['password'])
    }

    try:
        response = open_url(url=url, method='GET', headers=headers, validate_certs=False)

        response_body = json.loads(response.read())

        # total_number_of_results = int(response_body['total'])

        # if total_number_of_results == 0:
        #     module.fail_json(msg='The Rubrik Cluster does not contain a VM named "{}"'.format(
        #         ansible['vsphere_vm_name']))
        # elif total_number_of_results != 1:
        #     module.fail_json(msg='The search for a VM "{}" returned multiple results. Please verify the VM name.'.format(
        #         ansible['vsphere_vm_name']))

        # vm_id = response_body['data'][0]['id']

    except HTTPError as error:
        response_body = error.read()
        module.fail_json(msg=str(response_body))
    except URLError:
        module.fail_json(msg='Connection to the Node IP timed out.')

    return response_body


def rubrik_post(module, api_version, endpoint, data, timeout=20):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    url = 'https://{}/api/{}{}'.format(ansible['node'], api_version, endpoint)

    headers = {
        'Accept': "application/json",
        'Authorization': basic_auth_header(ansible['username'], ansible['password']),

    }

    try:

        response = open_url(url=url, method='POST', data=data, headers=headers, validate_certs=False)

        response_body = json.loads(response.read())

    except HTTPError as error:
        response_body = error.read()
        module.fail_json(msg=str(response_body))
    except URLError:
        module.fail_json(msg='Connection to the Node IP timed out.')

    return response_body


def rubrik_job_status(module, url, timeout=20):
    ''' '''

    # Ansible Specific Variables
    ansible = module.params

    url = url

    headers = {
        'Accept': "application/json",
        'Authorization': basic_auth_header(ansible['username'], ansible['password'])
    }

    try:
        response = open_url(url=url, method='GET', headers=headers, validate_certs=False)

        response_body = json.loads(response.read())

        # total_number_of_results = int(response_body['total'])

        # if total_number_of_results == 0:
        #     module.fail_json(msg='The Rubrik Cluster does not contain a VM named "{}"'.format(
        #         ansible['vsphere_vm_name']))
        # elif total_number_of_results != 1:
        #     module.fail_json(msg='The search for a VM "{}" returned multiple results. Please verify the VM name.'.format(
        #         ansible['vsphere_vm_name']))

        # vm_id = response_body['data'][0]['id']

    except HTTPError as error:
        response_body = error.read()
        module.fail_json(msg=str(response_body))
    except URLError:
        module.fail_json(msg='Connection to the Node IP timed out.')

    return response_body
