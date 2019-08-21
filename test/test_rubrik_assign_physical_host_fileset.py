import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_assign_physical_host_fileset as rubrik_assign_physical_host_fileset


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


def mock_get_no_host():
    return {
        "hasMore": True,
        "data": [],
        "total": 0
    }


def mock_get_no_fileset_template():
    return {
        "hasMore": True,
        "data": [],
        "total": 0
    }


def mock_get_no_fileset():
    return {
        "hasMore": True,
        "data": [],
        "total": 0
    }


def mock_get_v1_host():
    return {
        "hasMore": True,
        "data": [
            {
                "id": "string",
                "name": "string",
                "hostname": "hostname",
                "primaryClusterId": "string",
                "operatingSystem": "string",
                "operatingSystemType": "string",
                "status": "string",
                "nasBaseConfig": {
                    "vendorType": "string",
                    "apiUsername": "string",
                    "apiCertificate": "string",
                    "apiHostname": "string",
                    "apiEndpoint": "string",
                    "zoneName": "string"
                },
                "mssqlCbtEnabled": "Enabled",
                "mssqlCbtEffectiveStatus": "On",
                "organizationId": "string",
                "organizationName": "string"
            }
        ],
        "total": 1
    }


def mock_get_v1_fileset_template():
    return {
        "hasMore": True,
        "data": [
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "fileset",
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
        ],
        "total": 1
    }


def mock_get_multiple_fileset_templates():
    return {
        "hasMore": True,
        "data": [
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "fileset",
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
            },
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "fileset",
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
        ],
        "total": 2
    }


def mock_get_multiple_matching_fileset_templates():
    return {
        "hasMore": True,
        "data": [
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "fileset",
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
            },
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "name": "fileset",
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
        ],
        "total": 2
    }


