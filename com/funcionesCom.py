# Aqui se presentan varias funciones de uso comun.

def presentUso():
    print('Uso: spufi.py <opcion>')
    print('* Si desea ver el menu de ayuda, ingrese "spufi -h"')


def presentAyuda():
    print('\t|----- Spufi -----|')
    print('Opciones:')
    print(u'\t-h: Presenta este menú de ayuda.')
    print(u'\t-mac: Muestra MAC de interfaz local por defecto.')
    print(u'\t-pf: Activa port forwarding (solo Linux).')
