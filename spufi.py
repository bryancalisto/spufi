from com.GUI import GUI

try:
    import logging
    import os
    import sys
    from com.utils import Utils
    from com.exceptions import *
    from net.attacks import Attacks
    from net.hostScanner import HostScanner
    from net.cmnNet import CmnNet
    from com.GUI import GUI
    from com.programManager import programMgr
except ModuleNotFoundError as e:
    GUI.killWithNoDependencies(e)

if __name__ == '__main__':
    if not programMgr.isVenvOn():
        print('Please, activate the virtual environment')
        exit(-1)

    if not programMgr.isValidPythonVersion():
        print('Please, use python 3.8.x')
        exit(-1)

    # It must be an admin console
    if not programMgr.isAdminConsole():
        print('Run this program as admin...')
        exit(-1)

    if len(sys.argv) < 2 or len(sys.argv) > 5:
        GUI.showUsage()
        exit(-1)

    # We need to know what is the default NIC
    programMgr.getDefaultNICData()
    if not programMgr.mainNIC or not programMgr.mainNICName:
        print('Could\'t get this device\'s default NIC data')
        exit(-1)

    ### PROGRAM OPTIONS ###

    # Shows help menu
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
        ips = []
        hostsARP = HostScanner.scanWithARP()
        hostsTCP = HostScanner.scanWithTCP()
        hosts = hostsARP + hostsTCP
        # Remove repeated hosts
        i = 0
        for h in hosts:
            if h['ip'] in ips:
                del hosts[i]
            ips.append(h['ip'])
            i += 1

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

        CmnNet.getHostnameByIP(sys.argv[2])

    # Lets user change the MAC address of a NIC
    elif sys.argv[1] == '-chMAC':
        print('Beware that this function is supported by just some NICs')
        if len(sys.argv) != 4:
            print('Usage: spufi.py -chMAC <NIC_NAME> <NEW_MAC>')
            exit(-1)

        try:
            CmnNet.changeMAC(sys.argv[2], sys.argv[3])
        except InvalidMACException as e:
            print(e)
            exit(-1)
        except SubprocessException as e:
            print(e)
            exit(-1)
    else:
        print('Invalid option')

# TODO
# P: Pending
# C: Complete
# A: Abandoned
#
# - (P) Enhance host discovery with alternatives to ARP technique. Maybe TCP SYN
# or other socket oriented techniques. This will ensure most host discovered.
