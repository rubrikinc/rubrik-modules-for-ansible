# rubrik_managed_volume    

Begin or end snapshots on a Rubrik Managed Volume.

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`

# Example

```yaml
# Begin a new managed volume snapshot.
- rubrik_managed_volume:
    name: MV1
    action: begin

# End the managed volume snapshot
- rubrik_managed_volume:
    name: MV1
    action: end
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

| Name                | Description                                                                                                                                                                   | Default | Type   | Choices    | Mandatory | Aliases |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------|------------|-----------|---------|
| action              | Specify whether or not you wish to begin or end a snapshot.                                                                                                                   |         | string | being, end | true      |         |
| managed_volume_name | The name of the Managed Volume to begin or end the snapshot on.                                                                                                               |         |        |            | true      | name    |
| sla_name            | The SLA Domain name you want to assign the snapshot to. By default, the currently assigned SLA Domain will be used. This parameter is only required when the `action' is end. | current | string |            |           |         |
|                     |                                                                                                                                                                               |         |        |            |           |         |
|                     |                                                                                                                                                                               |         |        |            |           |         |
| timeout             | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                                  | 15      | int    |            |           |         |

# Return Values

| Name     | Description                                                                              | Returned                                                           | Type   |
|----------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------|--------|
| response | The full API response for POST /internal/managed_volume/{id}/begin_snapshot              | on success when action is begin                                    | dict   |
| response | The full API response for POST /internal/managed_volume/{id}/end_snapshot                | on success when action is end                                      | dict   |
| response | A "No changed require" message when the managed volume is already in a writable state.   | When the module idempotent check is succesful and action is begin. | string |
| response | A "No changed required" message when the managed volume is already in a read only state. | When the module idempotent check is succesful and action is begin. | string |
