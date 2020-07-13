from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
import ansible_collections.rubrikinc.cdm.plugins.modules.rubrik_add_organization_protectable_object_mssql_server_host as rubrik_add_organization_protectable_object_mssql_server_host


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
            rubrik_add_organization_protectable_object_mssql_server_host.main()

    # @patch.object(rubrik_add_organization_protectable_object_mssql_server_host.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    # @patch.object(rubrik_add_organization_protectable_object_mssql_server_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    # def test_module_configure_rubrik_add_organization_protectable_object_mssql_server_host(self, mock_get, mock_post):

    #     def mock_get_v1_fileset_template():
    #         return {
    #             "hasMore": True,
    #             "data": [],
    #             "total": 1
    #         }

    #     def mock_post_v1_fileset_template_bulk():
    #         return {
    #             "allowBackupNetworkMounts": True,
    #             "allowBackupHiddenFoldersInNetworkMounts": True,
    #             "useWindowsVss": True,
    #             "name": "string",
    #             "includes": [
    #                 "string"
    #             ],
    #             "excludes": [
    #                 "string"
    #             ],
    #             "exceptions": [
    #                 "string"
    #             ],
    #             "operatingSystemType": "UnixLike",
    #             "shareType": "NFS",
    #             "preBackupScript": "string",
    #             "postBackupScript": "string",
    #             "backupScriptTimeout": 0,
    #             "backupScriptErrorHandling": "string",
    #             "isArrayEnabled": True,
    #             "id": "string",
    #             "primaryClusterId": "string",
    #             "isArchived": True,
    #             "hostCount": 0,
    #             "shareCount": 0
    #         }

    #     set_module_args({
    #         'node_ip': '1.1.1.1',
    #         'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
    #         'fileset_name': 'name',
    #         'share_type': 'NFS',
    #         'include': ["includes"],
    #         'exclude': ['excludes'],
    #         'exclude_exception': ["exceptions"],
    #         'follow_network_shares': True
    #     })

    #     mock_get.return_value = mock_get_v1_fileset_template()

    #     mock_post.return_value = mock_post_v1_fileset_template_bulk()

    #     with self.assertRaises(AnsibleExitJson) as result:
    #         rubrik_add_organization_protectable_object_mssql_server_host.main()

    #     self.assertEqual(result.exception.args[0]['changed'], True)
    #     self.assertEqual(result.exception.args[0]['response'], mock_post_v1_fileset_template_bulk())

    @patch.object(rubrik_add_organization_protectable_object_mssql_server_host.rubrik_cdm.rubrik_cdm.Connect, 'object_id', autospec=True, spec_set=True)
    @patch.object(rubrik_add_organization_protectable_object_mssql_server_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence(self, mock_get, mock_object_id):

        def mock_get_internal_organization_org_id_mssql():
            return {
                "hasMore": True,
                "data": [
                    {
                        "managedId": "host_id",
                        "objectType": "string",
                        "name": "string",
                        "primaryClusterId": "string",
                        "isDeleted": True,
                        "isRelic": True,
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "descendantCounts": {
                            "appBlueprint": 0,
                            "fileset": 0,
                            "shareFileset": 0,
                            "mssqlDatabase": 0,
                            "oracleDatabase": 0,
                            "storageArrayVolumeGroup": 0,
                            "vapp": 0,
                            "volumeGroup": 0,
                            "virtualMachine": 0
                        },
                        "locations": {
                            "folder": [
                                {
                                    "managedId": "string",
                                    "name": "string"
                                }
                            ],
                            "infrastructure": [
                                {
                                    "managedId": "string",
                                    "name": "string"
                                }
                            ],
                            "physical": [
                                {
                                    "managedId": "string",
                                    "name": "string"
                                }
                            ]
                        },
                        "properties": {
                            "hostname": "string",
                            "clusterName": "string",
                            "operatingSystem": "string",
                            "operatingSystemType": "string",
                            "instanceName": "string"
                        },
                        "isEffectiveSlaDomainRetentionLocked": True
                    }
                ],
                "total": 1
            }

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'organization_name': 'org_name',
            'mssql_host': 'mssql_host',
        })

        mock_get.return_value = mock_get_internal_organization_org_id_mssql()

        mock_object_id.side_effect = ["org_id", "ord_admin_role_id", "host_id"]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_add_organization_protectable_object_mssql_server_host.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The MSSQL host mssql_host is already assigned to the org_name organization.")
