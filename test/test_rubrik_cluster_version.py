import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_cluster_version as rubrik_cluster_version


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


class TestRubrikClusterVersion(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_cluster_version.main()

    @patch.object(rubrik_cluster_version.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_cluster_version(self, mock_get):

        def mock_get_v1_cluster_me_version():
            return {'version': '5.0.1-1280'}

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.return_value = mock_get_v1_cluster_me_version()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_cluster_version.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['version'], '5.0.1-1280')
