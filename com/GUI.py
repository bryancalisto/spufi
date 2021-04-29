class Colors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'


class GUI():
    @staticmethod
    def yellow(s):
        return f'{Colors.WARNING}{s}{Colors.ENDC}'

    @staticmethod
    def showUsage():
        print(f'\n|--------------------------- {GUI.yellow("Spufi")} ---------------------------|\n')
        print(f'{GUI.yellow("Usage:")} spufi.py <option>')
        print(f'{GUI.yellow("spufi -h:")} to see help menu\n')

    @staticmethod
    def showMenu():
        print(f'\n|--------------------------- {GUI.yellow("Spufi")} ---------------------------|\n')
        print(GUI.yellow('Options:'))
        print(f'\t{GUI.yellow("-h:")}\tShow this help menu.')
        print(f'\t{GUI.yellow("-mac:")}\tShow MAC address of this device default NIC.')
        print(f'\t{GUI.yellow("-macIP:")}\tShow MAC address of a host\'s NIC based on IP.')
        print(f'\t{GUI.yellow("-s:")}\tShow the IP and MAC address of all the network hosts.')
        print(f'\t{GUI.yellow("-pARP:")}\tPoison the ARP table of a host given it\'s IP and some src and dst IP.')
        print(f'\t{GUI.yellow("-host:")}\tShow hostname based on IP.')
        print()
