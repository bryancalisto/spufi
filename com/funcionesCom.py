# Aqui se presentan varias funciones de uso comun.

def presentUso():
    print(u'Uso: spufi.py <opción>')
    print('* Si desea ver el menu de ayuda, ingrese "spufi -h"')


def presentAyuda():
    print('\t|----- Spufi -----|')
    print('Opciones:')
    print(u'\t-h: Presenta este menú de ayuda.')
    print(u'\t-mac: Muestra MAC de interfaz local por defecto.')
    print(u'\t-pf: Activa port forwarding (solo Linux).')
    print(u'\t-macIp: Obtiene la MAC de una NIC dada su IP.')
    print(u'\t-s: Escanea la IP y MAC de todos los hosts de la red.')
    print(u'\t-pArp: Poisonea la tabla ARP de un equipo destino dada IP src y dst.')
    print(u'\t-p: Muestra hostname de una IP.')
