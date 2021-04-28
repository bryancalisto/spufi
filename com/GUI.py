class GUI:
    @staticmethod
    def showUsage(self):
        print(u'Usage: spufi.py <option>')
        print('*"spufi -h" to see help menu')

    @staticmethod
    def showMenu(self):
        print('\t|----- Spufi -----|')
        print('Options:')
        print(u'\t-h: Show this help menu.')
        print(u'\t-mac: Show MAC address of this device default NIC.')
        print(u'\t-pf: Activate port forwarding (Linux only).')
        print(u'\t-macIp: Show MAC address of a host\'s NIC based on IP.')
        print(u'\t-s: Show the IP and MAC address of all the network hosts.')
        print(u'\t-pArp: Poison the ARP table of a host given it\'s IP and some src and dst IP.')
        print(u'\t-p: Show hostname based on IP.')
