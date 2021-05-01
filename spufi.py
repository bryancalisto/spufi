from com.GUI import GUI
from net.cmnNet import CmnNet
from net.hostScanner import HostScanner
from net.attacks import Attacks
import sys
import ctypes
import os
import logging
from com.exceptions import *

if __name__ == '__main__':
    logging.getLogger('scrapy').propagate = False

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
        hosts = HostScanner.scan()
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
