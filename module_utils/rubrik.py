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
from ansible.module_utils.six import iteritems

try:
    from pyRubrik import RubrikClient
    HAS_RUBRIK_CLIENT = True
except ImportError:
    HAS_RUBRIK_CLIENT = False

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


def connect_to_cluster(node, username, password, module):

    node = module.params['node']
    username = module.params['username']
    password = module.params['password']

    if not HAS_RUBRIK_CLIENT:
        module.fail_json(
            msg='The required pyRubrik library is missing. Please install. ')

    try:
        create_connection = RubrikClient.create(node, username, password)
    except:
        module.fail_json(
            msg="We are unable to connect to the Rubrik Cluster. Please verify the provided credentials.")

    return create_connection
