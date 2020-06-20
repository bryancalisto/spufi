import admin
from net.activForwLinux import activarForwLinux
from com import funcionesCom
from net import funcionesNet
import platform
import sys
import ctypes
import os

if __name__ == '__main__':
    # Verificamos si CMD es admin
    try:
        isAdmin = os.getuid() == 0
    except AttributeError:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not isAdmin:
        print('Ejecute este programa con derechos de administrador...')
        exit(-1)

    # Verificamos args.
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        funcionesCom.presentUso()
        exit(0)

    # Mostramos ayuda.
    if sys.argv[1] == '-h':
        funcionesCom.presentAyuda()
        exit(0)

    # Muestra MAC de interfaz local principal.
    elif sys.argv[1] == '-mac':
        mac = funcionesNet.obtMacLcl()
        if mac:
            print(f'MAC: {mac}')
        exit(0)

    # Activar port forwarding en el equipo (Solo Linux).
    elif sys.argv[1] == '-pF':
        os = platform.system()

        if os == "Linux":
            # Activamos port forwarding.
            print('Activando port forwarding...')
            activarForwLinux()
        else:
            print('Configuración disponible sólo para Linux...')
        exit(0)

    # Verificar si la NIC de un equipo esta en modo promiscuo.
    elif sys.argv[1] == '-chkProm':
        if len(sys.argv) != 3:
            print('Uso: spufi.py -chkProm <ip>')
            exit('-1')

        ip = sys.argv[2].strip()
        funcionesNet.chkPromiscIP(ip)

    # Obtiene la direccion MAC de una NIC en base a su IP.
    elif sys.argv[1] == '-macIp':
        if len(sys.argv) != 3:
            print('Uso: spufi.py -macIp <ip>')
            exit(-1)

        ip = sys.argv[2]
        mac = funcionesNet.obtMacIP(ip)

        if mac:
            prov = funcionesNet.proveeNic(mac)  # Tratamos de obtener proveedor
            if prov:
                print(f'La MAC de {ip} es {mac} ({prov})')
            else:
                print(f'La MAC de {ip} es {mac}')
        else:
            print('No se pudo obtener la MAC...')

    # Escanea todos los hosts de la red local.
    elif sys.argv[1] == '-s':
        funcionesNet.escanHostsLcl()


    # Envenena la tabla ARP (Poison ARP) de un host. Necesita IP src y dst.
    elif sys.argv[1] == '-pArp':
        if len(sys.argv) != 3:
            print('Uso: spufi.py -macIp <ip src> <ip src>')
            exit(-1)

        ip1 = sys.argv[2]

        funcionesNet.arpPoison(ip1)

    elif sys.argv[1] == '-p':
        if len(sys.argv) != 3:
            print('Uso: spufi.py -p <ip>')
            exit(-1)

        result = funcionesNet.hostnameXIp(sys.argv[2])

        if result:
            print(result)
        else:
            print('No se pudo obtener hostname')


    else:
        print('Opción inválida')
