# (for py2 compatibility) encoding: utf-8

""" Global variables module. Hold global info for application. """

# This should be set on runtime throuth the network login function
LOGIN_DATA = {
    'p_user': '<username>',
    'p_sisma': '<pass>',
    'p_mis_student': '<student_id>',
    'T_PLACE': 'https://opsrv.apps.openu.ac.il/myop',
}


# Links for login process
LOGON_FIRST_PAGE = 'https://sso.apps.openu.ac.il/SheiltaPortalLogin'\
                   '?self=1&T_PLACE=https%3A%2F%2Fopsrv.apps.openu.ac.il%2Fmyop'
LOGON_SECOND_PAGE = 'https://sso.apps.openu.ac.il/SheiltaPortalProcess'

# Links for data extraction
MAIN_PAGE_LINK = 'http://opal.openu.ac.il/my/'
