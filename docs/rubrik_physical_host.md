# rubrik_physical_host    

Add or delete a physical host from a Rubrik cluster.

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`

# Example

```yaml
- rubrik_physical_host:
    hostname: 'ubuntu-physical-demo'
    action: 'add'

- rubrik_physical_host:
    hostname: 'ubuntu-physical-demo'
    action: 'delete'
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

| Name     | Description                                                                                                  | Default | Type | Choices     | Mandatory | Aliases    |
|----------|--------------------------------------------------------------------------------------------------------------|---------|------|-------------|-----------|------------|
| action   | Specify whether or not you wish to add or delete the physical host from the Rubrik cluster.                  |         |      | add, delete | True      |            |
| hostname | The hostname or IP Address of the physical host you want to add or delete from the Rubrik cluster.           |         |      |             | True      | ip_address |
|          |                                                                                                              |         |      |             |           |            |
|          |                                                                                                              |         |      |             |           |            |
|          |                                                                                                              |         |      |             |           |            |
| timeout  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 120     | int  |             |           |            |

# Return Values

| Name     | Description                                                                                 | Returned                                                            | Type   |
|----------|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------|--------|
| response | The full API response for POST /v1/host                                                     | on success when action is add                                       | dict   |
| response | The full API response for DELETE /v1/host/{id}.                                             | on success when action is delete                                    | dict   |
| response | A "No changed required" message when the host has already been added to the Rubrik cluster. | When the module idempotent check is succesful and action is add.    | string |
| response | A "No changed required" message when the host is not present on the Rubrik cluster.         | When the module idempotent check is succesful and action is delete. | string |
