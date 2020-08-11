from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
import ansible_collections.rubrikinc.cdm.plugins.modules.rubrik_replication_private as rubrik_replication_private


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


class TestRubrikReplicationPrivate(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_replication_private.main()

    @patch.object(rubrik_replication_private.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_replication_private.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_replication_private(self, mock_get, mock_post):

        def mock_get_internal_cluster_me_replication_private():
            return {}

        def mock_post_internal_cluster_me_replication_private():
            return {
                "id": "DataLocation:::123ad456-a123-456b-789c-50a4387f2860",
                "replicationSetup": "Private Network",
                "targetClusterAddress": "10.10.10.10",
                "targetClusterName": "REPLCLUSTER",
                "targetClusterUuid": "123ad456-a123-456b-789c-50a4387f2860"
            }

        set_module_args({
            'target_username': 'admin',
            'target_password': 'Rubrik',
            'target_cluster_address': '10.10.10.10',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.return_value = mock_get_internal_cluster_me_replication_private()

        mock_post.return_value = mock_post_internal_cluster_me_replication_private()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_replication_private.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response']['targetClusterName'], 'REPLCLUSTER')
