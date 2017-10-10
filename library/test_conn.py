#!/usr/bin/python

import sys
import os
import json
import requests
import getopt
import base64
import traceback

import ansible.module_utils.pyRubrik as RubrikClient
from ansible.module_utils.basic import *

def main():
    requests.packages.urllib3.disable_warnings()

    module = AnsibleModule(
        argument_spec = dict(
            node = dict(required=True, type='str')
        )
    )

    debug_output = []

    try:
	    rk = RubrikClient.create(module.params['node'], module.params['rubrik_user'], module.params['rubrik_pass'])

    except:
        module.fail_json(msg="Rubrik node connection issues.  Please check Rubrik node IP address or hostname in the YAML configuration file.")

    module.exit_json(changed=False, debug_out=debug_output)

if __name__ == '__main__':
    main()
