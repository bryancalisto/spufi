from com.GUI import GUI

try:
    import re
    from scapy.layers.inet import IP, ICMP, TCP
    from scapy.layers.l2 import Ether, ARP, arping
    from scapy.all import srp, send, sr1, sr
    from com.exceptions import NetworkException
    from net.cmnNet import CmnNet
    from com.programManager import programMgr
except ModuleNotFoundError as e:
    GUI.killWithNoDependencies(e)


class HostScanner:
    @staticmethod
    def scanWithARP():
        hosts = []
        ipPattern = re.compile('\d+\.\d+\.\d+\.')
        hostPattern = re.compile('\d+$')

        try:
            ipPrefix = ipPattern.search(CmnNet.getLocalDefaultIP()).group(0)
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipPrefix + "0/24"), timeout=3, iface=programMgr.mainNICName)

            for snt, rcv in ans:
                hosts.append({"ip": rcv.sprintf(r"%ARP.psrc%"), 'mac': rcv.sprintf(r"%Ether.hwsrc%"),
                              "host": int(hostPattern.search(rcv.sprintf(r"%ARP.psrc%")).group(0))})

        except:
            raise NetworkException()

        return hosts

    def scanWithTCP():
        hosts = []
        ipPattern = re.compile('\d+\.\d+\.\d+\.')
        hostPattern = re.compile('\d+$')

        try:
            ipPrefix = ipPattern.search(CmnNet.getLocalDefaultIP()).group(0)
            ans, unans = sr(IP(dst=ipPrefix + '1')/TCP(dport=80, flags="S"), iface=programMgr.mainNICName, timeout=5)

            i = 0
            for snt, rcv in ans:
                hosts.append({"ip": rcv.sprintf(r"%IP.src%"), 'mac': '',
                              "host": 255 + i})
                i += 1

        except:
            raise NetworkException()

        return hosts
