# rubrik_replication_private

Configure replication partner as specified by user using PRIVATE NETWORK (direct connection).

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_replication_private:
    target_username: admin
    target_password: Rubrik
    target_cluster_address: 10.10.10.10
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
| target_username | Username allowed to connect to the replication target cluster.                                         |         | str  |         | true      |         |
| target_password | Password to connect to the replication target cluster.                                                 |         | str  |         | true      |         |
| target_cluster_address | The FQDN or IP of the replication target cluster.                                               |         | str  |         | true      |         |
| force | Force the replication target to refresh if it already exists.                                                    | False   | str  |         | false     |         |
| ca_certificate | CA certificiate used to perform TLS certificate validation.                                             |         | str  |         | false     |         |
| timeout   | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int  |         |           |         |

# Return Values

| Name     | Description                                                                       | Returned                                       | Type   | Aliases |
|----------|-----------------------------------------------------------------------------------|------------------------------------------------|--------|---------|
| response | The full API response from POST /internal/replication/target                      | success                                        | dict   |         |
| response | A "No changed required" message when the target cluster is already configured on the local cluster.                                | string |         |
