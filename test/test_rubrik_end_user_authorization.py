import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
import library.rubrik_end_user_authorization as rubrik_end_user_authorization

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

class TestRubrikEndUserAuthorization(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_end_user_authorization.main()

    def test_module_fail_with_invalid_object(self):

        set_module_args({
            'object_name': 'server_1',
            'end_user': 'testuser',
            'object_type': 'invalid_object_type',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_end_user_authorization.main()
        
        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], 'value of object_type must be one of: vmware, got: invalid_object_type')

    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'object_id', autospec=True, spec_set=True)
    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_fail_with_invalid_user(self, mock_get, mock_object_id):

        def mock_self_object_id():
            return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

        def mock_internal_user_username():
            return []

        set_module_args({
            'object_name': 'server_1',
            'end_user': 'testuser',
            'object_type': 'vmware',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_object_id.return_value = mock_self_object_id()

        mock_get.return_value = mock_internal_user_username()

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_end_user_authorization.main()
        
        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], 'The Rubrik cluster does not contain a End User account named "testuser".')

    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'object_id', autospec=True, spec_set=True)
    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_idempotence(self, mock_get, mock_object_id):

        def mock_self_object_id():
            return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

        def mock_internal_user_username():
            return [
                {
                    "id": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                    "authDomainId": "string",
                    "username": "testuser",
                    "firstName": "string",
                    "lastName": "string",
                    "emailAddress": "string",
                    "contactNumber": "string",
                    "mfaServerId": "string"
                }
            ]

        def mock_internal_authorization_role_end_user_principals():
            return {
                "hasMore": True,
                "data": [
                    {
                        "principal": "string",
                        "privileges": {
                            "destructiveRestore": [
                                "string"
                            ],
                            "restore": [
                                "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"
                            ],
                            "onDemandSnapshot": [
                                "string"
                            ],
                            "restoreWithoutDownload": [
                                "string"
                            ],
                            "viewEvent": [
                                "string"
                            ],
                            "provisionOnInfra": [
                                "string"
                            ],
                            "viewReport": [
                                "string"
                            ]
                        },
                        "organizationId": "string"
                    }
                ],
                "total": 1
            }

        set_module_args({
            'object_name': 'server_1',
            'end_user': 'testuser',
            'object_type': 'vmware',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_object_id.return_value = mock_self_object_id()

        mock_get.side_effect = [mock_internal_user_username(), mock_internal_authorization_role_end_user_principals()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_end_user_authorization.main()
        
        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], 'No change required. The End User "testuser" is already authorized to interact with the "server_1" VM.')

    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'object_id', autospec=True, spec_set=True)
    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_end_user_authorization.rubrik_cdm.rubrik_cdm.Connect, 'get', autospec=True, spec_set=True)
    def test_module_configure_user_authorization(self, mock_get, mock_post, mock_object_id):

        def mock_self_object_id():
            return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

        def mock_internal_user_username():
            return [
                {
                    "id": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                    "authDomainId": "string",
                    "username": "testuser",
                    "firstName": "string",
                    "lastName": "string",
                    "emailAddress": "string",
                    "contactNumber": "string",
                    "mfaServerId": "string"
                }
            ]

        def mock_internal_authorization_role_end_user_principals():
            return {
                "hasMore": True,
                "data": [
                    {
                        "principal": "string",
                        "privileges": {
                            "destructiveRestore": [
                                "string"
                            ],
                            "restore": [
                                "VirtualMachine:::e6a7e6r3-6050-1ee33-9ba6-8e284e2801de"
                            ],
                            "onDemandSnapshot": [
                                "string"
                            ],
                            "restoreWithoutDownload": [
                                "string"
                            ],
                            "viewEvent": [
                                "string"
                            ],
                            "provisionOnInfra": [
                                "string"
                            ],
                            "viewReport": [
                                "string"
                            ]
                        },
                        "organizationId": "string"
                    }
                ],
                "total": 1
            }

        def mock_internal_authorization_role_end_user():
            return {
                "hasMore": False,
                "data": [
                    {
                        "principal": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                        "privileges": {
                            "destructiveRestore": [],
                            "restore": [
                                "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297-not-present"
                            ],
                            "onDemandSnapshot": [],
                            "restoreWithoutDownload": [],
                            "viewEvent": [],
                            "provisionOnInfra": [],
                            "viewReport": []
                        },
                        "organizationId": "Organization:::05e3ee0b-5ec1-e33b-88a5-d916855aff5f"
                    }
                ],
                "total": 1
            }

        set_module_args({
            'object_name': 'server_1',
            'end_user': 'testuser',
            'object_type': 'vmware',
            'node_ip': '1.1.1.1',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        mock_object_id.return_value = mock_self_object_id()

        mock_get.side_effect = [mock_internal_user_username(), mock_internal_authorization_role_end_user_principals()]

        mock_post.return_value = mock_internal_authorization_role_end_user()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_end_user_authorization.main()
        
        self.assertEqual(result.exception.args[0]['changed'], True)
        self.assertEqual(result.exception.args[0]['response'], mock_internal_authorization_role_end_user())