#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_replication_private
short_description: Configure replication partner as specified by user using PRIVATE NETWORK (direct connection).
description:
    - Configure replication partner as specified by user using PRIVATE NETWORK (direct connection).
version_added: '2.8'
author: Eric Alba (@KowMangler) <noman.wonder@gmail.com>
options:
  target_username:
    description:
      - Hostname of the SMTP server.
    required: True
    type: str
  target_password:
    description:
      - Incoming port on the SMTP server.
      - Normally port 25, port 465, or port 587, depending upon the type of encryption used.
    required: True
    type: str
  target_cluster_address:
    description:
      - The email address assigned to the account on the SMTP server.
    required: True
    type: str
  force:
    description:
      - Force the replication target to refresh if it already exists.
    required: False
    type: bool
  ca_certificate:
    description:
      - CA certificiate used to perform TLS certificate validation.
    required: False
    type: str
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 15

extends_documentation_fragment: rubrikinc.cdm.credentials
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_replication_private:
    target_username: admin
    target_password: Rubrik
    target_cluster_address: 10.10.10.10
'''


RETURN = '''
full_response:
    description: The full API response from POST /internal/replication/target
    returned: on success
    type: dict

idempotent_response:
    description: A "No changed required" message when the target cluster is already configured on the local cluster.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The Rubrik cluster is already configured with I(target_cluster_address) as it's target_cluster_address.
'''

from ansible.module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule

try:
    import rubrik_cdm
    HAS_RUBRIK_SDK = True
except ImportError:
    HAS_RUBRIK_SDK = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = dict(
        target_username=dict(required=True, type='str'),
        target_password=dict(required=True, type='str', no_log=True),
        target_cluster_address=dict(required=True, type='str'),
        force=dict(required=False, type='bool', default=False),
        ca_certificate=dict(required=False, type='str'),
        timeout=dict(required=False, type='int', default=15),

    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    target_username = ansible["target_username"]
    target_password = ansible["target_password"]
    target_cluster_address = ansible["target_cluster_address"]
    force = ansible["force"]
    ca_certificate = ansible["ca_certificate"]
    timeout = ansible["timeout"]

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))
    
    chg_required = True
    if not force:
        local_config = rubrik.get("internal", "/replication/target", timeout)
        if len(local_config['data']) > 0:
            try:
              remote_rubrik = rubrik_cdm.Connect(target_cluster_address, target_username, target_password)
            except Exception as error:
              module.fail_json(msg=str(error))
            remote_cluster_name = remote_rubrik.get("internal", "/cluster/me/name", timeout)
            for rep_target in local_config['data']:
                if rep_target['targetClusterName'] == remote_cluster_name:
                  chg_required = False
                  break

    api_request = None
    if chg_required:
        try:
            api_request = rubrik.configure_replication_private(
                target_username, target_password, target_cluster_address, ca_certificate, timeout)
        except Exception as error:
            module.fail_json(msg=str(error))
    else:
        api_request = "No change required. The Rubrik cluster is already configured with I(target_cluster_address) as it's target_cluster_address."
    
    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
