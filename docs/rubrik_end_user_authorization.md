# rubrik_end_user_authorization    

Grant an End User authorization to the provided object.

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`

# Example

```yaml
- rubrik_assign_sla:
    object_name: "ansible-tower"
    sla_name: "Gold"
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

| Name        | Description                                                                                                  | Default | Type   | Choices | Mandatory | Aliases |
|-------------|--------------------------------------------------------------------------------------------------------------|---------|--------|---------|-----------|---------|
| end_user    | The name of the end user you wish to grant authorization to.                                                 |         | string |         | true      |         |
| object_name | The name of the object you wish to grant the `end_user' authorization to.                                    |         | string |         | true      |         |
| object_type | The Rubrik object type you wish to grant authorization to.                                                   | vmware  | string | vmware  |           |         |
| timeout     | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int    |         |           |         |

# Return Values

| Name     | Description                                                                                                       | Returned                                       | Type  |
|----------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------|-------|
| response | The full API response for POST /internal/authorization/role/end_user                                              | success                                        | dict  |
| response | A "No changed required" message when the end user is already authorized to interface with provided I(objec_name). | When the module idempotent check is succesful. | sring |
