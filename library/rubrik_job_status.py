#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            job_status_link=dict(required=True, aliases=['href']),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    while True:

        response_body = rubrik_job_status(module, ansible['job_status_link'], timeout=60)

        job_status = response_body['status']

        if job_status == "SUCCEEDED":
            break
        elif job_status == "QUEUED" or "RUNNING":
            time.sleep(20)
            continue
        else:
            module.fail_json(msg='The Rubrik job failed.')

    results['response'] = response_body

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule # isort:skip
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_job_status  # isort:skip


if __name__ == "__main__":
    main()
