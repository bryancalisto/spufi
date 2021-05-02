from scapy.layers.inet import IP, ICMP, TCP
from scapy.layers.l2 import Ether, ARP, arping
from scapy.all import srp, send, sr1, sr
from com.exceptions import NetworkException
from net.cmnNet import CmnNet
import re


class HostScanner:
    @staticmethod
    def scanWithARP():
        hosts = []

        try:
            ipPattern = re.compile('\d+\.\d+\.\d+\.')
            ipPrefix = ipPattern.search(CmnNet.getLocalDefaultIP()).group(0)
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ipPrefix + "0/24"), timeout=3, iface="Wi-Fi")

            for snt, rcv in ans:
                hosts.append({"ip": rcv.sprintf(r"%ARP.psrc%"), 'mac': rcv.sprintf(r"%Ether.hwsrc%"), host: })

        except:
            raise NetworkException()

        return hosts
