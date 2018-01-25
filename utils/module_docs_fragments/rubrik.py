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
  node:
    description:
      - Specifies the DNS hostname or IP address for connecting to the Rubrik
        Cluster.  
    required: true
  username:
    description:
      - Configures the username to use to authenticate the connection to
        the Rubrik Cluster.
    required: false
  password:
    description:
      - Specifies the password to use to authenticate the connection to
        the Rubrik Cluster.
    required: false
    default: null
  provider:
    description:
      - Convenience method that allows all connection arguments (node, username, password) 
        to be passed as a dict object.  All options must be met either by individual arguments 
        or values in this dict.
    required: false
    default: null
"""
