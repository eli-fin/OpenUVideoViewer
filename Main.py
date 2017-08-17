# (for py2 compatibility) encoding: utf-8

""" Main module. This is where the application should start from. """

from sys import version as py_ver

# Add modules folder to import path, so modules can be imported.
from sys import path
path.append('modules')

from MainWindow import MainWindow # pylint: disable=import-error,wrong-import-position
import GuiLib # pylint: disable=import-error,wrong-import-position

def main():
    """ Main function """
    if py_ver[0] != '3' and not (py_ver[:2] == '2.' and int(py_ver[2]) >= 6):
        print('This only works on python 2.6+ or 3+')
    else:
        MainWindow()

if __name__ == '__main__':
    try:
        exit(main())
    except Exception as err: # pylint: disable=broad-except
        # Try to show the error in a gui message,
        # otherwise, rethrow the original error.
        # This won't work for exceptions raised within other threads.
        try:
            GuiLib.show_error("Unknown error:\n" + str(err))
        except:
            raise err
