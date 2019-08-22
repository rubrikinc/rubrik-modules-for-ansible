# rubrik_on_demand_snapshot    

Take an on-demand snapshot of a Rubrik object.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_on_demand_snapshot:
    object_name: 'ansible-node01'
    object_type: "vmware"

- rubrik_on_demand_snapshot:
        object_name: "ansible-demo"
        object_type: "physical_host"
        fileset: "Python SDK"
        host_os: "Linux"
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

| Name        | Description                                                                                                                   | Default | Type   | Choices                    | Mandatory | Aliases |
|-------------|-------------------------------------------------------------------------------------------------------------------------------|---------|--------|----------------------------|-----------|---------|
| fileset     | The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host.                | None    | string |                            |           |         |
| host_os     | The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host.                | None    | string | None, Linux, Windows       |           |         |
| object_name | The name of the Rubrik object to take a on-demand snapshot of.                                                                | vmware  | string | vmware, physical_host, ahv | true      |         |
| object_type | The Rubrik object type you want to backup.                                                                                    |         |        |                            |           |         |
| sla_name    | The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used. | current |        |                            |           |         |
| timeout     | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                  | 30      | int    |                            |           |         |

# Return Values

| Name           | Description                                                                                                                | Returned                                     | Type   |
|----------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|--------|
| response       | The full API response for POST /v1/vmware/vm/{id}/snapshot.                                                                | on success when action is vmware             | dict   |
| response       | The full API response for POST /v1/fileset/{id}/snapshot.                                                                  | on success when object_type is physical_host | dict   |
| job_status_url | The job staturs url retuend by the full API response which can be passed into the rubrik_job_status module for monitoring. | success                                      | string |

