# rubrik_dns_servers

Live Mount a vSphere VM from a specified snapshot.
`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_vsphere_live_mount:
    vm_name: 'ansible-tower'
```

```yaml
- rubrik_vsphere_live_mount:
    vm_name: 'ansible-tower'
    date: '1-15-2019'
    time: '1:30 PM'
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
| vm_name                | The name of the vSphere VM to Live Mount.                                                                                                                           |         | str  |         | true      |         |
| date                   | The date of the snapshot you wish to Live Mount formated as Month-Day-Year (ex: 1-15-2014). If latest is specified, the last snapshot taken will be used.           | latest  | str  |         |           |         |
| time                   | The time of the snapshot you wish to Live Mount formated formated as Hour:Minute AM/PM (ex: 1:30 AM). If latest is specified, the last snapshot taken will be used. | latest  | str  |         |           |         |
| host                   | The hostname or IP address of the ESXi host to Live Mount the VM on.                                                                                                | current | str  |         |           |         |
| remove_network_devices | Flag that determines whether to remove the network interfaces from the Live Mounted VM. Set to True to remove all network interfaces.                               | False   | bool |         |           |         |
| power_on               | Flag that determines whether the VM should be powered on after the Live Mount. Set to True to power on the VM. Set to False to mount the VM but not power it on.    | True    | bool |         |           |         |
| timeout                | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                        | 15      | int  |         |           |         |

# Return Values

| Name     | Description                                                                | Returned | Type | Aliases |
|----------|----------------------------------------------------------------------------|----------|------|---------|
| response | The full API response for POST /v1/vmware/vm/snapshot/{snapshot_id}/mount. | success  | dict |         |
