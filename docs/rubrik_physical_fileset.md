# rubrik_physical_fileset    

Create a Fileset for a Linux or Windows machine.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_physical_fileset:
    name: 'AnsibleDemo'
    include: '/usr/local'
    operating_system: 'Linux'
    exclude: '/usr/local/temp,*.mp3,*.mp4,*mp5'
    exclude_exception: '/company*.mp4'
    follow_network_shares: False
    backup_hidden_folders: False
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

| Name                  | Description                                                                                                  | Default | Type | Choices        | Mandatory | Aliases |
|-----------------------|--------------------------------------------------------------------------------------------------------------|---------|------|----------------|-----------|---------|
| backup_hidden_folders | Include or exclude hidden folders inside locally-mounted remote file systems from backups.                   | False   | bool |                |           |         |
| exclude               | The full paths or wildcards that define the objects to exclude from the Fileset backup.                      | []      | list |                |           |         |
| exclude_exception     | The full paths or wildcards that define the objects that are exempt from the excludes variables.             | []      | list |                |           |         |
| fileset_name          | The name of the Fileset you wish to create.                                                                  |         |      |                | True      | name    |
| follow_network_shares | Include or exclude locally-mounted remote file systems from backups.                                         | False   | bool |                |           |         |
| include               | The full paths or wildcards that define the objects to include in the Fileset backup.                        | []      | list | Linux, Windows | True      |         |
| operating_system      | The operating system type of the Fileset you are creating.                                                   |         |      |                |           |         |
| timeout               | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int  |                |           |         |

# Return Values

| Name     | Description                                                                                    | Returned                                       | Type   |
|----------|------------------------------------------------------------------------------------------------|------------------------------------------------|--------|
| response | The full response for the POST /internal/fileset_template/bulk API endpoint.                   | success                                        | dict   |
| response | A "No changed required" message when the NAS Fileset is already present on the Rubrik cluster. | When the module idempotent check is succesful. | string |
