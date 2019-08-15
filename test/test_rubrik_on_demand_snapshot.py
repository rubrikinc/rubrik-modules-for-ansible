import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_on_demand_snapshot as rubrik_on_demand_snapshot

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

def mock_get_v1_vmware_vm():
    return {
        "hasMore": True,
        "data": [
            {
                "id": "string",
                "name": "test-vm",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Derived",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "moid": "string",
                "vcenterId": "string",
                "hostName": "string",
                "hostId": "string",
                "clusterName": "string",
                "snapshotConsistencyMandate": "UNKNOWN",
                "powerStatus": "string",
                "protectionDate": "2019-05-05T18:57:06.133Z",
                "ipAddress": "string",
                "agentStatus": {
                    "agentStatus": "string",
                    "disconnectReason": "string"
                },
                "toolsInstalled": True,
                "guestOsName": "string",
                "isReplicationEnabled": True,
                "folderPath": [
                    {
                        "id": "string",
                        "managedId": "string",
                        "name": "string"
                    }
                ],
                "infraPath": [
                    {
                        "id": "string",
                        "managedId": "string",
                        "name": "string"
                    }
                ],
                "vmwareToolsInstalled": True,
                "isRelic": True,
                "guestCredentialAuthorizationStatus": "string",
                "cloudInstantiationSpec": {
                    "imageRetentionInSeconds": 0
                },
                "parentAppInfo": {
                    "id": "string",
                    "isProtectedThruHierarchy": True
                }
            }
        ],
        "total": 1
    }

