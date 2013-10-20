# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('univhub'),XML('&trade;&nbsp;'),
                  _class="brand",_href=URL('default','index'))
response.title = request.application.replace('_',' ').title()
#response.subtitle = T('Connects Everyone')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'ranjith_univhub@gmailcom>'
response.meta.description = 'A School app'
response.meta.keywords = 'school, univhub, group'
response.meta.generator = 'Univhub'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('MarkAttendance'),False,URL('school','attendance'), [])
]
