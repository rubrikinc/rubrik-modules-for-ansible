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
            node            = dict(required=True, type='str'),
            rubrik_user     = dict(required=True, type='str'),
            rubrik_pass     = dict(required=True, type='str', no_log=True),
            host_name       = dict(required=True, type='str')
        )
    )

    debug_output = []

    try:
        rk = RubrikClient.create(module.params['node'], module.params['rubrik_user'], module.params['rubrik_pass'])

    except:
        module.fail_json(msg="Rubrik node connection issues.  Please check Rubrik node IP address or hostname in the YAML configuration file.")

    '''Register the host'''
    rk.register_host(host={"hostname": module.params['host_name'], "hasAgent":True})

    module.exit_json(changed=True, debug_out=debug_output)

if __name__ == '__main__':
    main()
