from net.activForwLinux import activarForwLinux
from com.GUI import GUI
from net import funcionesNet
import sys
import ctypes
import os

if __name__ == '__main__':

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

    # Gets MAC address of the user's default NIC
    elif sys.argv[1] == '-mac':
        mac = funcionesNet.obtMacLcl()
        if mac:
            print(mac)

    # Checks if a host's NIC is in promiscuos mode based on IP
    elif sys.argv[1] == '-chkProm':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -chkProm <ip>')
            exit(-1)

        ip = sys.argv[2].strip()
        funcionesNet.chkPromiscIP(ip)

    # Gets MAC address of a host based on it's IP
    elif sys.argv[1] == '-macIP':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -macIp <ip>')
            exit(-1)

        ip = sys.argv[2]
        mac = funcionesNet.obtMacIP(ip)

        if mac:
            prov = funcionesNet.proveeNic(mac)  # Try to find NIC manufacturer
            if prov:
                print(f'{ip} => {mac} ({prov})')
            else:
                print(f'{ip} => {mac}')
        else:
            print('Couldn\'t get MAC address...')

    # Gets local network hosts
    elif sys.argv[1] == '-s':
        funcionesNet.escanHostsLcl()

    # Poisons ARP table of the router allowing you to inpersonate another host
    elif sys.argv[1] == '-pARP':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -macIp <ip src> <ip src>')
            exit(-1)

        ip1 = sys.argv[2]

        funcionesNet.arpPoison(ip1)

    # Gets name of a host based on IP
    elif sys.argv[1] == '-host':
        if len(sys.argv) != 3:
            print('Usage: spufi.py -p <ip>')
            exit(-1)

        result = funcionesNet.hostnameXIp(sys.argv[2])

        if result:
            print(result)
        else:
            print('Couldn\'t get the hostname')

    else:
        print('Invalid option')
