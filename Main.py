# (for py2 compatibility) encoding: utf-8

""" Main module. This is where the application should start from. """

from sys import version as py_ver
from MainWindow import MainWindow

def main():
    """ Main function """
    if py_ver[0] != '3' and not (py_ver[:2] == '2.' and int(py_ver[2]) >= 6):
        print('This only works on python 2.6 or 3')
    else:
        MainWindow()

if __name__ == '__main__':
    exit(main())
