from scapy.layers.l2 import Ether
import socket


# Verifica que la IP dada sea IPv4 valida.
def validIp(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


# Obtiene la direccion MAC de la interfaz
# por defecto del equipo.
def obtMacLcl():
    return Ether().src
