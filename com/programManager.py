from com.GUI import GUI

try:
    import operator
    import subprocess
    import re
    import sys
    import os
    import ctypes
    from scapy.all import conf
except ModuleNotFoundError as e:
    GUI.killWithNoDependencies(e)


# Responsible of managing some fundamentals parts of the program
class ProgramManager:
    def __init__(self):
        self.mainNIC = None
        self.mainNICName = None

    def getDefaultNICData(self):
        self.mainNIC = self.__getDefaultNIC()
        self.mainNICName = self.__getNICNameFromRawNICData(self.mainNIC)

    def isVenvOn(self):
        prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
        return prefix != sys.prefix

    def isValidPythonVersion(self):
        if sys.version_info < (3, 8):
            return False
        return True

    def isAdminConsole(self):
        isAdmin = False

        try:
            isAdmin = os.getuid() == 0
        except AttributeError:
            isAdmin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        return isAdmin

    # Take the output of conf.route and compare the metrics of every interface. The one that
    # has the lowest value is the current main interface of the system.
    def __getDefaultNIC(self):
        mainInterface = None
        interfaceMetrics = 10000
        interfaces = []
        routes = str(conf.route).split('\n')

        if len(routes) > 0:
            routes.pop(0)

        for item in routes:
            interfaces.append(item.split())

        for item in interfaces:
            metric = int(item[-1])
            if metric < interfaceMetrics:
                interfaceMetrics = metric
                mainInterface = item

        return mainInterface if interfaceMetrics != 10000 else None

    def __getNICNameFromRawNICData(self, data: list):
        # data looks like this (it's supposed to be the output of getDefaultNIC()):
        # ['0.0.0.0', '0.0.0.0', '192.168.3.1', 'Intel(R)', 'Wireless-AC', '9560', '160MHz', '192.168.3.106', '45']
        # Indexes 0,1,2 and -1, -2 are fixed. The other ones are the 'InterfaceDescription' according to the output
        # of powershell's Get-NetAdapter.
        notWantedIndexes = (0, 1, 2, len(data) - 1, len(data) - 2)
        tmp = []
        for i in range(len(data)):
            if i not in notWantedIndexes:
                tmp.append(data[i])

        nicWithLowerMetricName = ' '.join(tmp)

        # Now get the system name of that interface
        p = subprocess.run(['powershell.exe', 'Get-NetAdapter'], capture_output=True)
        netAdaptersOutput = p.stdout.decode('utf-8')
        netAdaptersOutput = netAdaptersOutput.split('\n')

        for item in netAdaptersOutput:
            match = re.search(f'{re.escape(nicWithLowerMetricName)}', item)
            if match:
                # The next regex separates columns assuming everything that's columns are separated
                # from one another with 2 or more whitespaces.
                return re.split('\s{2,}', item)[0]

        return None


# This is a singleton
programMgr = ProgramManager()
