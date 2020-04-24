# Este programa activa 'port forwarding' en Linux.


def activarForwLinux():
    ruta = '/proc/sys/net/ipv4/ip_forward'

    try:
        with open(ruta) as archivo:
            if archivo.read() == '1':
                print('ip_formard activado previamente...')
                exit(0)

        with open(ruta,'w') as archivo:
            print('Activando ip_forwarding...')
            archivo.write('1')
        print('Port forwarding activado...')
    except PermissionError:
        print('No se puede leer el archivo "/proc/sys/net/ipv4/ip_forward"...')
        print('Tiene los permisos suficientes?')
