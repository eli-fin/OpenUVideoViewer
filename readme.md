# General information
This program will allow you to browse through the courses, playlists and videos of your courses in the Isreali Open University and download the videos to your computer.
The videos links are in m3u8 format, which is a list of ~10 seconds long videos in .ts format.
This app just downloads all of them and simply concatenates them.
Some players might not handle this type of file very well, meaning they will not show the full length of the video and will sometimes cause problems when trying to navigate around, but overall, they seem to be good enough to use.

# Usage instructions
- To run the application, just run the `Main.py` file.

- Video links will be shown when clicked and can be copied (or opened in browser)
~~Videos can also be exported to an HTML file, which will be saved in user downloads folder~~
(HTML no longer available, since I could not find an MP4 direct link)
- Username, password and ID should configured in config file. (I'ts just a plain text file)

- Unsupported courses (which either have no videos or are in an older format)
will have NULL as their course number (in brackets) and cannot be viewed.

- There's a screenshot of the main screen in the wiki (from the images folder)

## Dependencies
Tkinter is used for GUI in this app, so on linux, you will need to install TK, which is what tkinter uses internally.
`sudo apt-get install python-tk` [or `python3-tk`, for python3]
    
#### Python packages needed:
(to install packages, use `pip install <package_name>` (requires admin).
If pip is not in your path, find your python binary and replace `pip...` with `python -m pip...`)
    - requests
    - lxml
##### Note for lxml:
If you run the app on windows and get the following error:
`ImportError: DLL load failed: The specified procedure could not be found.`
There's probably something wrong with the lxml binaries.
To solve this, first uninstall your current lxml installation
(`pip uninstall lxml`) and then, go to: [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)
  and download an unofficial binary for lxml (the file `lxml‑3.8.0‑cp36‑cp36m‑win_amd64.whl` worked for me) and install it (`pip install <whl_filename>`).
(btw: the hyphens in the above file name are not regular ones, but some unicode character)

##### Note 
Sometimes installing the above packages can cause some problems
If you have any problems installing or using them,
go to their installation pages:
lxml:     [http://lxml.de/installation.html](http://lxml.de/installation.html)
requests: [http://docs.python-requests.org/en/master/user/install/](http://docs.python-requests.org/en/master/user/install/)

# Some more info
For GUI, tkinter was used. Hebrew support is incomplete (and even less so in Linux)
Written and tested mainly in Python 3.6.1 on Windows. It seems to work in python 2.6 and above (tested in windows and ubuntu).
I have no idea what will happen in other versions or operating systems.
Also, Hebrew on linux might look a little weirder, as it's inversed (to simulate RTL)

# Known bugs
- If you keep getting an error while getting the information, it could be because your internet is filtered.
- If the app has been on for a while without actively making requests, the session will time out. Just restart the app.

# TODO LIST
- implement `clas.__str__()` for data classes to make debugging easier
- add more error handling

# Disclaimer
    I am not responsible for anything. Anything you do or that happens that is in any way
    related or caused by this program is the users responsibility.
    In addition, the use of this program is subject to the Israeli OpenUs' license for the user
    and can only be used for what the user is allowed to do.
