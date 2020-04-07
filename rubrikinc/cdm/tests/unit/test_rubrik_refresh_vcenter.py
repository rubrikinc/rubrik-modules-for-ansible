from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from rubrik_cdm.exceptions import RubrikException, APICallException
import ansible_collections.rubrikinc.cdm.plugins.modules.rubrik_refresh_vcenter as rubrik_refresh_vcenter


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
            rubrik_refresh_vcenter.main()

    def test_module_fail_with_invalid_wait_for_completion(self):

        vcenter_ip = "vcenter.example.com"
        wait_for_completion = "foo"

        set_module_args({
            'vcenter_ip': vcenter_ip,
            'wait_for_completion': wait_for_completion,
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_refresh_vcenter.main()

        self.assertEqual(result.exception.args[0]['failed'], True)

    @patch.object(rubrik_refresh_vcenter.rubrik_cdm.rubrik_cdm.Cluster, 'refresh_vcenter', autospec=True, spec_set=True)
    def test_module_get_refresh_vcenter(self, mock_refresh):

        def mock_refresh_vcenter():
            return {
                "endTime": "2020-04-07T00:30:28.448Z",
                "id": "REFRESH_METADATA_01234567-8910-1abc-d435-0abc1234d567_01234567-8910-1abc-d435-0abc1234d567:::0",
                "links": [
                    {
                        "href": "https://cluster-b-rr.rubrik.us/api/v1/vmware/vcenter/request/REFRESH_METADATA_01234567-8910-1abc-d435-0abc1234d567_01234567-8910-1abc-d435-0abc1234d567:::0",
                        "rel": "self"
                    }
                ],
                "nodeId": "cluster:::RVM111S000000",
                "startTime": "2020-04-07T00:29:50.585Z",
                "status": "SUCCEEDED"
            }

        set_module_args({
            'vcenter_ip': 'vcenter.example.com',
            'wait_for_completion': True,
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_refresh.return_value = mock_refresh_vcenter()
        
        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_refresh_vcenter.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], mock_refresh_vcenter())