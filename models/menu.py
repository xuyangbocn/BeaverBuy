# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(IMG(_src=URL('static','images/Beaver_logo.png'), _alt="My Logo"),_class="navbar-brand", _href=URL('default','index'))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

# response.menu = [
#     (T('Home'), False, URL('main_control', 'index'), [])
# ]
response.menu = [
    (T('New Screening'), False, URL( 'main_control', 'index')),
    (T('Historical Screening Result'), False, URL('screeningHistory', 'index')),
    (T('Suspicious Case Record'), False, URL('suspiciousCases', 'index')),
    (T('User Guide'), False, URL('user_guide', 'index')),
    (T('Support'), False, URL('default', 'help')),

    ]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += []

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