def mock_get_v1_sla_domain():
    return {
        "hasMore": True,
        "data": [
            {
                "id": "string_sla_id",
                "primaryClusterId": "string",
                "name": "gold",
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


def mock_get_existing_fileset():
    return {
        "hasMore": True,
        "data": [
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "id": "string",
                "name": "string",
                "configuredSlaDomainId": "string_sla_id",
                "configuredSlaDomainName": "gold",
                "primaryClusterId": "string",
                "hostId": "string",
                "shareId": "string",
                "hostName": "string",
                "templateId": "string",
                "templateName": "string",
                "operatingSystemType": "string",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "includes": [
                    "string"
                ],
                "excludes": [
                    "string"
                ],
                "exceptions": [
                    "string"
                ],
                "isRelic": True,
                "arraySpec": {
                    "proxyHostId": "string"
                },
                "isPassthrough": True
            }
        ],
        "total": 1
    }


def mock_get_v1_fileset():
    return {
        "hasMore": True,
        "data": [
            {
                "allowBackupNetworkMounts": True,
                "allowBackupHiddenFoldersInNetworkMounts": True,
                "useWindowsVss": True,
                "id": "string",
                "name": "fileset",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "hostId": "string",
                "shareId": "string",
                "hostName": "string",
                "templateId": "string",
                "templateName": "string",
                "operatingSystemType": "string",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "includes": [
                    "string"
                ],
                "excludes": [
                    "string"
                ],
                "exceptions": [
                    "string"
                ],
                "isRelic": True,
                "arraySpec": {
                    "proxyHostId": "string"
                },
                "isPassthrough": True
            }
        ],
        "total": 1
    }


def mock_patch_v1_fileset():
    return {
        "configuredSlaDomainId": "string",
        "allowBackupNetworkMounts": True,
        "allowBackupHiddenFoldersInNetworkMounts": True,
        "useWindowsVss": True,
        "id": "string",
        "name": "fileset",
        "configuredSlaDomainName": "string",
        "primaryClusterId": "string",
        "hostId": "string",
        "shareId": "string",
        "hostName": "hostname",
        "templateId": "string",
        "templateName": "string",
        "operatingSystemType": "string",
        "effectiveSlaDomainId": "string",
        "effectiveSlaDomainName": "string",
        "effectiveSlaDomainPolarisManagedId": "string",
        "includes": [
            "string"
        ],
        "excludes": [
            "string"
        ],
        "exceptions": [
            "string"
        ],
        "isRelic": True,
        "arraySpec": {
            "proxyHostId": "string"
        },
        "isPassthrough": True,
        "protectionDate": "2019-05-23T15:36:06.889Z",
        "snapshotCount": 0,
        "archivedSnapshotCount": 0,
        "snapshots": [
            {
                "id": "string",
                "date": "2019-05-23T15:36:06.889Z",
                "expirationDate": "2019-05-23T15:36:06.889Z",
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
                "filesetName": "fileset",
                "fileCount": 0
            }
        ],
        "localStorage": 0,
        "archiveStorage": 0,
        "preBackupScript": "string",
        "postBackupScript": "string",
        "backupScriptTimeout": 0,
        "backupScriptErrorHandling": "string"
    }


def mock_post_v1_fileset():
    return {
        "configuredSlaDomainId": "string",
        "allowBackupNetworkMounts": True,
        "allowBackupHiddenFoldersInNetworkMounts": True,
        "useWindowsVss": True,
        "id": "string",
        "name": "string",
        "configuredSlaDomainName": "string",
        "primaryClusterId": "string",
        "hostId": "string",
        "shareId": "string",
        "hostName": "hostname",
        "templateId": "string",
        "templateName": "string",
        "operatingSystemType": "string",
        "effectiveSlaDomainId": "string",
        "effectiveSlaDomainName": "string",
        "effectiveSlaDomainPolarisManagedId": "string",
        "includes": [
            "string"
        ],
        "excludes": [
            "string"
        ],
        "exceptions": [
            "string"
        ],
        "isRelic": True,
        "arraySpec": {
            "proxyHostId": "string"
        },
        "isPassthrough": True,
        "protectionDate": "2019-05-23T15:36:06.821Z",
        "snapshotCount": 0,
        "archivedSnapshotCount": 0,
        "snapshots": [
            {
                "id": "string",
                "date": "2019-05-23T15:36:06.821Z",
                "expirationDate": "2019-05-23T15:36:06.821Z",
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
                "filesetName": "string",
                "fileCount": 0
            }
        ],
        "localStorage": 0,
        "archiveStorage": 0,
        "preBackupScript": "string",
        "postBackupScript": "string",
        "backupScriptTimeout": 0,
        "backupScriptErrorHandling": "string"
    }


class TestRubrikAssignPhysicalHostFileset(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_operating_system(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'osx'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_host_follow_network_shares(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'follow_network_shares': 'Yes'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_backup_hidden_folders(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'backup_hidden_folders': 'Yes'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_include(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'include': 'invalid_include'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_exclude(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'exclude': 'invalid_include'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    def test_module_fail_with_invalid_exclude_exception(self):
        set_module_args({
            'hostname': 'test-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'exclude_exception': 'invalid_include_exception'
        })
        with self.assertRaises(AnsibleFailJson):
            rubrik_assign_physical_host_fileset.main()

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_fail_with_invalid_hostname(self, mock_get):
        set_module_args({
            'hostname': 'invalid-host',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.return_value = mock_get_no_host()

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Rubrik cluster is not connected to a Linux physical host named 'invalid-host'.")

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_fail_with_invalid_fileset_name(self, mock_get):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'invalid-fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_host(), mock_get_no_fileset_template()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Rubrik cluster does not have a Linux Fileset named 'invalid-fileset'.")

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_fail_with_invalid_fileset_name_multiple_matches_not_specific(self, mock_get):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_host(), mock_get_multiple_fileset_templates()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Rubrik cluster contains multiple Linux Filesets named 'fileset'. Please populate all function arguments to find a more specific match.")

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_fail_with_invalid_fileset_name_multiple_matches_specific(self, mock_get):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'include': [""],
            'exclude': ["", True, True],
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_host(), mock_get_multiple_matching_fileset_templates()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "The Rubrik cluster contains multiple Linux Filesets named 'fileset' that match all of the populate function arguments. Please use a unique Fileset.")

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'patch', autospec=True, spec_set=True)
    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_assign_physical_host_fileset_patch_sla(self, mock_get, mock_patch):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [
            mock_get_v1_host(),
            mock_get_v1_fileset_template(),
            mock_get_v1_sla_domain(),
            mock_get_v1_fileset()]

        mock_patch.return_value = mock_patch_v1_fileset()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response']['hostName'], "hostname")

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_assign_physical_host_fileset_idempotence(self, mock_get):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [
            mock_get_v1_host(),
            mock_get_v1_fileset_template(),
            mock_get_v1_sla_domain(),
            mock_get_existing_fileset()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['changed'], False)

    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'patch', autospec=True, spec_set=True)
    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'post', autospec=True, spec_set=True)
    @patch.object(rubrik_assign_physical_host_fileset.rubrik_cdm.rubrik_cdm.Connect,
                  'get', autospec=True, spec_set=True)
    def test_module_assign_physical_host_no_current_fileset(self, mock_get, mock_post, mock_patch):
        set_module_args({
            'hostname': 'hostname',
            'fileset_name': 'fileset',
            'sla_name': 'gold',
            'operating_system': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [
            mock_get_v1_host(),
            mock_get_v1_fileset_template(),
            mock_get_v1_sla_domain(),
            mock_get_no_fileset()]

        mock_post.return_value = mock_post_v1_fileset()

        mock_patch.return_value = mock_patch_v1_fileset()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_physical_host_fileset.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'][0], mock_post_v1_fileset())
        self.assertEqual(result.exception.args[0]['response'][1], mock_patch_v1_fileset())


if __name__ == '__main__':
    unittest.main()
