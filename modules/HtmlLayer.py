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
        # (The search term is a JS function which only appears if login failed)
        if cls.__main_page.find('CHECK_VALID()') != -1:
            GuiLib.show_error('Login error')

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
        courses_nodes += tree.get_element_by_id('navbar').find('li/ul')\
            .findall('li[@class]/ul/li/a[@title]')

        for course_node in courses_nodes:
            course = DataClasses.CourseInfo()
            course.name = course_node.find('div/div[@class=\'mycoursefullname\']')\
                          .text_content().strip()
            course.semester = course_node.find('div/div[@class=\'mycoursesemester\']')\
                              .text_content().strip()
            course.link = course_node.attrib['href']
            course_list.append(course)

        return course_list

    @classmethod
    def get_video_page_link_and_number(cls, course_page_link):
        """ Return video page link and course number for course page link in a tupple """

        cls.setup()

        tree = html.fromstring(cls.__net.get_page(course_page_link))
        # This was added to deal with course pages that have no link to video page
        try:
            return (tree.get_element_by_id('quicklink3')[0].attrib['href'],
                    tree.get_element_by_id('openuheader')[1][0][1][0][0]
                    .text_content().split(' - ')[1])
        except Exception: # pylint: disable=broad-except
            return "", 'NULL'

    @classmethod
    def get_playlist_list(cls, course_video_page_link, course_id):
        """ This will return a list of PlaylistInfo objects found on the course video page
            course_id is needed to store it also in PlaylistInfo """

        cls.setup()

        playlist_list = []

        tree = html.fromstring(cls.__net.get_page(course_video_page_link))
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
            'http://opal.openu.ac.il/mod/ouilvideocollection/actions.php',
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
            'http://opal.openu.ac.il/mod/ouilvideocollection/actions.php',
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
        cdnid = response['cdnid']

        # Get video link (the ie9 part is needed, or a more complicated response,
        # ultimately leeding to an m3u8 file is returned)
        # This also has some basic info about video file
        req2 = cls.__net.get_page('http://opal.openu.ac.il/local/ouil_video/player.php?mediaid='
                                  + cdnid + '&ie9=1')
        # Response html for some reason has '//\' in all closing tags.
        # This data contains a few video quality links (usually 4, it seems)
        # I will extract the standard one
        # (It appears in a seperate place It's usually the third best).
        html_data = html.fromstring(eval(req2)['html'].replace('\\/', '/')) # pylint: disable=eval-used

        # This is the base video link, which leads to a redirector api
        tmp_link = html_data.find('video/source').attrib['src']
        # The network_layer doesn't provide this function, and I only need it here,
        # and also this doesn't require the session, so I just did it here.
        link = requests.get(tmp_link, allow_redirects=False).headers['location']

        return link
