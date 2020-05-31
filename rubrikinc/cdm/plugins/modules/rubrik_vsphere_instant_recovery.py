#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_vsphere_instant_recovery
short_description: Instantly recover a vSphere VM from a provided snapshot.
description:
    - Instantly recover a vSphere VM from a provided snapshot.
    - If a specific date and time is not provided, the last snapshot taken will be used.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  vm_name:
    description:
      - The name of the VM to Instantly Recover.
    required: True
    type: str
  date:
    description:
      - The date of the snapshot you wish to Instantly Recover formated as Month-Day-Year (ex. 1-15-2014).
      - If latest is specified, the last snapshot taken will be used.
    required: False
    type: str
    default: latest
  time:
    description:
      - The time of the snapshot you wish to Instantly Recover formated as Hour:Minute AM/PM (ex. 1:30 AM).
      - If latest is specified, the last snapshot taken will be used.
    required: False
    type: str
    default: latest
  host:
    description:
      - The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default, the current host will be used.
    required: False
    type: str
    default: current
  remove_network_devices:
    description:
      - Flag that determines whether to remove the network interfaces from the Instantly Recovered VM. Set to True to remove all network interfaces.
    required: False
    type: bool
    default: False
  power_on:
    description:
      - Flag that determines whether the VM should be powered on after the Instant Recovery.
      - Set to True to power on the VM. Set to False to mount the VM but not power it on.
    required: False
    type: bool
    default: True
  disable_network:
    description:
      - Sets the state of the network interfaces when the VM is instantly recovered.
      - Use False to enable the network interfaces. Use True to disable the network interfaces.
      - Disabling the interfaces can prevent IP conflicts.
    required: False
    type: bool
    default: False
  keep_mac_addresses:
    description:
      - Flag that determines whether the MAC addresses of the network interfaces on the source VM are assigned to the new VM.
      - Set to True to assign the original MAC addresses to the new VM. Set to False to assign new MAC addresses.
      - When 'remove_network_devices' is set to True, this property is ignored.
    required: False
    type: bool
    default: False
  preserve_moid:
    description:
      - Flag that determines whether to preserve the MOID of the source VM in a restore operation.
      - Use True to keep the MOID of the source. Use False to assign a new moid.
    required: False
    type: bool
    default: False
  timeout:
    description:
      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    type: int
    default: 15

extends_documentation_fragment:
    - rubrikinc.cdm.credentials
requirements: [rubrik_cdm]
'''


EXAMPLES = '''
- rubrik_vsphere_instant_recovery:
    vm_name: 'ansible-tower'

- rubrik_vsphere_instant_recovery:
    vm_name: 'ansible-tower'
    date: '1-15-2019'
    time: '1:30 PM'

'''

RETURN = '''
full_response:
    description: The full API response for POST /v1/vmware/vm/snapshot/{snapshot_id}/instant_recover.
    returned: success
    type: dict
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
        vm_name=dict(required=True, type='str'),
        date=dict(required=False, type='str', default="latest"),
        time=dict(required=False, type='str', default="latest"),
        host=dict(required=False, type='str', default="current"),
        remove_network_devices=dict(required=False, type='bool', default=False),
        power_on=dict(required=False, type='bool', default=True),
        disable_network=dict(required=False, type='bool', default=False),
        keep_mac_addresses=dict(required=False, type='bool', default=False),
        preserve_moid=dict(required=False, type='bool', default=False),
        timeout=dict(required=False, type='int', default=15),

    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.vsphere_instant_recovery(
            ansible["vm_name"],
            ansible["date"],
            ansible["time"],
            ansible["host"],
            ansible["remove_network_devices"],
            ansible["power_on"],
            ansible["disable_network"],
            ansible["keep_mac_addresses"],
            ansible["preserve_moid"],
            ansible["timeout"])
    except Exception as error:
        module.fail_json(msg=str(error))

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
