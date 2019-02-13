# rubrik_assign_physical_host_fileset   

Assign a fileset to a Linux or Windows machine. If you have multiple filesets with identical names, you will need to populate the filesets properties to find a specific match. Filesets with identical names and properties are not supported.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_assign_physical_host_fileset:
    hostname: 'ansible-tower'
    fileset_name: 'all-files'
    operating_system: Linux
    sla_name: 'Gold'
```

# Arugments

## Common

| Name     | Description                                                                                                                                                                                                                                                                                               | Default |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| node_ip  | The DNS hostname or IP address of the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_node_ip environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter.                    |         |
| password | The password used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_password environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| username | The username used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to read this value from the rubrik_cdm_username environment variable. If this environment variable is not present it will need to be manually specified here or in the `provider' parameter. |         |
| provider | Convenience method that allows all connection arguments (`node_ip', `username', `password') to be passed as a dict object. By default, the module will attempt to read these parameters from the rubrik_cdm_node_ip, rubrik_cdm_username, and rubrik_cdm_password environment variables.                  |         |


## Module Specific

| Name                  | Description                                                                                                  | Default | Type   | Choices        | Mandatory | Aliases    |
|-----------------------|--------------------------------------------------------------------------------------------------------------|---------|--------|----------------|-----------|------------|
| backup_hidden_folders | Include or exclude hidden folders inside locally-mounted remote file systems from backups.                   | False   | Bool   |                |           |            |
| exclude               | The full paths or wildcards that define the objects to exclude from the Fileset backup.                      | []      | list   |                |           |            |
| exclude_exception     | The full paths or wildcards that define the objects that are exempt from the excludes variables.             | []      | list   |                |           |            |
| fileset_name          | The name of the Fileset you wish to assign to the Linux or Windows host.                                     |         | string |                | true      |            |
| follow_network_shares | Include or exclude locally-mounted remote file systems from backups.                                         | False   | bool   |                |           |            |
| hostname              | The hostname or IP Address of the physical host you wish to associate to the Fileset.                        |         | string |                | true      | ip_address |
| include               | The full paths or wildcards that define the objects to include in the Fileset backup.                        | []      | list   |                |           |            |
| operating_system      | The operating system of the physical host you are assigning a Fileset to                                     |         | string | Linux, Windows | true      |            |
| sla_name              | The name of the SLA Domain to associate with the Fileset.                                                    |         | string |                |           | sla        |
| timeout               | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 30      | int    |                |           |            |






# Return Values

| Name     | Description                                                                                       | Returned                                       | Type   |
|----------|---------------------------------------------------------------------------------------------------|------------------------------------------------|--------|
| response | The full API response for POST /v1/host.                                                          | success                                        | dict   |
| response | A "No changed require" message when the physical host is already connected to the Rubrik cluster. | When the module idempotent check is succesful. | string |
