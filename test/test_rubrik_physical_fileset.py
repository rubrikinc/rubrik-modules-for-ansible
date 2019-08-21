import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_physical_fileset as rubrik_physical_fileset


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


class TestRubrikNASFileset(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_physical_fileset.main()

    @patch.object(rubrik_physical_fileset.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_physical_fileset.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_physical_fileset(self, mock_get, mock_post):

        def mock_get_v1_fileset_template():
            return {
                "hasMore": True,
                "data": [],
                "total": 1
            }

        def mock_post_v1_fileset_template_bulk():
            return {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "string",
                "includes": [
                    "string"
                ],
                "excludes": [
                    "string"
                ],
                "exceptions": [
                    "string"
                ],
                "operatingSystemType": "UnixLike",
                "shareType": "NFS",
                "preBackupScript": "string",
                "postBackupScript": "string",
                "backupScriptTimeout": 0,
                "backupScriptErrorHandling": "string",
                "isArrayEnabled": True,
                "id": "string",
                "primaryClusterId": "string",
                "isArchived": True,
                "hostCount": 0,
                "shareCount": 0
            }

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'fileset_name': 'name',
            'operating_system': 'Linux',
            'include': ["includes"],
            'exclude': ['excludes'],
            'exclude_exception': ["exceptions"],
            'follow_network_shares': True,
            'backup_hidden_folders': True
        })

        mock_get.return_value = mock_get_v1_fileset_template()

        mock_post.return_value = mock_post_v1_fileset_template_bulk()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_fileset.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_fileset_template_bulk())

    @patch.object(rubrik_physical_fileset.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence(self, mock_get):

        def mock_get_v1_fileset_template():
            return {
                "hasMore": True,
                "data": [
                    {
                        "allowBackupNetworkMounts": True,
                        "allowBackupHiddenFoldersInNetworkMounts": True,
                        "useWindowsVss": True,
                        "name": "name",
                        "includes": [
                            "includes"
                        ],
                        "excludes": [
                            "excludes"
                        ],
                        "exceptions": [
                            "exceptions"
                        ],
                        "operatingSystemType": "Linux",
                        "shareType": "NFS",
                        "preBackupScript": "string",
                        "postBackupScript": "string",
                        "backupScriptTimeout": 0,
                        "backupScriptErrorHandling": "string",
                        "isArrayEnabled": True,
                        "id": "string",
                        "primaryClusterId": "string",
                        "isArchived": True,
                        "hostCount": 0,
                        "shareCount": 0
                    }
                ],
                "total": 1
            }

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'fileset_name': 'name',
            'operating_system': 'Linux',
            'include': ["includes"],
            'exclude': ['excludes'],
            'exclude_exception': ["exceptions"],
            'follow_network_shares': True,
            'backup_hidden_folders': True
        })

        mock_get.return_value = mock_get_v1_fileset_template()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_fileset.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'], "No change required. The Rubrik cluster already has a Linux Fileset named 'name' configured with the provided variables.")
