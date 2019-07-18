#!/usr/bin/env python3

from nornir import InitNornir
import getpass
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F


class NornirHandler(object):
    def __init__(self, host_file, group_file, defaults_file):
        self.host_file = host_file
        self.group_file = group_file
        self.defaults_file = defaults_file

    # Initialize the Nornir object and apply filtering as needed
    def base_object(self, device_filter=None, group_filter=None):
        nr = InitNornir(core={"num_workers": 100},
                        inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory",
                                   "options": {"host_file": self.host_file,
                                               "group_file": self.group_file,
                                               "defaults_file": self.defaults_file}})

        self.set_creds(nr)  # Prompt for username/password then set defaults to it

        if device_filter is not None:  # Filters based on name (if the name contains the string)
            device = nr.filter(F(name__contains=device_filter))
            return device
        elif group_filter is not None:  # Filters based on group (if the group contains the string)
            group = nr.filter(F(groups__contains=group_filter))
            return group
        else:  # Will use all hosts in the inventory
            return nr

    # Use NAPALM's feature to complete a dry run
    def dry_run(self, task, config_filename):
        result = task.run(task=networking.napalm_configure,
                          dry_run=True,
                          filename=config_filename,
                          replace=False)

        if task.data.failed_hosts:  # Any failed hosts will be returned and printed at the bottom of the result
            return print_result(result), print(f'\nfailed hosts: {task.data.failed_hosts}')
        else:
            return print_result(result)

    # Uses Netmiko's config sending from a file to complete change
    def send_config(self, task, config_filename):
        result = task.run(task=networking.netmiko_send_config,
                          config_file=config_filename)

        if task.data.failed_hosts:
            return print_result(result), print(f'\nfailed hosts: {task.data.failed_hosts}')
        else:
            return print_result(result)

    # Uses built-in NAPALM's getters
    def getters(self, task, getters):
        result = task.run(task=networking.napalm_get,
                          getters=getters)

        if task.data.failed_hosts:
            return print_result(result), print(f'\nfailed hosts: {task.data.failed_hosts}')
        else:
            return print_result(result)

    # Run CLI commands against a device or group of devices using Netmiko
    def cli(self, task, cli):
        result = task.run(task=networking.netmiko_send_command,
                          command_string=cli,
                          use_textfsm=True)

        if task.data.failed_hosts:
            return print_result(result), print(f'\nfailed hosts: {task.data.failed_hosts}')
        else:
            return print_result(result)

    # Set default credentials for session. Host level credentials will be used first
    def set_creds(self, nr):
        username = input('Enter username: ')
        password = getpass.getpass('Input password: ')

        nr.inventory.defaults.username = username
        nr.inventory.defaults.password = password
