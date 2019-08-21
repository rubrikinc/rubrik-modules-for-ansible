#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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
module: rubrik_on_demand_snapshot
short_description: Take an on-demand snapshot of a Rubrik object.
description:
    - Take an on-demand snapshot of a Rubrik object.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:

  object_name:
    description:
      - The name of the Rubrik object to take a on-demand snapshot of.
    required: True
    type: str

  object_type:
    description:
      - The Rubrik object type you want to backup.
    required: False
    type: str
    default: vmware
    choices: [vmware, physical_host, ahv]

  sla_name:
    description:
      - The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used.
    required: False
    type: str
    default: current

  fileset:
    description:
      - The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host.
    required: False
    type: str
    default: None

  host_os:
    description:
      - The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host.
    required: False
    type: str
    default: None
    choices: [None, Linux, Windows]


extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_on_demand_snapshot:
    object_name: 'ansible-node01'
    object_type: "vmware"

- rubrik_on_demand_snapshot:
        object_name: "ansible-demo"
        object_type: "physical_host"
        fileset: "Python SDK"
        host_os: "Linux"
'''

RETURN = '''
response:
    description: The full API response for POST /v1/vmware/vm/{id}/snapshot.
    returned: on success when action is vmware
    type: dict
    sample:
        {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2018-10-16T03:48:59.118Z",
            "endTime": "2018-10-16T03:48:59.118Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                "href": "string",
                "rel": "string"
                }
            ]
        }

response:
    description: The full API response for POST /v1/fileset/{id}/snapshot.
    returned: on success when object_type is physical_host
    type: dict
    sample:
        {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2018-10-16T03:48:58.625Z",
            "endTime": "2018-10-16T03:48:58.625Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                "href": "string",
                "rel": "string"
                }
            ]
        }

job_status_url:
    description: The job staturs url retuend by the full API response which can be passed into the rubrik_job_status module for monitoring.
    returned: on success
    type: str
    sample: https://192.168.8.19/api/v1/fileset/request/CREATE_FILESET_SNAPSHOT_a2f6161c-33a4-3123-efaw-de7d1bef284e_dc0983bf-1c47-45ce-9ce0-b8df3c93b5fa:::0
'''


try:
    import rubrik_cdm
    HAS_RUBRIK_SDK = True
except ImportError:
    HAS_RUBRIK_SDK = False


def main():
    """ Main entry point for Ansible module execution.
    """

    argument_spec = dict(
        object_name=dict(required=True, type='str'),
        object_type=dict(required=False, type='str', default="vmware", choices=["vmware", "physical_host", "ahv"]),
        sla_name=dict(required=False, type='str', default='current'),
        fileset=dict(required=False, type='str', default='None'),
        host_os=dict(required=False, type='str', default='None', choices=["None", "Linux", "Windows"]),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = {}

    ansible = module.params

    load_provider_variables(module)

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    if ansible["fileset"] == "None":
        ansible["fileset"] = None

    if ansible["host_os"] == "None":
        ansible["host_os"] = None

    object_name = ansible["object_name"]
    object_type = ansible["object_type"]
    sla_name = ansible["sla_name"]
    fileset = ansible["fileset"]
    host_os = ansible["host_os"]

    try:
        api_request, job_status_url = rubrik.on_demand_snapshot(object_name, object_type, sla_name, fileset, host_os)
    except Exception as error:
        module.fail_json(msg=str(error))

    results["changed"] = True

    results["response"] = api_request
    results["job_status_url"] = job_status_url

    module.exit_json(**results)


if __name__ == '__main__':
    main()
