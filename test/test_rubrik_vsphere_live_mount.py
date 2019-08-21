import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_vsphere_live_mount as rubrik_vsphere_live_mount


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


class TestRubrikVsphereLiveMount(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_vsphere_live_mount.main()

    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_vsphere_live_mount(self, mock_get, mock_post):

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "vm_name",
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

        def mock_post_v1_vmware_vm_snapshot_id_mount():
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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'vm_name': 'vm_name',
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_vsphere_live_mount.main()

        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_vmware_vm_snapshot_id_mount())

    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect,
                  '_date_time_conversion', autospec=True, spec_set=True)
    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_vsphere_live_specific_time(self, mock_get, mock__date_time_conversion, mock_post):

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "vm_name",
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
                        "date": "2014-01-15T09:30:06.257Z",
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

        def mock_post_v1_vmware_vm_snapshot_id_mount():
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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'vm_name': 'vm_name',
            'date': '1-15-2014',
            'time': '1:30 AM'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        mock__date_time_conversion.return_value = "2014-01-15T09:30"

        mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_vsphere_live_mount.main()

        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_vmware_vm_snapshot_id_mount())

    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect,
                  '_date_time_conversion', autospec=True, spec_set=True)
    @patch.object(rubrik_vsphere_live_mount.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_vsphere_live_mount_specific_host(
            self, mock_get, mock__date_time_conversion, mock_post):

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "vm_name",
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
                        "date": "2014-01-15T09:30:06.257Z",
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

        def mock_get_v1_vmware_host():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "host",
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
                    }
                ],
                "total": 1
            }

        def mock_post_v1_vmware_vm_snapshot_id_mount():
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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'vm_name': 'vm_name',
            'date': '1-15-2014',
            'time': '1:30 AM',
            'host': 'host'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id(), mock_get_v1_vmware_host()]

        mock__date_time_conversion.return_value = "2014-01-15T09:30"

        mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_vsphere_live_mount.main()

        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_vmware_vm_snapshot_id_mount())
