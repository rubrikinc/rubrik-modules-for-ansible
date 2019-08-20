import json

import unittest
from unittest.mock import Mock, patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from urllib.error import HTTPError
from rubrik_cdm.exceptions import RubrikException, APICallException
from socket import gaierror
import library.rubrik_bootstrap as rubrik_bootstrap

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

class TestRubrikBootstrap(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, '__init__', autospec=True, spec_set=True)
    def test_module_bootstrap_idempotency(self, mock_bootstrap_init, mock_post):

        def mock_post_v1_exception():
            return APICallException('Cannot bootstrap from an already bootstrapped node')

        node_config = {}
        node_config['1'] = '10.255.1.10'

        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': node_config,
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'wait_for_completion': False
        })

        mock_bootstrap_init.return_value = None
        mock_bootstrap_init.ipv6_addr = 'ffd2::1'
        mock_bootstrap_init.ipv6_scope = '0'
        mock_bootstrap_init.node_ip = 'ffd2::1%0'

        mock_post.side_effect = mock_post_v1_exception()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response'], 'No change required. The Rubrik cluster is already bootstrapped.')

    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, '__init__', autospec=True, spec_set=True)
    def test_module_bootstrap_node_no_wait(self, mock_bootstrap_init, mock_post):
        def mock_post_v1_bootstrap():
            return {
                'id': 0,
                'status': 'IN_PROGRESS'
            }

        node_config = {}
        node_config['1'] = '10.255.1.10'

        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': node_config,
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'wait_for_completion': False
        })

        mock_bootstrap_init.return_value = None
        mock_bootstrap_init.ipv6_addr = 'ffd2::1'
        mock_bootstrap_init.ipv6_scope = '0'
        mock_bootstrap_init.node_ip = 'ffd2::1%0'

        mock_post.return_value = mock_post_v1_bootstrap()

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response']['status'], 'IN_PROGRESS')

    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.time, 'sleep', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'get', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, '__init__', autospec=True, spec_set=True)
    def test_module_bootstrap_node_wait_for_completion(self, mock_bootstrap_init, mock_post, mock_get, mock_sleep):
        def mock_post_v1_bootstrap():
            return {
                'id': 0,
                'status': 'IN_PROGRESS'
            }

        def mock_get_v1_bootstrap_status_1():
            return {
                'status': 'IN_PROGRESS',
                'message': '',
                'ipConfig': 'SUCCESS',
                'cassandraSetup': 'SUCCESS',
                'installSchema': 'SUCCESS',
                'startServices': 'SUCCESS',
                'ipmiConfig': 'SUCCESS',
                'configAdminUser': 'SUCCESS',
                'resetNodes': 'IN_PROGRESS',
                'setupDisks': 'SUCCESS',
                'setupEncryptionAtRest': 'SUCCESS',
                'setupOsAndMetadataPartitions': 'SUCCESS',
                'createTopLevelFilesystemDirs': 'SUCCESS',
                'setupLoopDevices': 'SUCCESS',
                'cockroachDbSetup': 'SUCCESS'
            }

        def mock_get_v1_bootstrap_status_2():
            return {
                'status': 'SUCCESS',
                'message': '',
                'ipConfig': 'SUCCESS',
                'cassandraSetup': 'SUCCESS',
                'installSchema': 'SUCCESS',
                'startServices': 'SUCCESS',
                'ipmiConfig': 'SUCCESS',
                'configAdminUser': 'SUCCESS',
                'resetNodes': 'SUCCESS',
                'setupDisks': 'SUCCESS',
                'setupEncryptionAtRest': 'SUCCESS',
                'setupOsAndMetadataPartitions': 'SUCCESS',
                'createTopLevelFilesystemDirs': 'SUCCESS',
                'setupLoopDevices': 'SUCCESS',
                'cockroachDbSetup': 'SUCCESS'
            }

        node_config = {}
        node_config['1'] = '10.255.1.10'

        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': node_config,
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'timeout': 1,
            'wait_for_completion': True
        })

        # Mock sleep function so test does not take 30 seconds to run
        mock_sleep.return_value = None

        mock_bootstrap_init.return_value = None
        mock_bootstrap_init.ipv6_addr = 'ffd2::1'
        mock_bootstrap_init.ipv6_scope = '0'
        mock_bootstrap_init.node_ip = 'ffd2::1%0'

        mock_post.return_value = mock_post_v1_bootstrap()

        mock_get.side_effect = [mock_get_v1_bootstrap_status_1(), mock_get_v1_bootstrap_status_2()]

        with self.assertRaises(AnsibleExitJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['changed'], False)
        self.assertEqual(result.exception.args[0]['response']['status'], 'SUCCESS')

    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.time, 'sleep', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'post', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, '__init__', autospec=True, spec_set=True)
    def test_module_fail_connection_timeout(self, mock_bootstrap_init, mock_post, mock_sleep):

        def mock_post_v1_exception():
            return APICallException('Failed to establish a new connection: [Errno 111] Connection refused')

        node_config = {}
        node_config['1'] = '10.255.1.10'

        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': node_config,
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
            'wait_for_completion': False
        })

        # Mock sleep function so test does not take too long to run
        mock_sleep.return_value = None
        mock_sleep.side_effect = None

        mock_bootstrap_init.return_value = None
        mock_bootstrap_init.ipv6_addr = 'ffd2::1'
        mock_bootstrap_init.ipv6_scope = '0'
        mock_bootstrap_init.node_ip = 'ffd2::1%0'

        mock_post.side_effect = mock_post_v1_exception()

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], 'Unable to establish a connection to the Rubrik cluster.')

    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.socket, 'getaddrinfo', autospec=True, spec_set=True)
    @patch.object(rubrik_bootstrap.rubrik_cdm.rubrik_cdm.Bootstrap, 'post', autospec=True, spec_set=True)
    def test_module_fail_resolution_failure(self, mock_post, mock_getaddrinfo):

        def mock_getaddrinfo_failure():
            return gaierror('Could not resolve link-local IPv6 address for cluster.')

        node_config = {}
        node_config['1'] = 'badhost.local'

        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': node_config,
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP',
        })

        mock_getaddrinfo.side_effect = mock_getaddrinfo_failure()

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], 'Error: Could not resolve addrsss for cluster, or invalid IP/address supplied')

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rubrik_bootstrap.main()

    def test_module_fail_with_malformed_node_config(self):
        set_module_args({
            'cluster_name': 'cluster_name',
            'admin_email': 'admin@noreply.com',
            'admin_password': 'adminpassword',
            'node_ip': 'rubrikbootstrap.local',
            'node_config': 'foo',
            'management_gateway': '10.255.1.1',
            'management_subnet_mask': '255.255.255.0',
            'username': 'foo',
            'api_token': 'vkys219gn2jziReqdPJH0asGM3PKEQHP'
        })

        with self.assertRaises(AnsibleFailJson) as result:
            rubrik_bootstrap.main()

        self.assertEqual(result.exception.args[0]['failed'], True)
        self.assertEqual(result.exception.args[0]['msg'], "argument node_config is of type <class 'str'> and we were unable to convert to dict: dictionary requested, could not parse JSON or key=value")