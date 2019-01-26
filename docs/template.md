# rubrik_cluster_version    

Retrieves the software version of the Rubrik cluster.

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`


```yaml
- rubrik_cluster_version:

- rubrik_cluster_version:
    provider: "{{ credentials }}"
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

| Name    | Description                                                                                                  | Default | Type | Choices | Mandatory | Aliases |
|---------|--------------------------------------------------------------------------------------------------------------|---------|------|---------|-----------|---------|
|         |                                                                                                              |         |      |         |           |         |
|         |                                                                                                              |         |      |         |           |         |
|         |                                                                                                              |         |      |         |           |         |
|         |                                                                                                              |         |      |         |           |         |
|         |                                                                                                              |         |      |         |           |         |
| timeout | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30      | int  |         |           |         |

# Return Values

| Name     | Description | Returned                                       | Type   |
|----------|-------------|------------------------------------------------|--------|
| response |             | success                                        | dict   |
| response |             | When the module idempotent check is succesful. | string |
|          |             |                                                |        |
|          |             |                                                |        |
