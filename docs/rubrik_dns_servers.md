# rubrik_dns_servers

Configure the DNS Servers on the Rubrik cluster.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_dns_servers:
    server_ip: ["192.168.100.20", "192.168.100.21"]
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

| Name      | Description                                                                                                  | Default | Type | Choices | Mandatory | Aliases |
|-----------|--------------------------------------------------------------------------------------------------------------|---------|------|---------|-----------|---------|
| server_ip | The DNS Server IPs you wish to add to the Rubrik cluster.                                                    |         | list |         | true      |         |
| timeout   | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int  |         |           |         |

# Return Values

| Name     | Description                                                                       | Returned                                       | Type   | Aliases |
|----------|-----------------------------------------------------------------------------------|------------------------------------------------|--------|---------|
| response | The full API response for POST /internal/cluster/me/dns_nameserver.               | success                                        | dict   |         |
| response | A "No changed required" message when the DNS servers have already been configured | When the module idempotent check is succesful. | string |         |
