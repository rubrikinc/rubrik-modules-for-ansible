import json
import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_physical_host as rubrik_physical_host


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


class TestRubrikPhysicalHost(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_physical_host.main()

    def test_module_fail_with_incorrect_hostname_list_when_action_is_delete(self):
        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'delete',
            'hostname': ['hostname1', 'hostname2'],
        })

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "A list of hostnames is not supported when action is delete.")

    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_physical_host_add(self, mock_get, mock_post):

        def mock_get_v1_host():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "string",
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

        def mock_post_v1_host():
            return {
                "id": "string",
                "name": "string",
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
                "organizationName": "string",
                "agentId": "string",
                "compressionEnabled": True,
                "isRelic": True,
                "mssqlCbtDriverInstalled": True,
                "hostVfdEnabled": "Enabled",
                "hostVfdDriverState": "NotInstalled",
                "oracleSysDbaUser": "string"
            }

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'add',
            'hostname': 'hostname'
        })

        mock_get.return_value = mock_get_v1_host()

        mock_post.return_value = mock_post_v1_host()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_post_v1_host())

    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_add(self, mock_get):

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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'add',
            'hostname': 'hostname'
        })

        mock_get.return_value = mock_get_v1_host()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'],
            "No change required. The host 'hostname' is already connected to the Rubrik cluster.")

    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_add_list(self, mock_get):

        def mock_get_v1_host():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "string",
                        "hostname": "hostname1",
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
                    },
                    {
                        "id": "string",
                        "name": "string",
                        "hostname": "hostname2",
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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'add',
            'hostname': ["hostname1", "hostname2"]
        })

        mock_get.return_value = mock_get_v1_host()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'],
                         "No Change Required. All Hosts Already added or supplied list was empty")

    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'delete', autospec=True, spec_set=True)
    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_rubrik_physical_host_delete(self, mock_get, mock_delete):

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
                    },
                    {
                        "id": "string",
                        "name": "string",
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
                "total": 2
            }

        def mock_delete_v1_host_id():
            return {"status_code: 204"}

            set_module_args({
                'node_ip': '1.1.1.1',
                'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
                'action': 'delete',
                'hostname': 'hostname'
            })

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'delete',
            'hostname': 'hostname'
        })

        mock_get.return_value = mock_get_v1_host()

        mock_delete.return_value = mock_delete_v1_host_id()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_delete_v1_host_id())

    @patch.object(rubrik_physical_host.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence_delete(self, mock_get):

        def mock_get_v1_host():
            return {
                "hasMore": True,
                "data": [
                    {
                        "id": "string",
                        "name": "string",
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

        set_module_args({
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'action': 'delete',
            'hostname': "hostname"
        })

        mock_get.return_value = mock_get_v1_host()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_physical_host.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(
            result.exception.args[0]['response'], "No change required. The host 'hostname' is not connected to the Rubrik cluster.")
