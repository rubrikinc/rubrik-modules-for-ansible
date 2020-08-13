# rubrik_create_sla   

Create a new SLA Domain.

`Requirement: Rubrik Python SDK (pip install rubrik_cdm)`

# Example

```yaml
- rubrik_create_sla:
    name: Ansible-SLA
    hourly_frequency: 1
    hourly_retention: 24
    daily_frequency: 1
    daily_retention: 30
    monthly_frequency: 1
    monthly_retention: 12
    yearly_frequency: 1
    yearly_retention: 5
    archive_name: S3:AWS-S3-Bucket
    retention_on_brik_in_days: 30
    instant_archive: True
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
| name                | The name of the new SLA Domain.                                                                              |         | str    |         | true      |         |
| hourly_frequency    | Hourly frequency to take backups.                                                                            |         | int    |         |           |         |
| hourly_retention    | Number of hours to retain the hourly backups.                                                                |         | int    |         |           |         |
| daily_frequency     | Daily frequency to take backups.                                                                             |         | int    |         |           |         |
| daily_retention     | Number of days to retain the daily backups.                                                                  |         | int    |         |           |         |
| monthly_frequency   | Monthly frequency to take backups.                                                                           |         | int    |         |           |         |
| monthly_retention   | Number of months to retain the monthly backups.                                                              |         | int    |         |           |         |
| yearly_frequency    | Yearly frequency to take backups.                                                                            |         | int    |         |           |         |
| yearly_retention    | Number of years to retain the yearly backups.                                                                |         | int    |         |           |         |
| starttime_hour      | Starting hour of allowed snapshot window. (CDM 5.0+)                                                         |         | int    |         |           |         |
| starttime_minute    | Starting minute of allowed snapshot window. (CDM 5.0+)                                                       |         | int    |         |           |         |
| duration_hours      | Length of allowed snapshot window in hours. (CDM 5.0+)                                                       |         | int    |         |           |         |
| archive_name        | The optional archive location you wish to configure on the SLA Domain. When populated, you must also provide `retention_on_brik_in_days`.                                                                                                         |         | str    |         |           |         |
| retention_on_brik_in_days | The number of days you wish to keep the backups on the Rubrik cluster. When populated, you must also provide `archive_name`.                                                                                                                      |         | int    |         |           |         |
| instant_archive     | Flag that determines whether or not to enable instant archive. Set to `true` to enable.                                                                                                                              |         | bool   |         |           |         |
| timeout             | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int    |         |           |         |

# Return Values

| Name                | Description                                                                            | Returned                                                    | Type |
|---------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------|------|
| full_response_cdm_4 | The full API response for POST /v1/sla_domain.                                         | On success when connected to a CDM v4.x or lower cluster    | dict |
| full_response_cdm_5 | The full API response for POST /v2/sla_domain.                                         | On success when connected to a CDM v5.0 or greater cluster  | dict |
| idempotent_response | A "No changed required" message when the Rubrik SLA is already present on the cluster. | When the module idempotent check is succesful.              | dict |
