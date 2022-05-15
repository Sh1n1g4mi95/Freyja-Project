from termcolor import colored

__author__ = 'Adrián Rodríguez Carneiro'


def title(color='blue', color2='white', on_color='yellow'):
    print(colored("---------------------------------------------------------------", color, on_color="on_" + on_color))
    print(colored("---------------------------------------------------------------", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("      _________                 ( )                        ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("     |    ____/       ______    ____ ___    ___            ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("     |   |_  ______  / (  ) \   |  | \  \  /  /_____       ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("     |   __||  __  \ |  _____\  |  |  \  \/ _/ \__  \      ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("     |  |   |  | \__\|  |____ __|  |   /  /     / __ \     ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("--", color, on_color="on_" + on_color) + colored("     |__|   |__|      \_____/ \____|  /__/     (______\    ", color2, on_color="on_" + color) + colored("--", color, on_color="on_" + on_color))
    print(colored("---------------------------------------------------------------", color, on_color="on_" + on_color))
    print(colored("------------", color, on_color="on_" + on_color) + colored(" Developed by Adrián Rodríguez Carneiro ", 'green') + colored("-----------", color, on_color="on_" + on_color))
    print(colored("---------------------------------------------------------------", color, on_color="on_" + on_color))


