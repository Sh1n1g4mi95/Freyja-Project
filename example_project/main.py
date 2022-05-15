import datetime
import os
import sys
import time

path_frejya_arc = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if path_frejya_arc not in sys.path:
    sys.path.append(path_frejya_arc)

from arc_frejya.lib.frejya_misc import title
from arc_frejya.utils.web_helpers.web_factory import get_web


if __name__ == "__main__":
    """Main Execution"""
    # ToDo: hacer argparse para poder obtener parámetros de ejecución de forma limpia y sencilla
    title()

    print('Started at:', datetime.datetime.now())
    # Prueba 1 de apertura de navegador (sin params)
    web1 = get_web()
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web1.close()

    # Prueba 2 de apertura de navegador (con browser)
    web2 = get_web(browser='chrome')
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web2.close()

    # Prueba 2 de apertura de navegador (con workspace)
    web3 = get_web(workspace='example_project')
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web3.close()

    # Prueba 3 de apertura de navegador (con browser y workspace)
    # web4 = get_web(browser='firefox', workspace='example_project')
    # print("Esperamos 5 Segundos")
    # Nos devuelve que no existe el driver (de momento no se ha implementado la descarga automática para Firefox)



    print('Ended at:', datetime.datetime.now())
