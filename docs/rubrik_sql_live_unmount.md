# rubrik_sql_live_unmount

Delete a Microsoft SQL Live Mount from the Rubrik cluster.
`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_sql_live_mount:
    mounted_db_name: 'AdventureWorksClone'
    sql_instance: 'MSSQLSERVER'
    sql_host: 'sql.rubrikdemo.com'
    force: false
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
| mounted_db_name        | The name of the Live Mounted database to be unmounted.    |         | str  |         | true      |         |
| sql_instance           | The SQL instance name with the database you wish to Live Mount.                               | None | str  |         |true|         |
| sql_host               | The name of the MSSQL host running the Live Mounted database to be unmounted.  | None   | str |         |true|         |
| force             | Remove all data within the Rubrik cluster related to the Live Mount, even if the SQL Server database cannot be contacted.  | false    | bool |        | false |         |
| timeout                | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30      | int  |         |false|         |

# Return Values

| Name     | Description                                                                | Returned | Type | Aliases |
|----------|----------------------------------------------------------------------------|----------|------|---------|
| response | The full response of `DELETE /mssql/db/mount/{id}?force={bool}`.           | success  | dict |         |
