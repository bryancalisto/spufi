from net.activForwLinux import activarForwLinux
from com import funcionesCom
from net import funcionesNet
import platform
import sys

if __name__ == '__main__':
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
    elif sys.argv[1] == '-pf':
        os = platform.system()
        print(f'Sistema operativo {os} detectado...')

        # Activamos port forwarding.
        print('Activando port forwarding...')

        if os == "Linux":
            activarForwLinux()
        else:
            print('Configuracion disponible solo para Linux')

        exit(0)
