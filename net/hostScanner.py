from scapy.config import conf
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether, ARP, getmacbyip
from scapy.sendrecv import srp, send
from com.exceptions import NetworkException


class HostScanner:
    @staticmethod
    def scan():
        try:
            ip = IP().src

            ip += '/24'
            arp = ARP(pdst=ip)  # (who has...)
            broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
            pack = broadcast / arp

            resp = srp(pack, timeout=3, verbose=False)[0]

            hosts = []
            for sent, received in resp:
                hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
        except:
            raise NetworkException()

        return hosts
