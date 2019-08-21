# rubrik_assign_sla 

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_assign_sla:
    object_name: "ansible-tower"
    sla_name: "Gold"
```

```yaml
- rubrik_assign_sla:
    object_name: "sql-host"
    object_type: "mssql_host"
    sla_name: "Gold"
    log_backup_frequency_in_seconds: 120
    log_retention_hours: 12
    copy_only: false
```

```yaml
- rubrik_assign_sla:
    object_name: ["C:\\", "D:\\"]
    sla_name: "Gold"
    windows_host: "windows2016.rubrik.com"
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

| Name                            | Description                                                                                                                                                                                                                                       | Default | Type   | Choices            | Mandatory | Aliases |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------|--------------------|-----------|---------|
| object_name                     | The name of the Rubrik object you wish to assign to an SLA Domain.                                                                                                                                                                                |         | string |                    | true      |         |
| sla_name                        | The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use do not protect as the sla_name. To assign the selected object to the SLA of the next higher level object use clear as the sla_name |         | string |                    | true      |         |
| object_type                     | The Rubrik object type you want to assign to the SLA Domain.                                                                                                                                                                                      | vmware  | string | vmware, mssql_host |           |         |
| log_backup_frequency_in_seconds | The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is mssql_host.                                                                                                                                 | None    | int    |                    |           |         |
| log_retention_hours             | The MSSQL Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is mssql_host.                                                                                                                              | None    | int    |                    |           |         |
| copy_only                       | Take Copy Only Backups with MSSQL. Required when the `object_type` is mssql_host.                                                                                                                                                                 | None    | bool   |                    |           |         |
| timeout                         | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                                                                                                      | 30      | int    |                    |           |         |

# Return Values

| Name     | Description                                                                                   | Returned                                       | Type   |
|----------|-----------------------------------------------------------------------------------------------|------------------------------------------------|--------|
| response | The full API reponse for POST /internal/sla_domain/{sla_id}/assign.                           | success                                        | dict   |
| response | A "No changed required" message when the Rubrik object is already assigned to the SLA Domain. | When the module idempotent check is succesful. | string |
