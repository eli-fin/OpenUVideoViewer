# (for py2 compatibility) encoding: utf-8
""" Classes to hold information """

import HtmlLayer

class CourseInfo(object): # pylint: disable=too-many-instance-attributes
    """ Course info """

    def __init__(self):
        self._name = None
        self._semester = None
        self._link = None
        self._video_pages_links = None
        self._course_number = None
        self._id = None
        self._playlist_list = None

    # Course name (in hebrew)
    @property
    def name(self):
        """ Getter """
        return self._name
    @name.setter
    def name(self, value):
        """ Setter """
        self._name = value

    # Course semester (in hebrew)
    @property
    def semester(self):
        """ Getter """
        return self._semester
    @semester.setter
    def semester(self, value):
        """ Setter """
        self._semester = value

    # Link to course site
    @property
    def link(self):
        """ Getter """
        return self._link
    @link.setter
    def link(self, value):
        """ Setter """
        self._link = value

    # Tupple of links to course video pages
    # (Some courses have more than one video page)
    @property
    def video_pages_links(self):
        """ Getter """
        # Lazy loading implementation (both values loading are tied)
        if self._video_pages_links is None:
            self._video_pages_links, self._course_number =\
                HtmlLayer.HtmlHandler.get_video_pages_links_and_number(self.link)
        return self._video_pages_links
    @video_pages_links.setter
    def video_pages_links(self, value):
        """ Setter """
        self._video_pages_links = value

    @property
    def course_number(self):
        """ Getter """
        # Lazy loading implementation (both values loading are tied)
        if self._course_number is None:
            self._video_pages_links, self._course_number = \
                HtmlLayer.HtmlHandler.get_video_pages_links_and_number(self.link)
        return self._course_number
    @course_number.setter
    def course_number(self, value):
        """ Setter """
        self._course_number = value

    # Course ID (extracted from link)
    @property
    def id(self): # pylint: disable=invalid-name
        """ Getter """
        # Split vars from links using '?', then split all key:values using '=',
        # search for id key and return value
        return list(filter(
            lambda var: var.split('=')[0] == 'id',
            self.link.split('?')[1].split('&')))[0].split('=')[1]

    # Course playlist list
    @property
    def playlist_list(self):
        """ Getter """
        # Lazy loading implementation
        if self._playlist_list is None:
            self._playlist_list = \
                HtmlLayer.HtmlHandler.get_playlist_list(self.video_pages_links, self.id)
        return self._playlist_list
    @playlist_list.setter
    def playlist_list(self, value):
        """ Setter """
        self._playlist_list = value

class PlaylistInfo(object): # pylint: disable=too-many-instance-attributes
    """ Playlist info """

    def __init__(self):
        self._title = None
        self._c_value = None
        self._cid = None
        self._mid = None
        self._course_id = None
        self._video_list = None

    # Playlist title (in hebrew)
    @property
    def title(self):
        """ Getter """
        return self._title
    @title.setter
    def title(self, value):
        """ Setter """
        self._title = value

    # c_value attribute
    @property
    def c_value(self):
        """ Getter """
        return self._c_value
    @c_value.setter
    def c_value(self, value):
        """ Setter """
        self._c_value = value

    # cid attribute
    @property
    def cid(self):
        """ Getter """
        return self._cid
    @cid.setter
    def cid(self, value):
        """ Setter """
        self._cid = value

    # mid attribute
    @property
    def mid(self):
        """ Getter """
        return self._mid
    @mid.setter
    def mid(self, value):
        """ Setter """
        self._mid = value

    # Course ID
    @property
    def course_id(self):
        """ Getter """
        return self._course_id
    @course_id.setter
    def course_id(self, value):
        """ Setter """
        self._course_id = value

    # Playlist video list
    @property
    def video_list(self):
        """ Getter """
        # Lazy loading implementation
        if self._video_list is None:
            self._video_list = \
                HtmlLayer.HtmlHandler.get_video_list(self.course_id, self)
        return self._video_list
    @video_list.setter
    def video_list(self, value):
        """ Setter """
        self._video_list = value

class VideoInfo(object): # pylint: disable=too-many-instance-attributes
    """ Video Info """

    def __init__(self):
        self._title = None
        self._thumb_link = None
        self._instructor_name = None
        self._record_date = None
        self._video_playlist_id = None
        self._video_link = None
        self._course_id = None
        self._parent_playlist = None

    # Video title (in hebrew)
    @property
    def title(self):
        """ Getter """
        return self._title
    @title.setter
    def title(self, value):
        """ Setter """
        # The decode was needed in py2, probably because text had a ' in it,
        # but py3 doesn't have the decode method
        try:
            self._title = value.decode('unicode-escape')
        except AttributeError:
            self._title = value

    # Video thumbnail image link
    @property
    def thumb_link(self):
        """ Getter """
        return self._thumb_link
    @thumb_link.setter
    def thumb_link(self, value):
        """ Setter """
        self._thumb_link = value

    # Instructor name (in hebrew)
    @property
    def instructor_name(self):
        """ Getter """
        return self._instructor_name
    @instructor_name.setter
    def instructor_name(self, value):
        """ Setter """
        # The decode was needed in py2, probably because text had a ' in it,
        # but py3 doesn't have the decode method
        try:
            self._instructor_name = value.decode('unicode-escape')
        except Exception: # pylint: disable=broad-except
            self._instructor_name = value

    # Recording date
    @property
    def record_date(self):
        """ Getter """
        return self._record_date
    @record_date.setter
    def record_date(self, value):
        """ Setter """
        self._record_date = value

    # Video playlist ID
    @property
    def video_playlist_id(self):
        """ Getter """
        return self._video_playlist_id
    @video_playlist_id.setter
    def video_playlist_id(self, value):
        """ Setter """
        self._video_playlist_id = value

    # Video download link
    @property
    def video_link(self):
        """ Getter """
        # Lazy loading implementation
        if self._video_link is None:
            self._video_link =\
                HtmlLayer.HtmlHandler.get_video_link(self.course_id,
                                                     self.parent_playlist,
                                                     self.video_playlist_id)
        return self._video_link
    @video_link.setter
    def video_link(self, value):
        """ Setter """
        self._video_link = value

    # Course ID
    @property
    def course_id(self):
        """ Getter """
        return self._course_id
    @course_id.setter
    def course_id(self, value):
        """ Setter """
        self._course_id = value

    # Parent playlist
    @property
    def parent_playlist(self):
        """ Getter """
        return self._parent_playlist
    @parent_playlist.setter
    def parent_playlist(self, value):
        """ Setter """
        self._parent_playlist = value
