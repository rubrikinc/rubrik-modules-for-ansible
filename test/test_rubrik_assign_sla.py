import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_assign_sla as rubrik_assign_sla


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


class TestRubrikAssignSla(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_assign_sla.main()

    def test_module_fail_with_incorrect_object_type(self):
        set_module_args({
            'object_name': 'test-vm',
            'object_type': "invalid-type",
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })
        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_assign_sla.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(
            result.exception.args[0]['msg'],
            "value of object_type must be one of: vmware, mssql_host, got: invalid-type")

    @patch.object(rubrik_assign_sla.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_specific_sla(self, mock_get):

        def mock_get_v1_sla_domain():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_sla_id",
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

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test-vm",
                        "configuredSlaDomainId": "string_sla_id",
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
                "configuredSlaDomainId": "string_sla_id",
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
                "name": "test-vm",
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
                "hostName": "test-vm",
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

        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_sla.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The vSphere VM 'test-vm' is already assigned to the 'Gold' SLA Domain.")

    @patch.object(rubrik_assign_sla.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_do_not_protect_sla(self, mock_get):

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test-vm",
                        "configuredSlaDomainId": "string_sla_id",
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
                "configuredSlaDomainId": "UNPROTECTED",
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

        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'do not protect',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_sla.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The vSphere VM 'test-vm' is already assigned to the 'do not protect' SLA Domain.")

    @patch.object(rubrik_assign_sla.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_clear_sla(self, mock_get):

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test-vm",
                        "configuredSlaDomainId": "string_sla_id",
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
                "configuredSlaDomainId": "INHERIT",
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

        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'clear',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_sla.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The vSphere VM 'test-vm' is already assigned to the 'clear' SLA Domain.")

    @patch.object(rubrik_assign_sla.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_assign_sla.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_assign_sla(self, mock_get, mock_post):

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

        def mock_get_v1_vmware_vm():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string_id",
                        "name": "test-vm",
                        "configuredSlaDomainId": "string_sla_id",
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
                "configuredSlaDomainId": "string_sla_id",
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
                "name": "test-vm",
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

        def mock_post_internal_sla_domain_id_assign():
            return {"status_code": "204"}

        set_module_args({
            'object_name': 'test-vm',
            'object_type': 'vmware',
            'sla_name': 'Gold',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

        mock_post.return_value = mock_post_internal_sla_domain_id_assign()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_assign_sla.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_internal_sla_domain_id_assign())


if __name__ == '__main__':
    unittest.main()
