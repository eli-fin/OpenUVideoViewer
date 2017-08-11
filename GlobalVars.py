# (for py2 compatibility) encoding: utf-8

""" Global variables module """

class GlobalVars(object):
    """ hold global info for application """

    # This should be set on runtime throuth the network login function
    login_data = {
        'p_user': '<username>',
        'p_sisma': '<pass>',
        'p_mis_student': '<student_id>',
        'T_PLACE': 'https://opsrv.apps.openu.ac.il/myop',
    }


    # Links for login process
    logon_first_page = 'https://sso.apps.openu.ac.il/SheiltaPortalLogin'\
                       '?self=1&T_PLACE=https%3A%2F%2Fopsrv.apps.openu.ac.il%2Fmyop'
    logon_second_page = 'https://sso.apps.openu.ac.il/SheiltaPortalProcess'

    # Links for data extraction
    main_page_link = 'http://opal.openu.ac.il/my/'
