from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
import ansible_collections.rubrikinc.cdm.plugins.modules.rubrik_login_banner as rubrik_login_banner


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


class TestRubrikLoginBanner(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_login_banner.main()

    @patch.object(rubrik_login_banner.rubrik_cdm.rubrik_cdm.Connect, 'put', autospec=True, spec_set=True)
    @patch.object(rubrik_login_banner.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_login_banner(self, mock_get, mock_put):

        def mock_get_internal_cluster_me_login_banner():
            return {}

        def mock_put_internal_cluster_me_login_banner():
            return {'status_code': '200'}

        set_module_args({
            'banner_text': 'Banner Test',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.return_value = mock_get_internal_cluster_me_login_banner()

        mock_put.return_value = mock_put_internal_cluster_me_login_banner()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_login_banner.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response']['status_code'], '200')

    @patch.object(rubrik_login_banner.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence(self, mock_get):

        def mock_get_internal_cluster_me_login_banner():
            return {'loginBanner': 'Banner Test'}

        set_module_args({
            'banner_text': 'Banner Test',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.return_value = mock_get_internal_cluster_me_login_banner()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_login_banner.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            'No change required. The Rubrik cluster is already configured with I(banner_text) as it\'s banner.')
