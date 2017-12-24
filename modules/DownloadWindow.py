# (for py2 compatibility) encoding: utf-8

""" This module defines the download window of the application """

try:
    import Tkinter as TK #py2
    import ttk
except ImportError:
    import tkinter as TK #py3
    from tkinter import ttk
from threading import Thread
from M3u8Downloader import download_m3u8_file

# Special case values
CURR_CHUNK_MARK_END     = -1
CURR_CHUNK_MARK_INVALID = -2

def start_download_window(root, m3u8_link, dest_file_name):
    """ Starts the download window to download the link and save it as dest_file """

    # Global variable allowing both threads to access this varible easily
    # Used to update progress
    global __curr_chunk
    __curr_chunk = 0

    win = TK.Toplevel(root)

    # Set geometry relative to parent window
    rootX, rootY = [int(x) for x in root.geometry().split('+')[-2:]]
    win.geometry('600x90' + '+' + str(rootX+250) + '+' + str(rootY + 100))

    # Focus and avoid moving/resizing/closing the window
    win.overrideredirect(True)
    win.grab_set()
    
    # Add outer frames
    fr1 = TK.Frame(win, padx=5, pady=5, highlightthickness=2, highlightbackground='green')
    fr1.pack(fill=TK.BOTH)
    fr2 = TK.Frame(fr1, padx=5, pady=5, highlightthickness=2, highlightbackground='blue')
    fr2.pack(fill=TK.BOTH)

    # Add progress bar
    top_label = TK.Label(fr2, text='Downloading \'{0}\':')
    top_label.pack()
    progress_txt = TK.Label(fr2)
    progress_txt._txt_template = '{0} out of {1} chunks done...'
    progress_txt.pack()
    progress_bar = ttk.Progressbar(fr2, orient='horizontal', mode='determinate', length=500, maximum=0)
    progress_bar.pack()

    def update_progress(): # chunk==-1==exit win
        """ Funtion to update progress bar """
        global __curr_chunk
        if __curr_chunk == CURR_CHUNK_MARK_END:
            progress_bar['value'] = progress_bar['maximum']
            progress_txt['text'] = 'Finished! Click to close box'
            win.bind('<Button-1>', lambda event:win.destroy())
        elif __curr_chunk == CURR_CHUNK_MARK_INVALID:
            win.destroy()
        else:
            progress_bar['value'] = __curr_chunk
            progress_txt['text'] = progress_txt._txt_template.format(__curr_chunk, progress_bar['maximum'])
            win.after(100, update_progress)

    # Both callbacks for download_m3u8_file
    def __curr_chunk_setter(n):
        """ Callback """
        global __curr_chunk
        __curr_chunk = n
    def __chunk_count_setter(count):
        """ Callback """
        progress_bar['maximum'] = count

    top_label['text'] = top_label['text'].format(dest_file_name)

    def thread_worker():
        """ Thread worker """
        global __curr_chunk
        if download_m3u8_file(win, m3u8_link, dest_file_name, __chunk_count_setter, __curr_chunk_setter):
            __curr_chunk = CURR_CHUNK_MARK_END
        else:
            __curr_chunk = CURR_CHUNK_MARK_INVALID
    
    # First call to update_progress
    win.after(100, update_progress)

    # Start in thread, to keep gui responsive
    Thread(target=thread_worker, name='Downloader').start()
