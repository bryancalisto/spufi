import time
import socket
import subprocess
import sys
from json import JSONDecodeError
from pip._vendor import requests
from scapy.config import conf
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether, ARP, getmacbyip
from scapy.layers.inet import ICMP, sr1
from scapy.all import arping
from scapy.sendrecv import srp, send
from com.exceptions import InvalidIPv4Exception
from com.exceptions import NetworkException, InvalidIPv4Exception, NoInternetException


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
            ans, unans = arping(ip, retry=3)
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
            # Send ARP packet to host by IP with an invalid MAC
            resp = srp(Ether(dst='ff:ff:ff:ff:ff:fe')/ARP(pdst=ip), timeout=3, verbose=False)[0]
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
    # DOES NOT WORK YET
    @staticmethod
    def getHostnameByIP(ip):
        PORT = 5353  # Multicast DNS
        for i in range(2):  # Try twice
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, UDP
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow IP address reuse
                s.bind(('224.0.0.251', PORT))
                s.sendall(b'224.0.0.251')
                print('llega')  # DEBUG
                data = s.recv(1024)
                print('Received', repr(data))  # DEBUG
                s.close()
                break
            except:
                raise NetworkException()
