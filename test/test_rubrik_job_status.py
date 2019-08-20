import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from rubrik_cdm.exceptions import RubrikException, APICallException
import library.rubrik_job_status as rubrik_job_status

def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)

class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

class TestRubrikJobStatus(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_job_status.main()

    def test_module_fail_with_invalid_wait_for_completion(self):

        set_module_args({
            'url': 'https://1.1.1.1/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0',
            'wait_for_completion': 'foo',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_job_status.main()
        
        self.assertEqual(result.exception.args[0]['failed'], True)

    @patch.object(rubrik_job_status.rubrik_cdm.rubrik_cdm.Connect, '_common_api', autospec=True, spec_set=True)
    def test_module_get_job_status(self, mock_common_api):

        def mock_job_status():
            return {
                "id": "CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0",
                "status": "SUCCEEDED",
                "startTime": "2019-04-17T21:31:17.785Z",
                "endTime": "2019-04-17T21:31:39.056Z",
                "nodeId": "cluster:::RVM189S019012",
                "links": [
                    {
                        "href": "CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0",
                        "rel": "self"
                    }
                ]
            }

        set_module_args({
            'url': 'https://1.1.1.1/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_common_api.return_value = mock_job_status()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_job_status.main()
        
        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], mock_job_status())