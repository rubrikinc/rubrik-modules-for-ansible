#!/usr/bin/python
# Copyright: Rubrik
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


def get_archive(module, aws_bucket_name):

    archive_present = False

    api_version = 'internal' #v1 or internal
    endpoint = '/archive/object_store'

    response_body = rubrik_get(module, api_version, endpoint)

    current_object_stores = []
    # Pull the individual object store definitions from the response_body
    for response in response_body['data']:
        for key, value in response.items():
            if key == 'definition':
                current_object_stores.append(value)

    for defintion in current_object_stores:
        if defintion['objectStoreType'] == 'S3':
            if defintion['bucket'] == aws_bucket_name:
                archive_present = True

    return archive_present


def create_aws_s3_object_store(module, archive_name, aws_bucket_name, aws_access_key, aws_secret_key, aws_region, rsa_key, s3_storage_class):

    ansible = module.params

    # Remove the Start and End of the .pem file and replace spaces with \n
    rsa_key = rsa_key.replace("-----BEGIN RSA PRIVATE KEY----- ",
                              '').replace(" -----END RSA PRIVATE KEY-----", '').replace(' ', '\n')
    # Recreate the .pem File
    rsa_pem_file_content = "-----BEGIN RSA PRIVATE KEY-----\n" + rsa_key + "\n-----END RSA PRIVATE KEY-----"

    create_object_store_data_model = {}
    create_object_store_data_model['name'] = archive_name
    create_object_store_data_model['bucket'] = aws_bucket_name
    create_object_store_data_model['objectStoreType'] = 'S3'
    create_object_store_data_model['accessKey'] = aws_access_key
    create_object_store_data_model['secretKey'] = aws_secret_key
    create_object_store_data_model['defaultRegion'] = aws_region
    create_object_store_data_model['pemFileContent'] = rsa_pem_file_content
    create_object_store_data_model['storageClass'] = s3_storage_class.upper()

    api_version = 'internal' #v1 or internal
    endpoint = '/archive/object_store'

    rubrik_post(module, api_version, endpoint, create_object_store_data_model, timeout=200)


def main():
    '''Ansible main. '''

    argument_spec = rubrik_argument_spec

    argument_spec.update(
        dict(
            aws_bucket_name=dict(required=True),
            aws_access_key=dict(required=True),
            aws_secret_key=dict(required=True, no_log=True),
            aws_region=dict(required=True, choices=['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1',
                                                    'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1']),
            rsa_key=dict(required=True, no_log=True),
            s3_storage_class=dict(required=True, choices=['standard', 'standard_ia', 'reduced_redundancy']),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    results = {}
    load_provider_variables(module)
    ansible = module.params

    archive_name = 'S3:{}'.format(ansible['aws_bucket_name'])
    aws_bucket_name = ansible['aws_bucket_name']
    aws_access_key = ansible['aws_access_key']
    aws_secret_key = ansible['aws_secret_key']
    aws_region = ansible['aws_region']
    rsa_key = ansible['rsa_key']
    s3_storage_class = ansible['s3_storage_class']

    # Validate that the AWS S3 Bucket is not already configured on the Rubrik Cluster
    current_archives = get_archive(module, aws_bucket_name)

    if current_archives:
        results['changed'] = False
        results['response'] = "The AWS S3 Bucket '{}' has already been configured as an Archive Location on the Rubrik Cluster.".format(
            aws_bucket_name)
    else:
        create_aws_s3_object_store(module, archive_name, aws_bucket_name, aws_access_key,
                                   aws_secret_key, aws_region, rsa_key, s3_storage_class)
        results['changed'] = True
        results['response'] = "Successfully connected the Rubrik Cluster to the AWS S3 Bucket '{}'.".format(
            aws_bucket_name)

    module.exit_json(**results)


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rubrik import load_provider_variables, rubrik_argument_spec, rubrik_get, rubrik_post


if __name__ == "__main__":
    main()
