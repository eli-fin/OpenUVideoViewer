# (for py2 compatibility) encoding: utf-8

""" Various helper functions module """

from threading import Lock
from re import sub
from os import name as os_name
from os import environ
from os import path
from lxml import html
from GlobalVars import GlobalVars

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

            except Exception as err:
                from GuiLib import GuiLib
                GuiLib.show_error('Error parsing config file\n(' + str(err.args) + ')')

    @classmethod
    def set_login_info(cls):
        """ Set login info to GlobalVars.login_data from config file """
        config = cls.get_config()

        try:
            GlobalVars.login_data['p_user'] = config['username']
            GlobalVars.login_data['p_sisma'] = config['password']
            GlobalVars.login_data['p_mis_student'] = config['student_id']
        except KeyError as err:
            from GuiLib import GuiLib
            GuiLib.show_error(err.args[0] + ' missing from config file')


def get_legal_filename(filename):
    """ Return filename after all char not (letter, number, -, ., _, <space>, ())
        replaced by dashes and quotes replaced by double aposrophies """
    return sub('[^\w\d\-_\. \(\)\']', '-', filename.replace('"', '\'\''))

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
        import subprocess
        start_info = subprocess.STARTUPINFO()
        start_info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocess.run(
            ['cmd', '/c', 'explorer', link],
            startupinfo=start_info)
    else:
        import webbrowser
        webbrowser.open(link)

export_mutex = Lock()
def export_to_html(course_info, playlist_index):
    """ This function will export a playlist to a formatted html """
    from GuiLib import GuiLib

    # This could take some time, because of the lazy loading of the video links
    GuiLib.show_notice('Starting to generate\nThis might take a moment'
                       ' (depending on the number of videos)')

    try:
        import io # for py2 utf-8 compatibility
        html_template = io.open('resources/_html_export_tepmlate_.html', encoding='utf-8').read()
    except Exception:
        GuiLib.show_error('Can\'t open html template file')

    # Set basic info, which can be done by simple replacing instead of parsing
    html_template =\
        html_template.replace('_course_title_', course_info.name + ' ' + course_info.semester)
    html_template =\
        html_template.replace('_course_name_', course_info.name + ' ' +
                              course_info.semester + ' (' + course_info.course_number + ')')
    html_template = html_template.replace('_course_page_link_', course_info.link)
    html_template = html_template.replace('_playlist_name_',
                                          course_info.playlist_list[playlist_index].title)

    # Parse page, get base (template element), remove it and use it to create new elements
    html_obj = html.fromstring(html_template)
    video_base_element = html_obj.get_element_by_id('video_container')
    video_base_element_text = html.tostring(video_base_element, encoding='unicode')
    video_container = video_base_element.getparent()
    video_container.remove(video_base_element)

    # Insert all the videos
    for video_info in course_info.playlist_list[playlist_index].video_list:
        # Reset
        video_element_text = video_base_element_text
        # Replacements
        video_element_text = video_element_text.replace('_video_title_', video_info.title)
        video_element_text = video_element_text.replace('_thumb_link_', video_info.thumb_link)
        video_element_text =\
            video_element_text.replace('_instructor_name_', video_info.instructor_name)
        video_element_text = video_element_text.replace('_record_date_', video_info.record_date)
        video_element_text =\
            video_element_text.replace('_video_download_link_', video_info.video_link)
        video_container.append(html.fromstring(video_element_text))

    # Save file (this part is mutexes, to avoid complications)
    export_mutex.acquire()
    try:
        # Get file name
        file_name = 'OpenU course #' + course_info.course_number + '.html'
        folder = get_download_folder()
        full_file_name = get_free_filename(folder + file_name)
        io.open(full_file_name, 'w', encoding='utf-8').\
            write(html.tostring(html_obj, encoding='unicode'))
        GuiLib.show_notice('File "' + full_file_name.split('/')[-1].split('\\')[-1].
                           rsplit('.', 1)[0] + '" created in folder "' + folder + '"')
    except Exception as err:
        GuiLib.show_error('Error generating file\n' + str(err.args))
    export_mutex.release()
