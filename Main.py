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
    try:
        exit(main())
    except Exception as err:
        # Try to show the error in a gui message,
        # otherwise, rethrow the original error.
        # This won't work for exceptions raised within other threads.
        try:
            from GuiLib import GuiLib
            GuiLib.show_error("Unknown error:\n" + str(err))
        except:
            raise err
