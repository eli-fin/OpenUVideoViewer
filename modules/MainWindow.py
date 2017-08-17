# (for py2 compatibility) encoding: utf-8

""" This module defines the main window of the application """

try:
    import Tkinter as TK #py2
except ImportError:
    import tkinter as TK #py3
from threading import Thread
from os import _exit
import GuiLib
import HtmlLayer
from HelperFunctions import cross_platform_hebrew
from HelperFunctions import open_link_in_browser
from HelperFunctions import export_to_html

class MainWindow(object): # pylint: disable=too-few-public-methods
    """ main gui window """

    def __init__(self): # pylint: disable=too-many-locals
        win_width = str(300+300+500)
        win_height = '400'
        padding = 10

        self.root = TK.Tk()
        self.root.title("OpenU Playlist Viewer")
        self.root.geometry(win_width+'x'+win_height+'+100+100')
        #root.resizable(False, False)

        # Pre declare variables, to allow GuiLib to create references to them
        self.course_list = None
        self.playlist_list = None
        self.video_list = None
        self.video_link_box = None

        self.helper_lib = GuiLib.GuiUpdater(self)

        #===================== Hello msg begin
        hello_msg = TK.Label(self.root,
                             text=cross_platform_hebrew(u'שלום ' +
                                                        HtmlLayer.HtmlHandler.get_student_name()) +
                             '\n--------------------------')
        hello_msg.pack(side=TK.TOP, anchor=TK.NE, padx=padding)
        #===================== Hello msg end

        #===================== Course frame begin
        course_frame = TK.LabelFrame(self.root,
                                     text=cross_platform_hebrew(u'רשימת קורסים - מוריד'),
                                     padx=padding, pady=padding, labelanchor=TK.NE, width=300)
        course_frame.pack_propagate(False) # This is so the width is not ignored
        self.course_list = TK.Listbox(course_frame)
        vertical_scrollbar = TK.Scrollbar(self.course_list, orient=TK.VERTICAL, width=10)
        horizontal_scrollbar = TK.Scrollbar(self.course_list, orient=TK.HORIZONTAL, width=10)
        self.course_list['yscrollcommand'] = vertical_scrollbar.set
        self.course_list['xscrollcommand'] = horizontal_scrollbar.set
        vertical_scrollbar.config(command=self.course_list.yview)
        horizontal_scrollbar.config(command=self.course_list.xview)

        vertical_scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        horizontal_scrollbar.pack(side=TK.BOTTOM, fill=TK.X)
        self.course_list.pack(side=TK.TOP, fill=TK.BOTH, expand=1)
        course_frame.pack(side=TK.RIGHT, padx=padding, pady=padding, fill=TK.BOTH)

        Thread(target=self.helper_lib.update_courses).start()

        # Bind clicks to update playlist_updater
        def playlist_updater(event): # pylint: disable=unused-argument
            """ Method for click action """
            curr_selection = self.course_list.curselection()
            # Check if anything is selected
            if curr_selection == ():
                return

            # For old course sites and sites that don't have a link to a video page
            if self.course_list.get(curr_selection).find('NULL') != -1:
                GuiLib.show_notice('This is the old format course site'
                                   ' or site doesn\'t have a video page link\nNot supported')
                return

            Thread(target=lambda: self.helper_lib.update_playlists(
                self.course_list.get(curr_selection).split(':')[0])).start()

        self.course_list.bind('<ButtonRelease-1>', playlist_updater)
        #===================== Course frame end

        #===================== Playlist frame begin
        playlist_frame = TK.LabelFrame(self.root,
                                       text=cross_platform_hebrew(u'רשימת פלייליסטים'),
                                       padx=padding, pady=padding, labelanchor=TK.NE, width=300)
        playlist_frame.pack_propagate(False) # This is so the width is not ignored
        self.playlist_list = TK.Listbox(playlist_frame)
        vertical_scrollbar = TK.Scrollbar(self.playlist_list, orient=TK.VERTICAL, width=10)
        horizontal_scrollbar = TK.Scrollbar(self.playlist_list, orient=TK.HORIZONTAL, width=10)
        self.playlist_list['yscrollcommand'] = vertical_scrollbar.set
        self.playlist_list['xscrollcommand'] = horizontal_scrollbar.set
        vertical_scrollbar.config(command=self.playlist_list.yview)
        horizontal_scrollbar.config(command=self.playlist_list.xview)

        vertical_scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        horizontal_scrollbar.pack(side=TK.BOTTOM, fill=TK.X)
        self.playlist_list.pack(side=TK.TOP, fill=TK.BOTH, expand=1)
        playlist_frame.pack(side=TK.RIGHT, padx=padding, pady=padding, fill=TK.BOTH)

        # Bind clicks to video_updater
        def video_updater(event): # pylint: disable=unused-argument
            """ Method for click action """
            curr_selection = self.playlist_list.curselection()
            # Check if anything is selected
            if curr_selection == ():
                return
            Thread(target=lambda: self.helper_lib.update_videos(
                self.playlist_list.get(curr_selection).split(':')[0])).start()

        self.playlist_list.bind('<ButtonRelease-1>', video_updater)
        #===================== Playlist frame end

        #===================== Video frame begin
        video_frame = TK.LabelFrame(self.root,
                                    text=cross_platform_hebrew(u'רשימת סרטונים'),
                                    padx=padding, pady=padding, labelanchor=TK.NE, width=500)
        video_frame.pack_propagate(False) # This is so the width is not ignored
        self.video_list = TK.Listbox(video_frame)
        vertical_scrollbar = TK.Scrollbar(self.video_list, orient=TK.VERTICAL, width=10)
        horizontal_scrollbar = TK.Scrollbar(self.video_list, orient=TK.HORIZONTAL, width=10)
        self.video_list['yscrollcommand'] = vertical_scrollbar.set
        self.video_list['xscrollcommand'] = horizontal_scrollbar.set
        vertical_scrollbar.config(command=self.video_list.yview)
        horizontal_scrollbar.config(command=self.video_list.xview)

        vertical_scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        horizontal_scrollbar.pack(side=TK.BOTTOM, fill=TK.X)
        self.video_list.pack(side=TK.TOP, fill=TK.BOTH, expand=1)
        video_frame.pack(side=TK.RIGHT, padx=padding, pady=padding, fill=TK.BOTH)

        # Bind clicks update link_box text
        def video_linkbox_updater(event): # pylint: disable=unused-argument
            """ Method for click action """
            curr_selection = self.video_list.curselection()
            # Check if anything is selected
            if curr_selection == ():
                return
            # Start in same thread. It's a short action and this avoid complications
            self.helper_lib.update_link_box(self.video_list.get(curr_selection).split(':')[0])

        self.video_list.bind('<ButtonRelease-1>', video_linkbox_updater)
        #===================== Video frame end

        #===================== Video link frame begin
        video_link_frame = TK.LabelFrame(video_frame,
                                         text=cross_platform_hebrew(u'לינק ישיר'),
                                         padx=padding, pady=padding, labelanchor=TK.NE)
        self.video_link_box = TK.Entry(video_link_frame, width=100)
        def link_copy_action():
            """ Method for click action """
            self.root.clipboard_clear()
            self.root.clipboard_append(self.video_link_box.get())
        video_link_button = TK.Button(video_link_frame,
                                      text=cross_platform_hebrew(u'העתק'),
                                      command=link_copy_action)

        video_link_button.pack(side=TK.RIGHT)
        self.video_link_box.pack(side=TK.LEFT)
        video_link_frame.pack(side=TK.TOP, padx=padding, pady=padding)
        #===================== Video link frame end

        #===================== Open in browser button begin
        # This will only work in windows
        def open_video():
            """ Method for click action """
            open_link_in_browser(self.video_link_box.get().strip())

        video_link_button = TK.Button(video_frame,
                                      text=cross_platform_hebrew(u'פתח לינק בדפדפן'),
                                      command=open_video)
        video_link_button.pack(side=TK.TOP, anchor=TK.E)
        #===================== Open in browser button end

        #===================== HTML export button begin
        # This will only work in windows
        def export_videos():
            """ Method for click action """
            # Check if there are any videos
            if self.video_list.size() == 0:
                GuiLib.show_notice('No videos found :-(\nTry clicking on a playlist')
                return

            Thread(target=lambda: export_to_html(
                self.helper_lib.all_courses[int(self.helper_lib.current_course_index) - 1],
                int(self.helper_lib.current_playlist_index) - 1)).start()

        export_html_button = TK.Button(video_frame,
                                       text='HTML ' + cross_platform_hebrew(u'יצוא כל הלינקים ל'),
                                       command=export_videos)
        export_html_button.pack(side=TK.TOP, anchor=TK.E)
        #===================== HTML export button end

        # I did this to avoid the warning (in the console)
        # when closing the app and a non-main thread is running tk
        # (RuntimeError: main thread is not in main loop)
        self.root.protocol('WM_DELETE_WINDOW', lambda: _exit(0))

        self.root.mainloop()
