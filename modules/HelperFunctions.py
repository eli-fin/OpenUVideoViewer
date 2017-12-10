# (for py2 compatibility) encoding: utf-8

""" Various helper functions module """

import subprocess
import webbrowser
import io
from threading import Lock
from re import sub
from os import name as os_name
from os import environ
from os import path
import GlobalVars
import GuiLib

class HelperFunctions(object):
    """ Helper functions for program """

    # This will hold the config
    config = None

    @classmethod
    def get_config(cls):
        """ This will parse the config file and return a dictionary of the settings """

        # Config file format:
        #   Line beginning with a # is a comment
        #   Each line is <key>:<value>
        #   Multiline values not allowed
        #   Spaces befoer/after keys/values will be ignored
        #   If a key is repeated, the last one will override

        if cls.config is None:
            try:
                config_lines = open('config').readlines()
                # Filter empty and comment lines
                config_lines = list(filter(
                    lambda line: line.strip() != '' and line.strip()[0] != '#', config_lines))

                cls.config = {}
                for line in config_lines:
                    cls.config[line.split(':')[0].strip()] = line.split(':')[1].strip()

                return cls.config

            except Exception as err: # pylint: disable=broad-except
                GuiLib.show_error('Error parsing config file\n(' + str(err.args) + ')')

    @classmethod
    def set_login_info(cls):
        """ Set login info to GlobalVars.LOGIN_DATA from config file """
        config = cls.get_config()

        try:
            GlobalVars.LOGIN_DATA['p_user'] = config['username']
            GlobalVars.LOGIN_DATA['p_sisma'] = config['password']
            GlobalVars.LOGIN_DATA['p_mis_student'] = config['student_id']
        except KeyError as err:
            GuiLib.show_error(err.args[0] + ' missing from config file')


def get_legal_filename(filename):
    """ Return filename after all char not (letter, number, -, ., _, <space>, ())
        replaced by dashes and quotes replaced by double aposrophies """
    return sub('[^\w\d\-_\. \(\)\']', '-', filename.replace('"', '\'\'')) # pylint: disable=anomalous-backslash-in-string

def get_download_folder():
    """ Get cross platform download folder (ending with a slash) """
    # Windows
    if os_name == 'nt':
        return environ['UserProfile']+'\\Downloads\\'
    return environ['HOME'] + '/Downloads/'

def cross_platform_hebrew(hebrew_text):
    """ Returns inverted text for linux and unchanged text for windows """
    # Windows
    if os_name == 'nt':
        return hebrew_text
    return hebrew_text[::-1]

def get_free_filename(file_path):
    """ This function will check if the path is free, otherwise, it will add '(n)'
        until 'file_path (n)' is free and return it """
    num = 1
    tmp_path = file_path
    while path.exists(tmp_path):
        tmp_path = file_path.rsplit('.', 1)[0] +\
                   ' (' + str(num) + ').' + file_path.rsplit('.', 1)[1]
        num += 1

    return tmp_path

def open_link_in_browser(link):
    """ This function will open the link in default browser.
        Link must start with protocol (http and https are supported)
        Link cannot have spaces. """

    if not (link.startswith('http://') or link.startswith('https://')) or not link.find(' ') == -1:
        return

    if os_name == 'nt':
        start_info = subprocess.STARTUPINFO()
        start_info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocess.run(
            ['cmd', '/c', 'explorer', link],
            startupinfo=start_info)
    else:
        webbrowser.open(link)
