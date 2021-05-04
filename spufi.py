from com.GUI import GUI

try:
    import logging
    import os
    import ctypes
    import sys
    from com.utils import Utils, ProgramManager
    from com.exceptions import *
    from net.attacks import Attacks
    from net.hostScanner import HostScanner
    from net.cmnNet import CmnNet
    from com.GUI import GUI
except ModuleNotFoundError as e:
    GUI.killWithNoDependencies(e)

if __name__ == '__main__':
    if sys.version_info < (3, 8):
        print('Please, use python 3.8.x')
        exit(-1)

    # It must be an admin console
    try:
        isAdmin = os.getuid() == 0
    except AttributeError:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not isAdmin:
        print('Run this program as admin...')
        exit(-1)

    if len(sys.argv) < 2 or len(sys.argv) > 5:
        GUI.showUsage()
        exit(-1)

    if sys.argv[1] == '-h':
        GUI.showMenu()
        exit(-1)

    # Gets local PC's NICs info
    elif sys.argv[1] == '-NIC':
        info = CmnNet.getLocalNICS()
        print(info, end='')

    # Checks if a host's NIC is in promiscuos mode based on IP
    elif sys.argv[1] == '-chkProm':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -chkProm <ip>')
            exit(-1)

        if CmnNet.chkIsPromiscuousByIP(sys.argv[2].strip()):
            print('Yes')
        else:
            print('No')

    # Gets MAC address of a host based on it's IP
    elif sys.argv[1] == '-macIP':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -macIp <ip>')
            exit(-1)

        ip = sys.argv[2]
        mac = CmnNet.getMACByIP(ip)

        if mac:
            mac = mac.replace('-', ':')
            prov = CmnNet.getNICVendor(mac)  # Try to find NIC vendor
            print(f'{ip} => {mac} ({prov})')
        else:
            print('Couldn\'t get MAC address...')

    # Gets local network hosts
    elif sys.argv[1] == '-s':
        hosts = HostScanner.scanWithARP()

        # Order ascendingly
        Utils.sortListOfObj(hosts, 'host', True)

        print(f'Detected hosts: {len(hosts)}')

        for h in hosts:
            print(f'{h["ip"]} - {h["mac"]}')

    # Poisons ARP table of the router allowing you to inpersonate another host
    elif sys.argv[1] == '-pARP':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -macIp <ip src> <ip src>')
            exit(-1)

        targetIP = sys.argv[2]
        Attacks.ARPpoison(targetIP)

    # Gets name of a host based on IP
    elif sys.argv[1] == '-host':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -p <ip>')
            exit(-1)

        hName = CmnNet.getHostnameByIP(sys.argv[2])

        if hName:
            print(hName)
        else:
            print('Couldn\'t get the hostname')

    else:
        print('Invalid option')

# TODO
# P: Pending
# C: Complete
# A: Abandoned
#
# - (P) Add unit testing.
#
# - (P) Build getHostnameByIP method. (Currently, don't know how to make this).
#
# - (P) Detect user default NIC and set it globally in all network
# related processes (I do not know why this is not working by default).
#
# - (P) Allow user to change MAC address of a NIC.
#
# - (P) Enhance host discovery with alternatives to ARP technique. Maybe TCP SYN
# or other socket oriented techniques. This will ensure most host discovered.
#
# - (C) Tell user to use python > 3.8 . If user is not using it, kill the program.
#
# - (P) Make a mechanism that makes sure the venv is active. If it's not inactive, activate it,
# if it is active, don't do anything. Aditionally, consider killing the venv when the program finishes.
