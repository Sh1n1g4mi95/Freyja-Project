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

    # ToDo: Hacer ejemplo de auto para el Cha Cha Slide
    web = get_web()
    print("Esperamos 5 Segundos")
    time.sleep(5)
    web.close()

    print('Ended at:', datetime.datetime.now())


if __name__ == "__main__":
    sys.exit(main())
