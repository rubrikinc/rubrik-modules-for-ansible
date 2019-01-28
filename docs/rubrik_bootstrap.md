# rubrik_bootstrap    

Issues a bootstrap request to a specified Rubrik cluster

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`

# Example

```yaml
vars:
  node_config:
    1: 10.255.1.5

rubrik_bootstrap:
  cluster_name: "Ansible Demo"
  admin_email: "ansiblebuild@rubrik.com"
  admin_password: "AnsibleAndRubrikPassword"
  management_gateway: "10.255.1.1"
  management_subnet_mask: "255.255.255.0"
  enable_encryption: True
  dns_search_domains: ["rubrikansible.com"]
  wait_for_completion: True
  node_config: "{{ node_config }}"
```

# Arugments

## Common

| Name     | Description                                                                                                                                                                                                                                                                                               | Default |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| node_ip  | The DNS hostname or IP address of the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_node_ip environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter.                    |         |
| password | The password used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_password environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| username | The username used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_username environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| provider | Convenience method that allows all connection arguments (`node_ip', `username', `password') to be passed as a dict object. By default, the module will attempt to read these parameters from the rubrik_cdm_node_ip, rubrik_cdm_username, and rubrik_cdm_password environment variables.                  |         |


## Module Specific

| Name                   | Description                                                                                                  | Default          | Type   | Choices | Mandatory | Aliases |
|------------------------|--------------------------------------------------------------------------------------------------------------|------------------|--------|---------|-----------|---------|
| admin_email            | The Rubrik cluster sends messages for the admin account to this email address.                               |                  | string |         | true      |         |
| admin_password         | Password for the admin account.                                                                              |                  | string |         | true      |         |
| cluster_name           | Unique name to assign to the Rubrik cluster.                                                                 |                  | string |         | true      |         |
| dns_nameservers        | IPv4 addresses of DNS servers                                                                                | ['8.8.8.8']      | list   |         |           |         |
| dns_search_domains     | The search domain that the DNS Service will use to resolve hostnames that are not fully qualified.           | []               | list   |         |           |         |
| enable_encryption      | Enable software data encryption at rest. When bootstraping a Cloud Cluster this value needs to be False.     | True             | bool   |         |           |         |
| management_gateway     | IP address assigned to the management network gateway                                                        |                  | string |         | true      |         |
| management_subnet_mask | Subnet mask assigned to the management network.                                                              |                  | string |         | true      |         |
| node_config            | The Node Name and IP formatted as a dictionary                                                               |                  | dict   |         | true      |         |
| ntp_servers            | FQDN or IPv4 address of a network time protocol (NTP) server.                                                | ['pool.ntp.org'] | list   |         |           |         |
| wait_for_completion    | Flag to determine if the function should wait for the bootstrap process to complete.                         | True             | bool   |         |           |         |
| timeout                | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30               | int    |         |           |         |

# Return Values

| Name     | Description                                                    | Returned | Type |
|----------|----------------------------------------------------------------|----------|------|
| response | The full API response for POST /internal/cluster/me/bootstrap. | success  | dict |


