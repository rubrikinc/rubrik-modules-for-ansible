# rubrik_get_vsphere_live_mount_names

Get existing Live Mount VM name(s) for a vSphere VM.
`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_get_vsphere_live_mount_names:
    vm_name: 'ansible-tower'
```

# Arugments

## Common

| Name      | Description                                                                                                                                                                                                                                                                                               | Default |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| node_ip   | The DNS hostname or IP address of the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_node_ip environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter.                    |         |
| password  | The password used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_password environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| username  | The username used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_username environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| api_token | The api token used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_token environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter.   |         |
| provider  | Convenience method that allows all connection arguments (`node_ip', `username', `password') to be passed as a dict object. By default, the module will attempt to read these parameters from the rubrik_cdm_node_ip, rubrik_cdm_username, and rubrik_cdm_password environment variables.                  |         |

| Note: The `username` and `password` must be supplied together and may not be provided if the `api_token` variable is present|
| --- |

## Module Specific

| Name                   | Description                                                                                                                                                         | Default | Type | Choices | Mandatory | Aliases |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|------|---------|-----------|---------|
| vm_name                | The name of the mounted vSphere VM.            |         | str  |         | true      |         |
| timeout                | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                        | 15      | int  |         |           |         |

# Return Values

| Name     | Description                                                                | Returned | Type | Aliases |
|----------|----------------------------------------------------------------------------|----------|------|---------|
| response | A list of the Live Mounted VM names.                                       | success  | list |         |
