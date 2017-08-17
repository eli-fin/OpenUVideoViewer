# (for py2 compatibility) encoding: utf-8

""" Network handling module """

import requests
import GlobalVars
import GuiLib
from HelperFunctions import HelperFunctions

class NetworkHandler(object):
    """ This singletone class will handle all network interactions """

    __instance = None

    def __init__(self):
        """ This will construct the class and connect to the server """
        self.__instance = self
        self.__session = None

    @classmethod
    def get_instance(cls):
        """ Singletone implementation """
        if cls.__instance is None:
            cls.__instance = NetworkHandler()
            cls.__instance.login()
        return cls.__instance

    def login(self):
        """ this function will login to the website """

        HelperFunctions.set_login_info()

        # Define session
        self.__session = requests.session()

        # This is the first step to login.
        # This request is for the frame found on the main page(http://www.openu.ac.il/)
        # when clicking on the 'כניסה' button with the login fields.
        # The url must include the vars and a 'cookies_enabled' cookie will be returns
        # and used for the next step.
        self.get_page(GlobalVars.LOGON_FIRST_PAGE)

        # This is the second step.
        # This is the request made by the previous form's submit.
        # The referer header is needed, or an 'unauthorized referer' error will show.
        # (At one point when debuggin, I noticed that the only cookie needed to be passed on
        #   (when not usin a session)
        #   is the 'cookies_enabled' one, or an 'cookies not supported' error will show.
        #   Also, I've made successful requests (without a session) using only the cookies
        #   returened from req2)
        self.post_page(
            GlobalVars.LOGON_SECOND_PAGE,
            data=GlobalVars.LOGIN_DATA,
            headers={'Referer':GlobalVars.LOGON_FIRST_PAGE})
        # Now we're connected.

    def get_page(self, link):
        """ Return html of given link within session """
        try:
            return self.__session.get(link).text
        except Exception: # pylint: disable=broad-except
            GuiLib.show_error('Can\'t get info. Connection problem.')

    def post_page(self, link, data=None, headers=None):
        """ Return html of given link within session """
        try:
            return self.__session.post(link, data=data, headers=headers).text
        except Exception: # pylint: disable=broad-except
            GuiLib.show_error('Can\'t get info. Connection problem.')
