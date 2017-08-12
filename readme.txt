# Written in July 2017

# Usage instructions
    This program will allow you to browse through the courses, playlists and videos.
    Video links will be shown when clicked and can be copied (or opened in browser)
    Videos can also be exported to an HTML file, which will be saved in user downloads folder
    Username, password and ID should configured in config file. (I'ts just a text file)

# Dependencies
    Tkinter is used as GUI in this app. So with linux, you need to install TK, which is what tkinter uses internally.
    sudo apt-get install python-tk [or python3-tk, for python3]
    
    # Packages:
        (to install packages, use 'pip install <package_name>' (requires admin).
         if pip is not in your path, find your python binary and replace 'pip...' with 'python -m pip...')

        1. requests
        2. lxml
            Note for lxml:
                If you run the app on windows and get the following error:
                "ImportError: DLL load failed: The specified procedure could not be found."
                There's probably something wrong with the lxml binaries.
                To solve this, first uninstall your current lxml installation
                ('pip uninstall lxml') and then, go to: http://www.lfd.uci.edu/~gohlke/pythonlibs/
                and download an unofficial binary for lxml (the file 'lxml‑3.8.0‑cp36‑cp36m‑win_amd64.whl'
                worked for me) and install it ('pip install <whl_filename>').
                (btw: the hyphens in the above file name are not regular ones, but some unicode form)

        Note:
            Sometimes installing the above packages can cause some problems
            If you have any problems installing or using them,
            go to their installation pages:
            lxml:        http://lxml.de/installation.html
            requests:    http://docs.python-requests.org/en/master/user/install/

# Some more info
    For GUI, tkinter was used. Hebrew support is incomplete (and even more so in Linux)
    Written and tested mainly in Python 3.6.1 on Windows. It seems to work in python 2.6 and above (tested in windows and ubuntu).
    I have no idea what will happen in other versions or operating systems.

    Hebrew on linux might look a little weirder, as it's inversed (to simulate RTL)

# Known bugs
    --

# TODO LIST
- implement __str__ for data classes to make debuggin easier
- more error handling
- deal with pylint errors (there's a ton!)
