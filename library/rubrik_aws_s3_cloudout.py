#!/usr/bin/python
# (c) 2018 Rubrik, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from module_utils.rubrik_cdm import credentials, load_provider_variables, rubrik_argument_spec
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: rubrik_aws_s3_cloudout
short_description: Add a new AWS S3 archival location to the Rubrik cluster.
description:
    - Add a new AWS S3 archival location to the Rubrik cluster..
version_added: '2.8'
author: Rubrik Build Team (@drew-russell) <build@rubrik.com>
options:
  aws_bucket_name:
    description:
      - The name of the AWS S3 bucket you wish to use as an archive target. The bucket name will automatically have all whitespace removed, all letters lowercased, and can not contain any of the following characters: _\/*?%.:|<>.
    required: true
    type: str
  aws_region:
    description:
      - The name of the AWS region where the bucket is located. If set to the default None keyword argument, we will look for a AWS_DEFAULT_REGION environment variable to pull the value from.
    choices: [ap-south-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, ca-central-1, cn-north-1, cn-northwest-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, sa-east-1, us-gov-west-1, us-west-1, us-east-1, us-east-2, us-west-2]
    required: false
    default: None
    type: str
  aws_access_key:
    description:
      - The access key of a AWS account with the required permissions. If set to the default None keyword argument, we will look for a AWS_ACCESS_KEY_ID environment variable to pull the value from.
    required: false
    default: None
    type: str
  aws_secret_key:
    description:
      - The secret key of a AWS account with the required permissions. If set to the default None keyword argument, we will look for a AWS_SECRET_ACCESS_KEY environment variable to pull the value from.
    required: false
    default: None
    type: str
  kms_master_key_id:
    description:
      - The AWS KMS master key ID that will be used to encrypt the archive data. If set to the default None keyword argument, you will need to provide a I(rsa_key) instead.
    required: false
    default: None
    type: str
  rsa_key:
    description:
      - The RSA key that will be used to encrypt the archive data. A key can be generated through openssl genrsa -out rubrik_encryption_key.pem 2048. If set to the default None keyword argument, you will need to provide a I(kms_master_key_id) instead.
    required: false
    default: None
    type: str
  archive_name:
    description:
      - The name of the archive location used in the Rubrik GUI. If set to 'default' the following naming convention will be used: "AWS:S3:aws_bucket_name".
    required: false
    default: None
    type: str
  storage_class:
    description:
      - The AWS storage class you wish to use.
    required: false
    choices: [standard, standard_ia, reduced_redundancy]
    default: standard
    type: str
  timeout:
    description:
    - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.
    required: False
    default: 180
    type: int

extends_documentation_fragment:
    - rubrik_cdm
requirements: [rubrik_cdm]
'''

EXAMPLES = '''
- rubrik_aws_s3_cloudout:
    aws_bucket_name: rubrik-s3-bucket
    kms_master_key_id: "{{ kms_master_key_id }}"
'''

RETURN = '''
response:
    description:The full API response for POST /internal/archive/object_store.
    returned: on success
    type: dict

response:
    description: A "No changed required" message when the S3 archival location has already been configured on the Rubrik cluster.
    returned: When the module idempotent check is succesful.
    type: str
    sample: No change required. The 'name' archival location is already configured on the Rubrik cluster.
'''


try:
    import rubrik_cdm
    HAS_RUBRIK_SDK = True
except ImportError:
    HAS_RUBRIK_SDK = False


def main():
    """ Main entry point for Ansible module execution.
    """

    results = {}

    argument_spec = dict(
        aws_bucket_name=dict(required=True, type='str'),
        aws_region=dict(required=False, default=None, type='str'),
        aws_access_key=dict(required=False, default=None, type='str'),
        aws_secret_key=dict(required=False, default=None, type='str'),
        kms_master_key_id=dict(required=False, default=None, type='str'),
        rsa_key=dict(required=False, default=None, type='str'),
        archive_name=dict(required=False, default=None, type='str'),
        storage_class=dict(required=False, default="standard", type='str'),
        timeout=dict(required=False, type='int', default=180),
    )

    argument_spec.update(rubrik_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    ansible = module.params

    load_provider_variables(module)

    aws_bucket_name = ansible["aws_bucket_name"]
    aws_region = ansible["aws_region"]
    aws_access_key = ansible["aws_access_key"]
    aws_secret_key = ansible["aws_secret_key"]
    kms_master_key_id = ansible["kms_master_key_id"]
    rsa_key = ansible["rsa_key"]
    archive_name = ansible["archive_name"]
    storage_class = ansible["storage_class"]
    timeout = ansible["timeout"]

    if not HAS_RUBRIK_SDK:
        module.fail_json(msg='The Rubrik Python SDK is required for this module (pip install rubrik_cdm).')

    node_ip, username, password, api_token = credentials(module)

    try:
        rubrik = rubrik_cdm.Connect(node_ip, username, password, api_token)
    except Exception as error:
        module.fail_json(msg=str(error))

    try:
        api_request = rubrik.aws_s3_cloudout(
            aws_bucket_name,
            archive_name,
            aws_region,
            aws_access_key,
            aws_secret_key,
            kms_master_key_id,
            rsa_key,
            storage_class,
            timeout)
    except Exception as error:
        module.fail_json(msg=str(error))

    if "No change required" in api_request:
        results["changed"] = False
    else:
        results["changed"] = True

    results["response"] = api_request

    module.exit_json(**results)


if __name__ == '__main__':
    main()
