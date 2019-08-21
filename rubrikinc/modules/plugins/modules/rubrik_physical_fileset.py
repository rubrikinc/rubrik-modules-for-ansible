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
module: rubrik_physical_fileset
short_description: Create a Rubrik fileset for a Linux or Windows machine.
description:
    - Create a Fileset for a Linux or Windows machine.
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  fileset_name:
    description:
      - The name of the Fileset you wish to create.
    required: True
    aliases: ["name"]
  operating_system:
    description:
      - The operating system type of the Fileset you are creating.
    required: True
    choices: [Linux, Windows]
  include:
    description:
      - The full paths or wildcards that define the objects to include in the Fileset backup.
    required: False
    type: list
    default: []
  exclude:
    description:
      - The full paths or wildcards that define the objects to exclude from the Fileset backup.
    required: False
    type: list
    default: []
  exclude_exception:
    description:
      - The full paths or wildcards that define the objects that are exempt from the excludes variables.
    required: False
    type: list
    default: []
  follow_network_shares:
    description:
      - Include or exclude locally-mounted remote file systems from backups.
    required: False
    type: bool
    default: False
  backup_hidden_folders:
    description:
      - Include or exclude hidden folders inside locally-mounted remote file systems from backups.
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
    - rubrik_cdm
requirements: [rubrik_cdm]
'''


EXAMPLES = '''
- rubrik_physical_fileset:
    name: 'AnsibleDemo'
    include: '/usr/local'
    operating_system: 'Linux'
    exclude: '/usr/local/temp,*.mp3,*.mp4,*mp5'
    exclude_exception: '/company*.mp4'
    follow_network_shares: False
    backup_hidden_folders: False
'''

RETURN = '''
response:
    description: The full response for the POST /internal/fileset_template/bulk API endpoint.
    returned: on success
    type: dict
    sample: {
        "hasMore": true,
        "data": [
          {
            "allowBackupNetworkMounts": true,
            "allowBackupHiddenFoldersInNetworkMounts": true,
            "useWindowsVss": true,
            "name": "string",
            "includes": [
              "string"
            ],
            "excludes": [
              "string"
            ],
            "exceptions": [
              "string"
            ],
            "operatingSystemType": "Linux",
            "shareType": "NFS",
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string",
            "id": "string",
            "primaryClusterId": "string",
            "isArchived": true,
            "hostCount": 0,
            "shareCount": 0
          }
        ],
        "total": 0
      }

response:
    description: A "No changed required" message when the NAS Fileset is already present on the Rubrik cluster.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The Rubrik cluster already has a NAS Fileset named 'name' configured with the provided variables.
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
        fileset_name=dict(required=True, aliases=['name']),
        operating_system=dict(required=True, choices=['Linux', 'Windows']),
        include=dict(required=False, type='list', default=[]),
        exclude=dict(required=False, type='list', default=[]),
        exclude_exception=dict(required=False, type='list', default=[]),
        follow_network_shares=dict(required=False, type='bool', default=False),
        backup_hidden_folders=dict(required=False, type='bool', default=False),
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

    fileset_name = ansible["fileset_name"]
    operating_system = ansible["operating_system"]
    include = ansible["include"]
    exclude = ansible["exclude"]
    exclude_exception = ansible["exclude_exception"]
    follow_network_shares = ansible["follow_network_shares"]
    backup_hidden_folders = ansible["backup_hidden_folders"]
    timeout = ansible["timeout"]

    try:
        api_request = rubrik.create_physical_fileset(
            fileset_name,
            operating_system,
            include,
            exclude,
            exclude_exception,
            follow_network_shares,
            backup_hidden_folders,
            timeout)

    except Exception as error:
        module.fail_json(msg=str(error))

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
