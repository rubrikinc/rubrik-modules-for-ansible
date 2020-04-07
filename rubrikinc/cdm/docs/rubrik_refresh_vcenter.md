# rubrik_job_status    

Refresh the metadata for the specified vCenter Server. Refreshing vCenter metadata happens automatically on a regular basis, but it may be necessary to trigger a refresh to protect a newly deployed VM.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_refresh_vcenter:
    vcenter_ip: "vcenter.example.com"
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

| Name                | Description                                                                                                  | Default | Type   | Choices | Mandatory | Aliases |
|---------------------|--------------------------------------------------------------------------------------------------------------|---------|--------|---------|-----------|---------|
| vcenter_ip          | The IP address or FQDN of the vCenter you wish to refesh.                                                    |         | string |         | true      |         |
| wait_for_completion | Flag that determines if the method should wait for the job to complete before exiting.                       | true    | bool   |         |           |         |
| timeout             | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int    |         |           |         |

# Return Values

| Name     | Description                             | Returned | Type |
|----------|-----------------------------------------|----------|------|
| response | The full API response for the API call. | success  | dict |