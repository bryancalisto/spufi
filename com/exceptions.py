class InvalidIPv4Exception(Exception):
    def __init__(self, ip):
        self.ip = ip


class InvalidMACException(Exception):
    def __init__(self, mac):
        self.mac = mac

    def __str__(self):
        return f"'{self.mac}' is not a valid MAC address"


class NetworkException(Exception):
    def __str__(self):
        return 'Got a problem with the network'


class NoInternetException(Exception):
    def __str__(self):
        return 'Got an Internet exception'


class SubprocessException(Exception):
    def __str__(self, e):
        return 'Got a subprocess error: ' + e
