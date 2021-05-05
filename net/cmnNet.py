from com.GUI import GUI

try:
    import re
    import time
    import socket
    import subprocess
    import sys
    from json import JSONDecodeError
    import requests
    from scapy.config import conf
    from scapy.layers.inet import IP
    from scapy.layers.l2 import Ether, ARP
    from scapy.layers.inet import ICMP, sr1
    from scapy.all import arping
    from scapy.sendrecv import srp, send
    from com.exceptions import InvalidIPv4Exception
    from com.exceptions import NetworkException, InvalidIPv4Exception, NoInternetException
    from com.programManager import programMgr
except e:
    GUI.killWithNoDependencies(e)


### Common network operations ###
class CmnNet:

    @staticmethod
    def getDefaultGatewayIP():
        try:
            return conf.route.route("0.0.0.0")[2]
        except:
            raise NetworkException()

    @staticmethod
    def isValidIP(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def getLocalNICS():
        p = subprocess.run(['powershell.exe', 'Get-NetAdapter'], capture_output=True)
        return p.stdout.decode('utf-8')

    @staticmethod
    def getLocalDefaultIP():
        return ARP().psrc

    @staticmethod
    def getMACByIP(ip):
        try:
            ans, unans = arping(ip, retry=3, iface=programMgr.mainNICName)
            for snd, rcv in ans:
                return rcv.sprintf(r"%Ether.src%")

            subprocess.run(['powershell.exe', f'ping {ip}'], capture_output=False, shell=False)
            p = subprocess.run(['powershell.exe', f'arp -a | findstr {ip}'], capture_output=True)
            arpInfo = p.stdout.decode('utf-8').split()

            if len(arpInfo) > 1:
                return arpInfo[1]

            return None
        except:
            raise NetworkException()

    @staticmethod
    def chkIsPromiscuousByIP(ip):
        # Validamos IP.
        if not isValidIP(ip):
            raise InvalidIPv4Exception(ip)

        try:
            # Send ARP packet to host by IP with an practically not existant MAC
            resp = srp(Ether(dst='ff:ff:ff:ff:ff:fe')
                       / ARP(pdst=ip), timeout=3, verbose=False, iface=programMgr.mainNICName)[0]
        except:
            raise NetworkException()

        # If there's a response, promisc mode is active
        if resp:
            return True
        else:
            return False

    # Tries to find a NIC's vendor on third party resources
    @staticmethod
    def getNICVendor(mac):
        try:
            url = 'https://www.macvendorlookup.com/oui.php?mac=' + mac  # Gets JSON with NIC vendor data
            # print(url) #DEBUG
            data = requests.get(url).json()[0]
            # print(data['company'] + ' - ' + data['country']) #DEBUG
            return data['company'] + ' - ' + data['country']
        except JSONDecodeError:
            return 'Vendor not detected'

    # Gets hostname by IP
    # PROVISIONAL SOLUTION (it actually shows the hostname in the result of the command)... Don't know how to solve it yet
    @staticmethod
    def getHostnameByIP(ip):
        try:
            # Hostname is shown when calling this method
            arping(ip, retry=3, iface=programMgr.mainNICName)
            return None
        except:
            raise NetworkException()
