
from networkconfigutility import NornirHandler
import configparser
import sys
import argparse


def main():

    # Setup argument parsers
    my_parser = argparse.ArgumentParser(prog='networkconfigutility')

    group = my_parser.add_mutually_exclusive_group(required=True)  # Only allow one type to be done at a time
    group.add_argument('-config', metavar='path to config file for device(s)',
                       help='change configuration on a device or group of devices')
    group.add_argument('-merge', metavar='path to config file for device(s)',
                       help='merge a configuration to a device or group of devices')
    group.add_argument('-replace', metavar='path to config file for device(s)',
                       help='replace a configuration on a device or group of devices')
    group.add_argument('-getters', nargs='+', help='use built-in NAPALM getters to retrieve information')
    group.add_argument('-cli', metavar='command', help='use the system CLI to retrieve information')

    # Setup optional, extra arguments for getters or running additional CLI commands
    group_2 = my_parser.add_mutually_exclusive_group()
    group_2.add_argument('-getters_extra', nargs='+', help='optional, additional getters to use')
    group_2.add_argument('-cli_extra', metavar='command', help='optional, additional CLI to retrieve information')

    # Required arguments - program's config file, filter type and the filter itself
    my_parser.add_argument('configuration_file', help='name of configuration file for program itself')
    my_parser.add_argument('ftype', metavar='ftype', choices=['group', 'name'], help='type of filter to use')
    my_parser.add_argument('filter', help='name of device or group')

    args = my_parser.parse_args()

    push_config = args.config
    merge_config = args.merge
    replace_config = args.replace
    getters = args.getters
    cli = args.cli
    getters_extra = args.getters_extra
    cli_extra = args.cli_extra
    nornir_filter = args.filter
    nornir_ftype = args.ftype

    # Set up program configuration by reading from file
    config_file = args.configuration_file
    config = configparser.ConfigParser()
    config.read(config_file)
    nornir_stuff = config['Config']
    host_file = nornir_stuff.get('host_file')
    group_file = nornir_stuff.get('group_file')
    defaults_file = nornir_stuff.get('defaults_file')

    # Spawn Nornir object to be used in other tasks/functions
    all_tasks = NornirHandler(host_file, group_file, defaults_file)

    if nornir_ftype == 'name':  # Verify if filtering by name or by group (uses 'F' type on backend)
        task = all_tasks.base_object(device_filter=nornir_filter)
    elif nornir_ftype == 'group':
        task = all_tasks.base_object(group_filter=nornir_filter)
    else:
        print('\nPlease specify either name or group for ftype\n')
        sys.exit()

    # Configuration pushing completed here using Netmiko
    if push_config:

        while True:  # Prompt if wanting to do a dry run first
            dry_run = input('\nPerform a dry run [y/n]? \n')
            if dry_run.lower() == 'y':
                all_tasks.dry_run(task, push_config)
                print('\nDry run completed\n')

                while True:  # Dry run complete, prompt if would like to push configuration to production
                    push = input('\nPush configuration now to device(s) [y/n]? \n')
                    if push.lower() == 'y':
                        all_tasks.send_config(task, push_config)
                        if getters_extra:
                            all_tasks.getters(task, getters_extra)
                        elif cli_extra:
                            all_tasks.cli(task, cli_extra)
                        sys.exit()
                    elif push.lower() == 'n':
                        sys.exit()
                    else:
                        print('\nSpecify either "y" or "n"\n')
            elif dry_run.lower() == 'n':
                all_tasks.send_config(task, push_config)
                if getters_extra:
                    all_tasks.getters(task, getters_extra)
                elif cli_extra:
                    all_tasks.cli(task, cli_extra)
                sys.exit()
            else:
                print('\nSpecify either "y" or "n"\n')

    # Merge a configuration using NAPALM
    elif merge_config:
        while True:  # Prompt if wanting to do a dry run first
            dry_run = input('\nPerform a dry run [y/n]? \n')
            if dry_run.lower() == 'y':
                all_tasks.dry_run(task, merge_config)
                print('\nDry run completed\n')

                while True:  # Dry run complete, prompt if would like to push configuration to production
                    push = input('\nPush configuration now to device(s) [y/n]? \n')
                    if push.lower() == 'y':
                        all_tasks.merge_config(task, merge_config)
                        if getters_extra:
                            all_tasks.getters(task, getters_extra)
                        elif cli_extra:
                            all_tasks.cli(task, cli_extra)
                        sys.exit()
                    elif push.lower() == 'n':
                        sys.exit()
                    else:
                        print('\nSpecify either "y" or "n"\n')
            elif dry_run.lower() == 'n':
                all_tasks.merge_config(task, merge_config)
                if getters_extra:
                    all_tasks.getters(task, getters_extra)
                elif cli_extra:
                    all_tasks.cli(task, cli_extra)
                sys.exit()
            else:
                print('\nSpecify either "y" or "n"\n')

    # Replace a configuration using NAPALM
    elif replace_config:

        if nornir_ftype == 'group':
            print('\n*' * 79)
            print('WARNING: Filtering method is set to "group". Multiple devices may have their configuration replaced')
            print('*' * 79)

        while True:  # Prompt if wanting to do a dry run first
            dry_run = input('\nPerform a dry run [y/n]? \n')
            if dry_run.lower() == 'y':
                all_tasks.dry_run_replace(task, replace_config)
                print('\nDry run completed\n')

                while True:  # Dry run complete, prompt if would like to push configuration to production
                    push = input('\nPush configuration now to device(s) [y/n]? \n')
                    if push.lower() == 'y':
                        all_tasks.replace_config(task, replace_config)
                        if getters_extra:
                            all_tasks.getters(task, getters_extra)
                        elif cli_extra:
                            all_tasks.cli(task, cli_extra)
                        sys.exit()
                    elif push.lower() == 'n':
                        sys.exit()
                    else:
                        print('\nSpecify either "y" or "n"\n')
            elif dry_run.lower() == 'n':
                all_tasks.replace_config(task, replace_config)
                if getters_extra:
                    all_tasks.getters(task, getters_extra)
                elif cli_extra:
                    all_tasks.cli(task, cli_extra)
                sys.exit()
            else:
                print('\nSpecify either "y" or "n"\n')

    elif getters:  # Will take list of supported NAPALM getters and return the output w/ print_result()
        all_tasks.getters(task, getters)

    elif cli:  # Will take single command to run on device using TextFSM and print_result()
        all_tasks.cli(task, cli)

    else:  # Added just in case. Arguments are set as required so will return instructions instead
        print('\nNo arguments given, exiting\n')
        sys.exit()


if __name__ == '__main__':
    main()
