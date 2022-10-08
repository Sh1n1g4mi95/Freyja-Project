#!/usr/bin/python3
import datetime
import os
import sys
import time

path_frejya_arc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path_frejya_arc not in sys.path:
    sys.path.append(path_frejya_arc)

from arc_frejya.lib.frejya_misc import title
from arc_frejya.utils.web_helpers.web_factory import get_web


def main():
    """Main Execution"""
    title()
    # ToDo: usar argparse para poder obtener parámetros de ejecución de forma limpia y sencilla

    print('Started at:', datetime.datetime.now())
    # Prueba 1 de apertura de navegador (sin params)
    print('Prueba 1 de apertura de navegador (sin params) - Chrome (valor por defecto de Frejya)')
    web1 = get_web()
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web1.close()

    print('Prueba 2 de apertura de navegador (con browser) - Edge')
    # Prueba 2 de apertura de navegador (con browser)
    web2 = get_web(browser='Edge')
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web2.close()

    # Prueba 3 de apertura de navegador (con workspace)
    print('Prueba 3 de apertura de navegador (con workspace) - Firefox (valor del workspace)')
    web3 = get_web(workspace='example_project')
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web3.close()

    # Prueba 4 de apertura de navegador (con browser y workspace)
    print('Prueba 4 de apertura de navegador (con browser y workspace) - Edge (valor especificado, ignora workspace)')
    web4 = get_web(browser='Edge', workspace='example_project')
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web4.close()

    print('Ended at:', datetime.datetime.now())


if __name__ == "__main__":
    sys.exit(main())
