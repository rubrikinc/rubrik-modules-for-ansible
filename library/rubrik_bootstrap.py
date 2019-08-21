#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_bootstrap
short_description: Issues a bootstrap request to a specified Rubrik cluster
description:
    - Issues a bootstrap request to a specified Rubrik cluster
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  cluster_name:
    description:
      - Unique name to assign to the Rubrik cluster.
    required: True
    type: str
  admin_email:
    description:
      - The Rubrik cluster sends messages for the admin account to this email address.
    required: True
    type: str
  admin_password:
    description:
      - Password for the admin account.
    required: True
    type: str
  management_gateway:
    description:
      - IP address assigned to the management network gateway
    required: True
    type: str
  management_subnet_mask:
    description:
      - Subnet mask assigned to the management network.
    required: True
    type: str
  node_config:
    description:
      - The Node Name and IP formatted as a dictionary
    required: True
    type: dict
  enable_encryption:
    description:
      - Enable software data encryption at rest. When bootstraping a Cloud Cluster this value needs to be False.
    required: False
    type: bool
    default: True
  dns_search_domains:
    description:
      - The search domain that the DNS Service will use to resolve hostnames that are not fully qualified.
    required: False
    type: list
    default: []
  dns_nameservers:
    description:
      - IPv4 addresses of DNS servers
    required: False
    type: list
    default: [8.8.8.8]
  ntp_servers:
    description:
      - FQDN or IPv4 address of a network time protocol (NTP) server.
    required: False
    type: list
    default: [pool.ntp.org]
  wait_for_completion:
    description:
      - Flag to determine if the function should wait for the bootstrap process to complete.
    required: False
    type: bool
    default: True
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 30

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_bootstrap:
    node_ip: "{{ mgmt_node_ip }}"
    cluster_name: "Ansible Demo"
    admin_email: "ansiblebuild@rubrik.com"
    admin_password: "AnsibleAndRubrikPassword"
    management_gateway: "10.255.1.1"
    management_subnet_mask: "255.255.255.0"
    enable_encryption: True
    dns_search_domains: ["rubrikansible.com"]
    wait_for_completion: True
    node_config: "{{ node_config }}"
'''

RETURN = '''
response:
    description: The full API response for POST /internal/cluster/me/bootstrap.
    returned: on success
    type: dict
'''


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
        cluster_name=dict(required=True, type='str'),
        admin_email=dict(required=True, type='str'),
        admin_password=dict(required=True, type='str', no_log=True),
        management_gateway=dict(required=True, type='str'),
        management_subnet_mask=dict(required=True, type='str'),
        node_config=dict(required=True, type='dict'),
        enable_encryption=dict(required=False, type='bool', default=True),
        dns_search_domains=dict(required=False, type='list', default=[]),
        dns_nameservers=dict(required=False, type='list', default=['8.8.8.8']),
        ntp_servers=dict(required=False, type='list', default=['pool.ntp.org']),
        wait_for_completion=dict(required=False, type='bool', default=True),
        timeout=dict(required=False, type='int', default=30),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Bootstrap(node_ip)
    except Exception as error:
        module.fail_json(msg=str(error))

    cluster_name = ansible["cluster_name"]
    admin_email = ansible["admin_email"]
    admin_password = ansible["admin_password"]
    management_gateway = ansible["management_gateway"]
    management_subnet_mask = ansible["management_subnet_mask"]
    node_config = ansible["node_config"]
    enable_encryption = ansible["enable_encryption"]
    dns_search_domains = ansible["dns_search_domains"]
    dns_nameservers = ansible["dns_nameservers"]
    ntp_servers = ansible["ntp_servers"]
    wait_for_completion = ansible["wait_for_completion"]
    timeout = ansible["timeout"]

    try:
        api_request = rubrik.setup_cluster(cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask,
                                           node_config, enable_encryption, dns_search_domains, dns_nameservers, ntp_servers, wait_for_completion, timeout)
    except Exception as error:
        module.fail_json(msg=str(error))

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
