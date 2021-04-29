class InvalidIPv4Exception(Exception):
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return f"'{self.ip}' is not a valid IPv4 address"


class NetworkException(Exception):
    def __str__(self):
        return 'Got a problem with the network'


class NoInternetException(Exception):
    def __str__(self):
        return 'Got an Internet exception'
