# rubrik_assign_sla 



`Requirement: Rubrik Python SDK (pip install rubri-cdm)`


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

| Name        | Description                                                                                                                                                                                                                                       | Default | Type   | Choices | Mandatory | Aliases |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------|---------|-----------|---------|
| object_name | The name of the Rubrik object you wish to assign to an SLA Domain.                                                                                                                                                                                |         | string |         | true      |         |
| sla_name    | The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use do not protect as the sla_name. To assign the selected object to the SLA of the next higher level object use clear as the sla_name |         | string |         | true      |         |
| object_type | The Rubrik object type you want to assign to the SLA Domain.                                                                                                                                                                                      | vmware  | string | vmware  |           |         |
| timeout     | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                                                                                                      | 30      | int    |         |           |         |



# Return Values

| Name     | Description                                                                                   | Returned                                       | Type   |
|----------|-----------------------------------------------------------------------------------------------|------------------------------------------------|--------|
| response | The full API reponse for POST /internal/sla_domain/{sla_id}/assign.                           | success                                        | dict   |
| response | A "No changed required" message when the Rubrik object is already assigned to the SLA Domain. | When the module idempotent check is succesful. | string |

