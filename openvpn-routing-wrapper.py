#!/usr/bin/env python3

import ipdb
import sys
import subprocess
import time

def execute(cmd):
    '''
    Origin: https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running

    Arguments:
    cmd - A list with the command and its arguments in it.
    '''
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def get_cmd_from_log(log_line):
    '''
    Converts a line like this:
    Sun Aug 19 12:05:20 2018 /usr/bin/ip link set dev tun0 up mtu 1500
    To this:
    ["/usr/bin/ip", "link", "set", "dev", "tun0", "up", "mtu", "1500"]
    '''

    cmd_string = log_line[log_line.find("/usr/bin"):]
    cmd = cmd_string.split()

    return cmd

def main():
    print("==================================================\n"
          "You're running OPENVPN ROUTING WRAPPER\n"
          "See the original bug at\n"
          "https://community.openvpn.net/openvpn/ticket/1086\n"
          "==================================================\n")

    exec_cmd = sys.argv[1:]   
    print("Executing: ", end="")
    print(*exec_cmd)

    routing_cmds = []

    for line in execute(exec_cmd):
        if "/usr/bin" in line:
            routing_cmds.append(get_cmd_from_log(line))
        
        if "Initialization Sequence Completed" in line:

            wait_seconds = 3
            
            print("Waiting " + wait_seconds + " seconds...")
            time.sleep(wait_seconds)

            print("RE-EXECUTING ROUTING CMDS")
            
            for cmd in routing_cmds:
                os.system(cmd)

            print("Wrapping done. Leave me open.")
            
        print(line, end="")

        
if __name__ == '__main__':
    main()
