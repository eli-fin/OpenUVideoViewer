# (for py2 compatibility) encoding: utf-8

""" This module will handle the HTML """

from lxml import html
import requests
import DataClasses
import GlobalVars
from NetworkLayer import NetworkHandler
import GuiLib

class HtmlHandler(object):
    """ This class will handle all html parsing """
    __is_setup = False


    @classmethod
    def setup(cls):
        """ This is to setup the class. Every class method should call it at first
            (Multiple calls will be ignored) """
        if cls.__is_setup:
            return
        cls.__is_setup = True

        cls.__net = NetworkHandler.get_instance()
        cls.__main_page = cls.__net.get_page(GlobalVars.MAIN_PAGE_LINK)

        # Check if login was successful
        # (The search term is a JS function which only appears if login failed,
        #  or if the login div is there)
        if 'CHECK_VALID()'   in cls.__main_page or \
           '<div id="login"' in cls.__main_page:
            GuiLib.show_error('Login error. Check the config file.')

    @classmethod
    def get_student_name(cls):
        """ This function exceptcts the main_page html return from NetworkHandler
            and returns the student's display name """

        cls.setup()

        tree = html.fromstring(cls.__main_page)
        return tree.find_class('logininfo')[0].find('a').text_content()

    @classmethod
    def get_course_list(cls):
        """ This will return a list of CourseInfo objects found on the main page
            (current semester courses) """

        cls.setup()

        course_list = []

        tree = html.fromstring(cls.__main_page)
        # Current semester courses
        courses_nodes = tree.get_element_by_id('navbar').find('li/ul').findall('li/a[@title]')
        # Previous courses
        courses_nodes += tree.get_element_by_id('navbar').find('.//ul[@class="dropdown-menu"]')\
            .findall('li/a[@title]')

        for course_node in courses_nodes:
            course = DataClasses.CourseInfo()
            course.name = course_node.text_content().split('(')[0].strip()
            course.semester = course_node.text_content().split(course.name)[1].strip()
            course.link = course_node.attrib['href']
            course_list.append(course)

        return course_list

    @classmethod
    def get_video_pages_links_and_number(cls, course_page_link):
        """ Return video pages links and course number for course page link in a tupple """

        cls.setup()

        tree = html.fromstring(cls.__net.get_page(course_page_link))
        # This was added to deal with course pages that have no link to video page
        try:
            return ([link.attrib['href']
                     for link in tree.get_element_by_id('quicklinks_panel').findall('.//a')
                     if link.attrib['href'].startswith('https://opal.openu.ac.il/mod/ouilvideocollection/view.php')],
                    tree.find('.//h1[@class="coursename_header"]').text_content().split(' - ')[1])
        except Exception: # pylint: disable=broad-except
            return "", 'NULL'

    @classmethod
    def get_playlist_list(cls, course_video_pages_links, course_id):
        """ This will return a list of PlaylistInfo objects found on the course video page
            course_id is needed to store it also in PlaylistInfo """

        cls.setup()

        playlist_list = []

        for page_link in course_video_pages_links:
            tree = html.fromstring(cls.__net.get_page(page_link))
            playlist_nodes = tree.get_element_by_id('ovc_collections_list').iter('li')

            for playlist_node in playlist_nodes:
                playlist = DataClasses.PlaylistInfo()
                playlist.title = playlist_node.find('a/span[@data-title]').text_content()
                playlist.c_value = playlist_node.find('a').attrib['c-value']
                playlist.cid = playlist_node.find('a').attrib['cid']
                playlist.mid = playlist_node.find('a').attrib['mid']
                playlist.course_id = course_id
                playlist_list.append(playlist)

        return playlist_list

    @classmethod
    def get_video_list(cls, course_id, curr_playlist_info):
        """ This will return a list of VideoInfo from curr_playlist_info
            course_id and playlist info are needed to make the requests """

        cls.setup()

        video_list = []

        # Get div with all videos
        videos_div = cls.__net.post_page(
            'https://opal.openu.ac.il/mod/ouilvideocollection/actions.php',
            data={
                'cid':curr_playlist_info.c_value,
                'action':'getcollection',
                'course':course_id,
                'context':curr_playlist_info.cid,
                'mid':curr_playlist_info.mid,
                })

        # Response is an 2 items list (as string). Second one always seems to be empty.
        # For some reason, all the closing tags in the response are '\\/', so this fixes it
        for video_div in html.fromstring(eval(videos_div)[0].replace('\\/', '/')).findall('div'): # pylint: disable=eval-used
            video = DataClasses.VideoInfo()
            video.title = video_div.find('div/span[@title]').text_content()
            video.thumb_link = video_div.find('div/div/img').attrib['src']
            video.instructor_name = video_div.find('div/span/span[@user]').text_content()
            # Some times the name is empty
            if video.instructor_name == '':
                video.instructor_name = 'ללא שם'
            video.record_date = video_div.find('div/span/span[@class=\'pl_recorddate\']')\
                                .text_content()
            video.video_playlist_id = video_div.attrib['id'].replace('playlist', '')
            video.course_id = course_id
            video.parent_playlist = curr_playlist_info
            video_list.append(video)

        return video_list

    @classmethod
    def get_video_link(cls, course_id, curr_playlist_info, video_playlist_id):
        """ All args are needed for the request """

        cls.setup()

        req1 = cls.__net.post_page(
            'https://opal.openu.ac.il/mod/ouilvideocollection/actions.php',
            data={
                'action': 'getplaylist',
                'context': curr_playlist_info.cid,
                'playlistid': video_playlist_id,
                'course': course_id,
                'mid': curr_playlist_info.mid
            })
        # Parse json to dict
        # Note: This json has a lot of info about the video properties and lesson info
        response = eval(req1.replace('true', 'True'). # pylint: disable=eval-used
                        replace('false', 'False').replace('null', 'None'))

        return 'https://api.bynetcdn.com/Redirector/openu/manifest/' + response['media']['ar'] + '_mp4/HLS/playlist.m3u8'
