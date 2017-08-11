# (for py2 compatibility) encoding: utf-8

""" Gui lib module """

from time import sleep
from threading import Lock
from threading import current_thread
from HelperFunctions import cross_platform_hebrew
try:
    import Tkinter as TK #py2
except ImportError:
    import tkinter as TK #py3
try:
    import tkMessageBox as TKmsg #py2
except ImportError:
    from tkinter import messagebox as TKmsg #py3


class GuiLib(object):
    """ This class will hold the gui helper functions """

    def __init__(self, main_window_instance):
        """ The """
        self.__is_setup = False
        self.main_window_instance = main_window_instance

    def __setup(self):
        """ This is to setup the class. Every class method should call it at first
            (Multiple calls will be ignored) """
        # This part will always run, to update references
        self.course_listbox = self.main_window_instance.course_list
        self.playlist_listbox = self.main_window_instance.playlist_list
        self.video_listbox = self.main_window_instance.video_list
        self.video_link_box = self.main_window_instance.video_link_box

        if self.__is_setup:
            return
        self.__is_setup = True

        from HtmlLayer import HtmlHandler
        self.all_courses = HtmlHandler.get_course_list()

        # This is so the updating process is visible and more intuitive
        self.clear_sleep_time = 0.1

        # This text will be added to the listview's parent when it's being updated
        # (and removed when finished)
        self.update_waiting_text = ' - ' + cross_platform_hebrew(u'מעדכן') + '...'
        self.courses_box_text = cross_platform_hebrew(u'רשימת קורסים')
        self.playlist_box_text = cross_platform_hebrew(u'רשימת פלייליסטים') + ' - '
        self.video_box_text = cross_platform_hebrew(u'רשימת סרטונים') + ' - '

        # These 2 vars are to keep track of the most recent operation
        # (to avoid updating the playlist, if it's the same as the previous update)
        self.current_course_index = None
        self.current_playlist_index = None
        self.current_video_index = None

        # These variables are used to avoid more than 1 thread running an update function
        # A TID is saved, if if it changes, the update loop should exit
        self.update_courses_active_tid = None
        self.update_playlists_active_tid = None
        self.update_videos_active_tid = None

        # These may not be completely necessary, but it simplifies stuff when an update function
        # has only 1 instance
        # (It's important to only lock after saving the TID, or it will be irrelevant,
        #  because the mutex will prevent another function instance to start, but it will wait
        #  for the current one to finish, which is unecessary and anoying)
        self.update_courses_mutex = Lock()
        self.update_playlists_mutex = Lock()
        self.update_videos_mutex = Lock()

    def update_courses(self):
        """ This will update the course listbox """
        self.__setup()

        # Save current thread ID and lock
        self.update_courses_active_tid = current_thread().ident
        self.update_courses_mutex.acquire()

        # Prepare for updating
        self.course_listbox.master['text'] = self.courses_box_text + self.update_waiting_text
        self.course_listbox.delete(0, TK.END)
        if self.playlist_listbox != None:
            self.playlist_listbox.delete(0, TK.END)
        if self.video_listbox != None:
            self.video_listbox.delete(0, TK.END)
        if self.video_link_box != None:
            self.reset_link_box()
        sleep(self.clear_sleep_time)

        # Update
        for course_index, course in enumerate(self.all_courses):
            # Break if another thread started this function
            if self.update_courses_active_tid != current_thread().ident:
                break
            self.course_listbox.insert(TK.END,
                                       str(course_index + 1) + ': ' +
                                       cross_platform_hebrew(course.name) + ' ' +
                                       course.semester + ' (' + course.course_number + ')')

        # Wrap up and release
        self.course_listbox.master['text'] =\
            self.course_listbox.master['text'].replace(self.update_waiting_text, '')
        self.update_courses_mutex.release()

    def update_playlists(self, new_course_index):
        """ This will update the playlist listbox """
        self.__setup()

        # Do nothing if nothing changed
        if new_course_index == self.current_course_index:
            return

        # Save current thread ID and lock
        self.update_playlists_active_tid = current_thread().ident
        self.update_playlists_mutex.acquire()

        # Prepare for updating
        self.playlist_listbox.master['text'] = self.update_waiting_text
        self.playlist_listbox.delete(0, TK.END)
        if self.video_listbox != None:
            self.video_listbox.delete(0, TK.END)
        self.current_course_index = new_course_index
        if self.video_link_box != None:
            self.reset_link_box()
        sleep(self.clear_sleep_time)

        # Update
        enumed_playlists =\
            enumerate(self.all_courses[int(self.current_course_index) - 1].playlist_list)
        for playlist_index, playlist in enumed_playlists:
            # Break if another thread started this function
            if self.update_playlists_active_tid != current_thread().ident:
                break
            self.playlist_listbox.insert(
                TK.END, str(playlist_index + 1) + ': ' + cross_platform_hebrew(playlist.title))

        # Wrap up and release
        self.playlist_listbox.master['text'] = \
            self.playlist_box_text +\
                cross_platform_hebrew(self.all_courses[int(new_course_index) - 1].name) + ' ' + \
                self.all_courses[int(new_course_index) - 1].semester
        self.update_playlists_mutex.release()

    def update_videos(self, new_playlist_index):
        """ This will update the videos listbox """
        self.__setup()

        # Do nothing if nothing changed
        if new_playlist_index == self.current_playlist_index:
            return

        # Save current thread ID and lock
        self.update_videos_active_tid = current_thread().ident
        self.update_videos_mutex.acquire()

        # Prepare for updating
        self.video_listbox.master['text'] = self.update_waiting_text
        self.video_listbox.delete(0, TK.END)
        self.current_playlist_index = new_playlist_index
        if self.video_link_box != None:
            self.reset_link_box()
        sleep(self.clear_sleep_time)

        # Update
        enumed_videos =\
            enumerate(self.all_courses[int(self.current_course_index) - 1].
                      playlist_list[int(self.current_playlist_index) - 1].video_list)
        for video_index, video in enumed_videos:
            # Break if another thread started this function
            if self.update_videos_active_tid != current_thread().ident:
                break
            self.video_listbox.insert\
                (TK.END,
                 str(video_index + 1) + ': ' + cross_platform_hebrew(video.title) + ' - ' +
                 cross_platform_hebrew(video.instructor_name) + ' - ' + video.record_date)

        # Wrap up and release
        self.video_listbox.master['text'] = \
            self.video_box_text + cross_platform_hebrew(
                self.all_courses[int(self.current_course_index) - 1].
                playlist_list[int(self.current_playlist_index) - 1].title)
        self.update_videos_mutex.release()

    def update_link_box(self, new_video_index):
        """ This will update the video link box """
        self.__setup()

        # Do nothing if nothing changed
        if new_video_index == self.current_video_index:
            return

        # Prepare for updating
        self.current_video_index = new_video_index
        self.video_link_box.delete(0, TK.END)

        # Update
        current_video =\
            self.all_courses[int(self.current_course_index) - 1]\
            .playlist_list[int(self.current_playlist_index) - 1]\
            .video_list[int(self.current_video_index) - 1]
        self.video_link_box.master['text'] =\
            cross_platform_hebrew(u'לינק ישיר - ') +\
            cross_platform_hebrew(current_video.title) + ' - ' +\
            cross_platform_hebrew(current_video.instructor_name) + ' - ' + current_video.record_date
        self.video_link_box.insert(0, current_video.video_link)

    def reset_link_box(self):
        """ This will reset the video link box """
        self.__setup()

        self.video_link_box.delete(0, TK.END)
        self.video_link_box.master['text'] = cross_platform_hebrew(u'לינק ישיר')

    @staticmethod
    def show_error(error_msg):
        """ Show a window message with the error and exit """
        TKmsg.showerror('Error', error_msg)
        # This is needed to exit all threads
        import os
        os._exit(1)

    @staticmethod
    def show_notice(msg):
        """ Show a window message with the notice """
        TKmsg.showinfo('Info', msg)
