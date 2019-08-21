import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_managed_volume as rubrik_managed_volume


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


class TestRubrikManagedVolume(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_managed_volume.main()

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_begin_snapshot_idempotence(self, mock_get):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": True,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "string",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Derived",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": True,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'begin',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The Managed Volume 'test_mv' is already assigned in a writeable state.")

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_begin_snapshot(self, mock_get, mock_post):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": True,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "string",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Derived",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": False,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        def mock_post_internal_managed_volume_id_begin_snapshot():
            return {
                "snapshotId": "string",
                "ownerId": "string"
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'begin',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_internal_managed_volume_id_begin_snapshot())

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_end_snapshot_idempotence(self, mock_get):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": True,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "test_mv",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Derived",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": False,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'end',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The Managed Volume 'test_mv' is already assigned in a read only state.")

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_fail_when_end_mv_snapshot_invalid_current_sla(self, mock_get):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": False,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "test_mv",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Unassigned",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": True,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'end',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Managed Volume 'test_mv' does not have a SLA assigned currently assigned. You must populate the sla_name argument.")

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_fail_when_end_mv_snapshot_current_sla_unprotected(self, mock_get):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": False,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "test_mv",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "string",
                "effectiveSlaDomainId": "UNPROTECTED",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": True,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'end',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Managed Volume 'test_mv' does not have a SLA assigned currently assigned. You must populate the sla_name argument.")

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_end_mv_snapshot_current_sla(self, mock_get, mock_post):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": False,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "test_mv",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "string",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": True,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        def mock_post_internal_managed_volume_id_begin_snapshot():
            return {
                "id": "string",
                "date": "2019-05-07T00:59:46.025Z",
                "expirationDate": "2019-05-07T00:59:46.025Z",
                "sourceObjectType": "string",
                "isOnDemandSnapshot": True,
                "cloudState": 0,
                "consistencyLevel": "string",
                "indexState": 0,
                "replicationLocationIds": [
                    "string"
                ],
                "archivalLocationIds": [
                    "string"
                ],
                "slaId": "string",
                "slaName": "string",
                "links": {
                    "exportLink": {
                        "href": "string",
                        "rel": "string"
                    },
                    "self": {
                        "href": "string",
                        "rel": "string"
                    }
                }
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'end',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

        mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_internal_managed_volume_id_begin_snapshot())

    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_managed_volume.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_end_mv_snapshot_specific_sla(self, mock_get, mock_post):

        def mock_get_internal_managed_volume():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test_mv",
                        "configuredSlaDomainId": "string",
                        "configuredSlaDomainName": "string",
                        "primaryClusterId": "string",
                        "slaAssignment": "Derived",
                        "effectiveSlaDomainId": "string",
                        "effectiveSlaDomainName": "string",
                        "effectiveSlaDomainPolarisManagedId": "string",
                        "effectiveSlaSourceObjectId": "string",
                        "effectiveSlaSourceObjectName": "string",
                        "snapshotCount": 0,
                        "pendingSnapshotCount": 0,
                        "isRelic": True,
                        "applicationTag": "Oracle",
                        "numChannels": 0,
                        "volumeSize": 0,
                        "usedSize": 0,
                        "state": "ExportRequested",
                        "hostPatterns": [
                            "string"
                        ],
                        "mainExport": {
                            "isActive": True,
                            "channels": [
                                {
                                    "ipAddress": "string",
                                    "mountPoint": "string"
                                }
                            ],
                            "config": {
                                "hostPatterns": [
                                    "string"
                                ],
                                "nodeHint": [
                                    "string"
                                ],
                                "smbDomainName": "string",
                                "smbValidUsers": [
                                    "string"
                                ],
                                "smbValidIps": [
                                    "string"
                                ],
                                "subnet": "string",
                                "shareType": "NFS"
                            }
                        },
                        "isWritable": False,
                        "links": [
                            {
                                "href": "string",
                                "rel": "string"
                            }
                        ],
                        "isDeleted": True,
                        "shareType": "NFS",
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ]
                    }
                ],
                "total": 1
            }

        def mock_get_internal_managed_volume_id():
            return {
                "id": "string",
                "name": "test_mv",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "string",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "snapshotCount": 0,
                "pendingSnapshotCount": 0,
                "isRelic": True,
                "applicationTag": "Oracle",
                "numChannels": 0,
                "volumeSize": 0,
                "usedSize": 0,
                "state": "ExportRequested",
                "hostPatterns": [
                    "string"
                ],
                "mainExport": {
                    "isActive": True,
                    "channels": [
                        {
                            "ipAddress": "string",
                            "mountPoint": "string"
                        }
                    ],
                    "config": {
                        "hostPatterns": [
                            "string"
                        ],
                        "nodeHint": [
                            "string"
                        ],
                        "smbDomainName": "string",
                        "smbValidUsers": [
                            "string"
                        ],
                        "smbValidIps": [
                            "string"
                        ],
                        "subnet": "string",
                        "shareType": "NFS"
                    }
                },
                "isWritable": True,
                "links": [
                    {
                        "href": "string",
                        "rel": "string"
                    }
                ],
                "isDeleted": True,
                "shareType": "NFS",
                "smbDomainName": "string",
                "smbValidUsers": [
                    "string"
                ],
                "smbValidIps": [
                    "string"
                ]
            }

        def mock_get_v1_sla_domain():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "primaryClusterId": "string",
                        "name": "Gold",
                        "frequencies": [
                            {
                                "timeUnit": "string",
                                "frequency": 0,
                                "retention": 0
                            }
                        ],
                        "allowedBackupWindows": [
                            {
                                "startTimeAttributes": {
                                    "minutes": 0,
                                    "hour": 0,
                                    "dayOfWeek": 0
                                },
                                "durationInHours": 0
                            }
                        ],
                        "firstFullAllowedBackupWindows": [
                            {
                                "startTimeAttributes": {
                                    "minutes": 0,
                                    "hour": 0,
                                    "dayOfWeek": 0
                                },
                                "durationInHours": 0
                            }
                        ],
                        "localRetentionLimit": 0,
                        "maxLocalRetentionLimit": 0,
                        "archivalSpecs": [
                            {
                                "locationId": "string",
                                "archivalThreshold": 0
                            }
                        ],
                        "replicationSpecs": [
                            {
                                "locationId": "string",
                                "retentionLimit": 0
                            }
                        ],
                        "numDbs": 0,
                        "numOracleDbs": 0,
                        "numFilesets": 0,
                        "numHypervVms": 0,
                        "numNutanixVms": 0,
                        "numManagedVolumes": 0,
                        "numStorageArrayVolumeGroups": 0,
                        "numWindowsVolumeGroups": 0,
                        "numLinuxHosts": 0,
                        "numShares": 0,
                        "numWindowsHosts": 0,
                        "numVms": 0,
                        "numEc2Instances": 0,
                        "numVcdVapps": 0,
                        "numProtectedObjects": 0,
                        "isDefault": True,
                        "uiColor": "string"
                    }
                ],
                "total": 1
            }

        def mock_post_internal_managed_volume_id_begin_snapshot():
            return {
                "id": "string",
                "date": "2019-05-07T00:59:46.025Z",
                "expirationDate": "2019-05-07T00:59:46.025Z",
                "sourceObjectType": "string",
                "isOnDemandSnapshot": True,
                "cloudState": 0,
                "consistencyLevel": "string",
                "indexState": 0,
                "replicationLocationIds": [
                    "string"
                ],
                "archivalLocationIds": [
                    "string"
                ],
                "slaId": "string",
                "slaName": "string",
                "links": {
                    "exportLink": {
                        "href": "string",
                        "rel": "string"
                    },
                    "self": {
                        "href": "string",
                        "rel": "string"
                    }
                }
            }

        set_module_args({
            'managed_volume_name': 'test_mv',
            'action': 'end',
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [
            mock_get_internal_managed_volume(),
            mock_get_internal_managed_volume_id(),
            mock_get_v1_sla_domain()]

        mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_managed_volume.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_internal_managed_volume_id_begin_snapshot())
