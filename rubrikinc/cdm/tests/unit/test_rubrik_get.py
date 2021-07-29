from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
import ansible_collections.rubrikinc.cdm.plugins.modules.rubrik_get as rubrik_get


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


class TestRubrikGet(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_get.main()

    @patch.object(rubrik_get.rubrik_cdm.rubrik_cdm.Connect, '_common_api', autospec=True, spec_set=True)
    def test_module_get(self, mock_get):

        def mock_get_get():
            return {"data": [], "hasMore": False, "total": 0}

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'api_version': 'v1',
            'api_endpoint': '/sla_domain',
            'params': {"name": "Python SDK"}
        })

        mock_get.return_value = mock_get_get()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_get.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], {"data": [], "hasMore": False, "total": 0})
    
    def test_v3_support(self, mock_get):

        def mock_get_get():
            return {"data": [], "hasMore": False, "total": 0}

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'api_version': 'v3',
            'api_endpoint': '/sla_domain',
            'params': {"name": "Python SDK"}
        })

        mock_get.return_value = mock_get_get()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_get.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], {"data": [], "hasMore": False, "total": 0})

if __name__ == '__main__':
    unittest.main()
