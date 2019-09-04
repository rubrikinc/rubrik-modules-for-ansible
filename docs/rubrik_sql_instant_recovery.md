# rubrik_sql_instant_recovery

Perform an instant recovery for an MSSQL database from a specified recovery point.
`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_sql_live_mount:
    db_name: 'AdventureWorks2016'
    date: '08-26-2018'
    time: '12:11 AM'
    sql_instance: 'MSSQLSERVER'
    sql_host: 'sql.rubrikdemo.com'
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
| db_name                | The name of the database to instantly recover      |         | str  |         | true      |         |
| date                   | The recovery_point date to recover to formated as `Month-Day-Year` (ex: 1-15-2014).  |       | str  |         |true|         |
| time                   | The recovery_point time you wish to Live Mount formated as `Hour:Minute AM/PM` (ex: 1:30 AM). |       | str  |         |true|         |
| sql_instance           | The SQL instance name with the database to instantly recover.  | None | str  |         |true|         |
| sql_host               | The SQL Host of the database/instance to instantly recover.  | None   | str |         |true|         |
| finish_recovery        | A Boolean value that determines the recovery option to use during database restore. When this value is 'true', the database is restored using the RECOVERY option and is fully functional at the end of the restore operation. When this value is 'false', the database is restored using the NORECOVERY option and remains in recovering mode at the end of the restore operation.  | True  | bool |         |False|         |
| max_data_streams       | Maximum number of parallel data streams that can be used to copy data to the target system. | 0  | int |      |False|         |
| timeout                | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30      | int  |         |false|         |

# Return Values

| Name     | Description                                                                | Returned | Type | Aliases |
|----------|----------------------------------------------------------------------------|----------|------|---------|
| response | The full response of POST /mssql/db/{id}/restore.                       | success  | dict |         |
