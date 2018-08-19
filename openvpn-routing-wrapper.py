#!/usr/bin/env python3

import ipdb
import sys
import os
import time

class ColorPrint:
    '''
    Origin:
    https://stackoverflow.com/questions/39473297/how-do-i-print-colored-output-with-python-3
    '''

    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)

def get_cmd_from_log(log_line):
    '''
    Converts a line like this:
    Sun Aug 19 12:05:20 2018 /usr/bin/ip link set dev tun0 up mtu 1500
    To this:
    /usr/bin/ip link set dev tun0 up mtu 1500
    '''

    cmd_string = log_line[log_line.find("/usr/bin"):]

    return cmd_string

def main():

    print("\n")
    ColorPrint.print_info("==================================================\n"
                          "You're running OPENVPN ROUTING WRAPPER\n"
                          "See the original bug at\n"
                          "https://community.openvpn.net/openvpn/ticket/1086\n"
                          "==================================================")
    print()

    routing_cmds = []

    for line in sys.stdin:
        print(line, end="")
        
        if "/usr/bin" in line:
            ColorPrint.print_info("---> Recording route command")
            routing_cmds.append(get_cmd_from_log(line))
        
        if "Initialization Sequence Completed" in line:

            wait_seconds = 3
            
            ColorPrint.print_info("Waiting " + str(wait_seconds) + " seconds...")
            time.sleep(wait_seconds)

            ColorPrint.print_warn("RE-EXECUTING ROUTING CMDS")
            
            for cmd in routing_cmds:
                ColorPrint.print_bold(cmd)
                os.system(cmd)

            ColorPrint.print_pass("Wrapping done. Leave me open.")           

        
if __name__ == '__main__':
    main()
