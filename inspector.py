#!/bin/env python3
import sys
import socket
import subprocess
import ipaddress
from argparse import ArgumentParser, SUPPRESS

header = r"""
.__                                     __
|__| ____   ____________   ____   _____/  |_  ___________
|  |/    \ /  ___/\____ \_/ __ \_/ ___\   __\/  _ \_  __ \
|  |   |  \\___ \ |  |_> >  ___/\  \___|  | (  <_> )  | \/
|__|___|  /____  >|   __/ \___  >\___  >__|  \____/|__|
        \/     \/ |__|        \/  𝘣𝘺 \/  𝘤𝘶𝘳𝘷𝘵𝘥

"""


def argument_parser():
    parser = ArgumentParser(add_help=False)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-i', '--ip',
                          metavar='IP', required=True,
                          help='target IP address')

    optional.add_argument('-n', '--min', nargs="?",
                          metavar='PORT', type=int, default=1,
                          help='minimum port in scanning range (default = 1)')
    optional.add_argument('-x', '--max', nargs="?",
                          metavar='PORT', type=int, default=65535,
                          help='maximum port in scanning range (default = 65535)')
    optional.add_argument('-h', '--help',
                          action='help', default=SUPPRESS,
                          help='show this help message and exit')

    args = parser.parse_args()
    target = args.ip
    port_minimum = args.min
    port_maximum = args.max
    return target, port_minimum, port_maximum


def validation(target):
    """Checks entered IP address"""
    try:
        valid = ipaddress.ip_address(target)
        ping = subprocess.call(  # checks if the host is alive
            ["ping", "-c", "1", target],
            stdout=open('/dev/null', 'w'),
            stderr=subprocess.STDOUT
        )

        if ping == 0:
            print(f"{header}")
            return target
        else:
            print(f"{target} didn't respond.")
            sys.exit()
    except ValueError:
        print(f"IP address {target} isn't valid")
        sys.exit()


'''Port scanning'''
target, port_minimum, port_maximum = argument_parser()
validation(target)
try:
    for port in range(port_minimum, port_maximum):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = soc.connect_ex((target, port))  # return an error indicator
        if result == 0:
            print(f"Open {target}:{port}")
        soc.close()

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()
