# NetworkConfigUtility

NetworkConfigUtility is currently a small program to assist with pushing configuration data to network devices. It can
also retrieve state data. This utility is built using the Nornir framework:

https://github.com/nornir-automation/nornir

## Source Code
https://github.com/naonder/NetworkConfigUtility

##PyPI package
https://pypi.org/project/networkconfigutility

##Setup
    pip install networkconfigutility
    
See sample hosts, groups, and defaults file for reference. Also see the following for more information on Nornir and
SimpleInventory

https://nornir.readthedocs.io/en/stable/tutorials/intro/inventory.html

Also - see the sample 'configuration.ini' file on how to set it up properly

Lastly - this requires that ntc-templates are downloaded to the host running this program:

https://github.com/networktocode/ntc-templates

##ntc-templates
Easiest method is to download and keep the ntc-templates in the home directory of the user running this program.

    git clone https://github.com/networktocode/ntc-templates

Otherwise you can explicitly tell the program (namely Netmiko) where to look for them (example is for Linux):

    export NET_TEXTFSM=/path/to/ntc-templates/templates/
    
More information is here:

https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html

##Usage
Run using the following:

    python -m networkconfigutility [options\files\filters]

Example of current capabilities:

    usage: networkconfigutility [-h] -config path to config file for device(s |
                            -getters GETTERS [GETTERS ...] | -cli command)
                            configuration_file ftype filter

    positional arguments:
      configuration_file    name of configuration file for program itself
      ftype                 type of filter to use
      filter                name of device or group

    optional arguments:
      -h, --help            show this help message and exit
      -config path to config file for device(s)
                            change configuration on a device or groups of devices
      -getters GETTERS [GETTERS ...]
                            use built-in NAPALM getters to retrieve information
      -cli command          use the system CLI to retrieve information

Example execution of the getters looks like such:

    Enter username: test-user
    Input password: 
    napalm_get**********************************************************************
    * test-device ** changed : False ***********************************************
    vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    { 'get_interfaces_ip': { 'Vlan10': { 'ipv4': { '10.96.128.18': { 'prefix_length': 24}}}}}
    ^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returned output is utilized from the Nornir 'print_result()' method