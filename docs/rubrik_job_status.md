# rubrik_job_status    

Certain Rubrik operations may not instantaneously complete. In those cases we have the ability to monitor the status of the job through a job status link provided in the actions API response body. In those cases the Ansible Module will return a "job_status_link" which can then be registered and used as a variable in the rubrik_job_status module. The rubrik_job_status will check on the status of the job every 20 seconds until the job has successfully completed for failed.

`Requirement: Rubrik Python SDK (pip install rubri-cdm)`

# Example

```yaml
- rubrik_job_status:
    url: "https://192.168.1.100/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fbcb1d87-9872-4227-a68c-5982f48-vm-289386_e837-a04c-4327-915b-7698d2c5ecf48:::0"
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

| Name                | Description                                                                                                  | Default | Type   | Choices | Mandatory | Aliases |
|---------------------|--------------------------------------------------------------------------------------------------------------|---------|--------|---------|-----------|---------|
| url                 | The job status URL provided by a previous API call.                                                          |         | string |         | true      |         |
| wait_for_completion | Flag that determines if the method should wait for the job to complete before exiting.                       | true    | bool   |         |           |         |
| timeout             | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15      | int    |         |           |         |

# Return Values

| Name     | Description                             | Returned | Type |
|----------|-----------------------------------------|----------|------|
| response | The full API response for the API call. | success  | dict |
