# rubrik_get

Send a GET request to the provided Rubrik API endpoint.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_post:
    api_version: internal
    api_endpoint: "/managed_volume"
    config: {"name": "AnsibleDemo", "volumeSize": 10737418240}
```

# Arguments

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

| Name           | Description                                                                                                  | Default | Type   | Choices | Mandatory | Aliases |
|----------------|--------------------------------------------------------------------------------------------------------------|---------|--------|---------|-----------|---------|
| api_version    | The version of the Rubrik CDM API to call.                                                                   |         | string |         | true      |         |
| api_endpoint   | The endpoint of the Rubrik CDM API to call (ex. /cluster/me).                                                |         | string |         | true      |         |
| config         | The specified data to send with the API call.                                                                |         | raw    |         | false     |         |
| authentication | Flag that specifies whether or not to utilize authentication when making the API call.                       | True    | book   |         | false     |         |
| timeout        | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30      | int    |         | false     |         |

# Return Values

| Name     | Description                        | Returned | Type |
|----------|------------------------------------|----------|------|
| response | The response body of the API call. | success  | dict |
