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
module: rubrik_job_status
short_description: Monitor the progress of a Rubrik job.
description:
    - Certain Rubrik operations may not instantaneously complete. In those cases we have the ability to monitor the status of
      the job through a job status link provided in the actions API response body. In those cases the Ansible Module will return a "job_status_link"
      which can then be registered and used as a variable in the rubrik_job_status module. The rubrik_job_status will check on the status of the
      job every 20 seconds until the job has successfully completed for failed.
version_added: 2.8
author: Rubrik Ranger Team
options:
  url:
    description:
      - The job status URL provided by a previous API call.
    required: True
  wait_for_completion:
    description:
      - Flag that determines if the method should wait for the job to complete before exiting.
    required: False
    type: bool
    default: True
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
- rubrik_job_status:
    url: "https://192.168.1.100/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0"
'''

RETURN = '''
response:
    description: The full API response for the API call.
    returned: on success
    type: dict
    sample: differs depending on the object_type being monitored.
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrik_cdm import load_provider_variables, rubrik_argument_spec

try:
    import rubrik_cdm
    sdk_present = True
except BaseException:
    sdk_present = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = rubrik_argument_spec

    # Start Parameters
    argument_spec.update(
        dict(
            url=dict(required=True),
            wait_for_completion=dict(required=False, type='bool', default=True),
            timeout=dict(required=False, type='int', default=15)
        )
    )
    # End Parameters

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if sdk_present is False:
        module.fail_json(msg="The Rubrik Python SDK is required for this module (pip install rubrik_cdm).")

    load_provider_variables(module)
    ansible = module.params

    try:
        rubrik = rubrik_cdm.Connect()
    except SystemExit as error:
        if "has not been provided" in str(error):
            try:
                ansible["node_ip"]
                ansible["username"]
                ansible["password"]
            except KeyError:
                module.fail_json(
                    msg="Error: The Rubrik login credentials are missing. Verify the correct env vars are present or provide them through the provider param.")
        else:
            module.fail_json(msg=str(error))

        try:
            rubrik = rubrik_cdm.Connect(ansible['node_ip'], ansible['username'], ansible['password'])
        except SystemExit as error:
            module.fail_json(msg=str(error))

    try:
        api_request = rubrik.job_status(ansible["url"], ansible["wait_for_completion"], ansible["timeout"])
    except SystemExit as error:
        module.fail_json(msg=str(error))

    results["changed"] = False

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