def mock_get_v1_vmware_vm_id():
    return {
        "maxNestedVsphereSnapshots": 0,
        "isVmPaused": True,
        "configuredSlaDomainId": "string",
        "snapshotConsistencyMandate": "UNKNOWN",
        "preBackupScript": {
            "scriptPath": "string",
            "timeoutMs": 0,
            "failureHandling": "abort"
        },
        "postSnapScript": {
            "scriptPath": "string",
            "timeoutMs": 0,
            "failureHandling": "abort"
        },
        "postBackupScript": {
            "scriptPath": "string",
            "timeoutMs": 0,
            "failureHandling": "abort"
        },
        "isArrayIntegrationEnabled": True,
        "cloudInstantiationSpec": {
            "imageRetentionInSeconds": 0
        },
        "throttlingSettings": {
            "ioLatencyThreshold": 0,
            "datastoreIoLatencyThreshold": 0,
            "cpuUtilizationThreshold": 0
        },
        "id": "string",
        "name": "string",
        "configuredSlaDomainName": "string",
        "primaryClusterId": "string",
        "slaAssignment": "Derived",
        "effectiveSlaDomainId": "string",
        "effectiveSlaDomainName": "string",
        "effectiveSlaDomainPolarisManagedId": "string",
        "effectiveSlaSourceObjectId": "string",
        "effectiveSlaSourceObjectName": "string",
        "moid": "string",
        "vcenterId": "string",
        "hostName": "string",
        "hostId": "string",
        "clusterName": "string",
        "powerStatus": "string",
        "protectionDate": "2019-05-05T18:57:06.257Z",
        "ipAddress": "string",
        "agentStatus": {
            "agentStatus": "string",
            "disconnectReason": "string"
        },
        "toolsInstalled": True,
        "guestOsName": "string",
        "isReplicationEnabled": True,
        "folderPath": [
            {
                "id": "string",
                "managedId": "string",
                "name": "string"
            }
        ],
        "infraPath": [
            {
                "id": "string",
                "managedId": "string",
                "name": "string"
            }
        ],
        "vmwareToolsInstalled": True,
        "isRelic": True,
        "guestCredentialAuthorizationStatus": "string",
        "parentAppInfo": {
            "id": "string",
            "isProtectedThruHierarchy": True
        },
        "blackoutWindowStatus": {
            "isGlobalBlackoutActive": True,
            "isSnappableBlackoutActive": True
        },
        "blackoutWindows": {
            "globalBlackoutWindows": [
                {
                    "startTime": "string",
                    "endTime": "string"
                }
            ],
            "snappableBlackoutWindows": [
                {
                    "startTime": "string",
                    "endTime": "string"
                }
            ]
        },
        "effectiveSlaDomain": {
            "id": "string",
            "primaryClusterId": "string",
            "name": "string",
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
        },
        "currentHost": {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "datacenterId": "string",
            "computeClusterId": "string",
            "datastores": [
                {
                    "id": "string",
                    "name": "string",
                    "capacity": 0,
                    "dataStoreType": "string",
                    "dataCenterName": "string",
                    "isLocal": True
                }
            ],
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "effectiveSlaDomainPolarisManagedId": "string"
        },
        "virtualDiskIds": [
            "string"
        ],
        "snapshots": [
            {
                "id": "string",
                "date": "2019-05-05T18:57:06.257Z",
                "expirationDate": "2019-05-05T18:57:06.257Z",
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
                "vmName": "string"
            }
        ],
        "snapshotCount": 0,
        "physicalStorage": 0,
        "guestOsType": "Linux",
        "isArrayIntegrationPossible": True,
        "guestCredential": {
            "username": "string"
        },
        "isAgentRegistered": True
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

def mock_post_v1_vmware_vm_id_snapshot():
    return {
        "id": "string",
        "status": "string",
        "progress": 0,
        "startTime": "2019-05-05T18:57:06.298Z",
        "endTime": "2019-05-05T18:57:06.298Z",
        "nodeId": "string",
        "error": {
            "message": "string"
        },
        "links": [
            {
                "href": "href_string",
                "rel": "string"
            }
        ]
    }

def mock_get_internal_nutanix_vm():
    return {
        "hasMore": True,
        "data": [
            {
                "id": "string",
                "name": "test-vm",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "slaAssignment": "Derived",
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "Gold",
                "effectiveSlaDomainPolarisManagedId": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "nutanixClusterId": "string",
                "nutanixClusterName": "string",
                "isRelic": True,
                "snapshotConsistencyMandate": "Automatic",
                "agentStatus": {
                    "agentStatus": "string",
                    "disconnectReason": "string"
                },
                "operatingSystemType": "AIX"
            }
        ],
        "total": 1
    }

def mock_get_internal_nutanix_vm_id():
    return {
        "configuredSlaDomainId": "string",
        "isPaused": True,
        "snapshotConsistencyMandate": "Automatic",
        "excludedDiskIds": [
            "string"
        ],
        "id": "string",
        "name": "string",
        "configuredSlaDomainName": "string",
        "primaryClusterId": "string",
        "slaAssignment": "Derived",
        "effectiveSlaDomainId": "string",
        "effectiveSlaDomainName": "Gold",
        "effectiveSlaDomainPolarisManagedId": "string",
        "effectiveSlaSourceObjectId": "string",
        "effectiveSlaSourceObjectName": "string",
        "nutanixClusterId": "string",
        "nutanixClusterName": "string",
        "isRelic": True,
        "agentStatus": {
            "agentStatus": "string",
            "disconnectReason": "string"
        },
        "operatingSystemType": "AIX",
        "blackoutWindowStatus": {
            "isGlobalBlackoutActive": True,
            "isSnappableBlackoutActive": True
        },
        "blackoutWindows": {
            "globalBlackoutWindows": [
                {
                    "startTime": "string",
                    "endTime": "string"
                }
            ],
            "snappableBlackoutWindows": [
                {
                    "startTime": "string",
                    "endTime": "string"
                }
            ]
        },
        "isAgentRegistered": True
    }

def mock_post_internal_nutanix_vm_id_snapshot():
    return {
        "id": "string",
        "status": "string",
        "progress": 0,
        "startTime": "2019-05-05T19:20:22.137Z",
        "endTime": "2019-05-05T19:20:22.137Z",
        "nodeId": "string",
        "error": {
            "message": "string"
        },
        "links": [
            {
                "href": "href_string",
                "rel": "string"
            }
        ]
    }

def mock_get_v1_host():
    return {
        "hasMore": True,
        "data": [
            {
                "id": "string",
                "name": "test-host",
                "hostname": "string",
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

def mock_get_no_fileset():
    return {
        "hasMore": True,
        "data": [],
        "total": 0
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
                "effectiveSlaDomainName": "Gold",
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

def mock_post_v1_fileset_id_snapshot():
    return {
        "id": "string",
        "status": "string",
        "progress": 0,
        "startTime": "2019-05-05T18:57:06.003Z",
        "endTime": "2019-05-05T18:57:06.003Z",
        "nodeId": "string",
        "error": {
            "message": "string"
        },
        "links": [
            {
                "href": "href_string",
                "rel": "string"
            }
        ]
    }

class TestRubrikOnDemandSnapshot(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_on_demand_snapshot.main()

    def test_module_fail_with_incorrect_object_type(self):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'foo',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })
        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_on_demand_snapshot.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "value of object_type must be one of: vmware, physical_host, ahv, got: foo")

    def test_module_fail_with_incorrect_host_os(self):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'host_os': 'foo',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })
        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_on_demand_snapshot.main()    

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "value of host_os must be one of: None, Linux, Windows, got: foo")

    def test_module_fail_with_physical_host_host_os_not_populated(self):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'physical_host',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })
        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_on_demand_snapshot.main()    

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "The on_demand_snapshot() `host_os` argument must be populated when taking a Physical host snapshot.")
    
    def test_module_fail_with_physical_host_host_fileset_not_populated(self):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'physical_host',
            'host_os': 'Linux',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })
        with self.assertRaises(AnsibleFailJson)  as result:
            rubrik_on_demand_snapshot.main()    

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "The on_demand_snapshot() `fileset` argument must be populated when taking a Physical host snapshot.")

    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_vmware_current_sla(self, mock_get, mock_post):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'current',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        mock_post.return_value = mock_post_v1_vmware_vm_id_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_on_demand_snapshot.main()
        
        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['job_status_url'], 'href_string')


    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_vmware_specific_sla(self, mock_get, mock_post):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_sla_domain()]

        mock_post.return_value = mock_post_v1_vmware_vm_id_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_on_demand_snapshot.main()
        
        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['job_status_url'], 'href_string')

    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_ahv_current_sla(self, mock_get, mock_post):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'ahv',
            'sla_name': 'current',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_nutanix_vm(), mock_get_internal_nutanix_vm_id()]

        mock_post.return_value = mock_post_internal_nutanix_vm_id_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_on_demand_snapshot.main()
        
        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['job_status_url'], 'href_string')

    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_ahv_specific_sla(self, mock_get, mock_post):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'ahv',
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_internal_nutanix_vm(), mock_get_v1_sla_domain()]

        mock_post.return_value = mock_post_internal_nutanix_vm_id_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_on_demand_snapshot.main()
        
        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['job_status_url'], 'href_string')

    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Cluster, 'cluster_version', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_fail_with_physical_host_invalid_fileset(self, mock_get, mock_cluster_version):
        set_module_args({
            'object_name': 'test-host',
            'object_type': 'physical_host',
            'host_os': 'Linux',
            'fileset': 'fileset',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_cluster_version.return_value = "5.0"

        mock_get.side_effect = [
            mock_get_v1_host(),
            mock_get_v1_fileset_template(),
            mock_get_no_fileset()]

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_on_demand_snapshot.main()
        
        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "The Physical Host 'test-host' is not assigned to the 'fileset' Fileset.")

    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Cluster, 'cluster_version', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_on_demand_snapshot.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_physical_host_current_sla(self, mock_get, mock_post, mock_cluster_version):
        set_module_args({
            'object_name': 'test-host',
            'object_type': 'physical_host',
            'host_os': 'Linux',
            'fileset': 'fileset',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_cluster_version.return_value = "5.0"

        mock_get.side_effect = [
            mock_get_v1_host(),
            mock_get_v1_fileset_template(),
            mock_get_v1_fileset()]

        mock_post.return_value = mock_post_v1_fileset_id_snapshot()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_on_demand_snapshot.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_fileset_id_snapshot())
        self.assertEqual(result.exception.args[0]['job_status_url'], 'href_string')

if __name__ == '__main__':
    unittest.main()
