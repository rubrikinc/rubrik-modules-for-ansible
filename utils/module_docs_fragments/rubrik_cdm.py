#
# (c) Rubrik
# Author: Drew Russell (@drusse11)
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = """
options:
  node_ip:
    description:
      - The DNS hostname or IP address of the Rubrik cluster. By defeault, the module will attempt to 
        read this value from the rubrik_cdm_node_ip environment variable. If this environment variable is 
        not present it will need to be manually specified here or in the I(provider) parameter.
    required: false
  username:
    description:
      - The username used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to 
        read this value from the rubrik_cdm_username environment variable. If this environment variable is 
        not present it will need to be manually specified here or in the I(provider) parameter.
    required: false
  password:
    description:
      - The password used to authenticate the connection to the Rubrik cluster. By defeault, the module will attempt to 
        read this value from the rubrik_cdm_password environment variable. If this environment variable is 
        not present it will need to be manually specified here or in the I(provider) parameter.
    required: false
  provider:
    description:
      - Convenience method that allows all connection arguments (I(node_ip), I(username), I(password)) to be passed as a dict object. By default,
        the module will attempt to read these parameters from the rubrik_cdm_node_ip, rubrik_cdm_username, and rubrik_cdm_password environment variables.
        If these environment variables are not found the parameters must be provided as individual parameter or values in this dict.
    required: false
"""
