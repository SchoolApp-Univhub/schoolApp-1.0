# -*- coding: utf-8 -*-


#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
#request.requires_https()
string_length = 50

db = DAL('mysql://root:ranjith@localhost/schoolapp',pool_size=1,check_reserved=['all'])

response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

db.define_table('school_bs',
    Field('school_nm', 'string',length=string_length),
    Field('city','string',length=string_length),
    format = '%(school_nm)s, %(city)s'
    )
    
db.define_table('class_bs',
    Field('class_nm', 'string',length=string_length),
    format = '%(class_nm)s'
    )
    
db.define_table('section_bs',
    Field('section_nm', 'string',length=string_length),
    format = '%(section_nm)s'
    )

db.define_table('subject_bs',
    Field('subject_nm', 'string',length=string_length),
    format = '%(subject_nm)s'
    )

db.define_table('user_type',
    Field('user_type_desc', 'string',length=string_length),
    format = '%(user_type_desc)s'
    )
    
auth.settings.extra_fields['auth_user']= [
  Field('school_id', 'reference school_bs'),
  Field('user_type', 'reference user_type'),
  Field('zip'),
  Field('phone')
  ]
  
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

db.define_table('teacher_tbl',
    Field('user_id', 'reference auth_user'),
    Field('school_id', 'reference school_bs'),
    Field('teacher_desc', 'string'),
    format = '%(teacher_desc)s'
    )

db.define_table('class_tbl',
    Field('school_id', 'reference school_bs'),
    Field('class_id', 'reference class_bs'),
    Field('class_nm', 'string'),
    format = '%(class_nm)s'
    )
    
db.define_table('section_tbl',
    Field('class_id', 'reference class_tbl'),
    Field('section_id', 'reference section_bs'),
    Field('section_nm', 'string'),
    Field('class_teacher_id', 'reference teacher_tbl'),
    format = '%(class_id)s'
    )
    
db.define_table('student',
    Field('user_id', 'reference auth_user'),
    Field('section_id', 'reference section_tbl')
    )

db.define_table('attendance',
    Field('school_id', 'reference school_bs'),
    Field('working_day','date'),
    Field('AbsenteesList','list:integer')
    )

db.define_table('holiday',
    Field('school_id', 'reference school_bs'),
    Field('holiday','date'),
    Field('description','string')
    )
    
db.define_table('mail_queue',
    Field('entity_id', 'integer'),
    Field('entity_type', 'integer'),
    Field('mail_subject', 'string'),
    Field('mail_content', 'text'),
    Field('status', 'string')
    )

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging'
mail.settings.sender = 'ranjith2041@gmail.com'
mail.settings.login = 'ranjith:Pp11134711133@'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
crud.settings.formstyle='divs'
auth.settings.formstyle='divs'
auth.messages.label_remember_me="Remember me"
#auth.settings.actions_disabled.append('register')
## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

##############################################################
####################The different callbacks###################
##############################################################

########Variables for Different user types and groups#########
admin_str='admin'
teacher_str='teacher'
student_str='student'
##############################################################

####################################################################
# Function: give_membership
# Return Value: Nill
# Input : f  -> the input form of the auth_user
#         id -> The Id generated while inserting into aut_user table
# Purpose : Adding the memberships for the user while registering.
# ################################################################### 
def give_membership(f,id):
    AdminGroupDesc='All the admins of a school'
    TeacherGroupDesc='All the teachers of a school'
    StudentGroupDesc='All the students of a school'
    GroupId = 0
    UsertypeString = ' '
    UserTyperow = ' '
    UserTyperow = db((db.auth_user.id==id) & (db.auth_user.user_type==db.user_type.id)).select(db.user_type.user_type_desc).first()
    UsertypeString = UserTyperow.user_type_desc
    if UsertypeString == admin_str:
        if auth.id_group(admin_str):
            GroupId = auth.id_group(admin_str)
        else:
            GroupId = auth.add_group(role=admin_str,description=AdminGroupDesc)
            
    elif UsertypeString == teacher_str:
        db.teacher_tbl.insert(user_id=id,school_id=f.school_id,teacher_desc=f.first_name+" "+f.last_name)
        if auth.id_group(teacher_str):
            GroupId = auth.id_group(teacher_str)
        else:
            GroupId = auth.add_group(role=teacher_str,description=TeacherGroupDesc)

    elif UsertypeString == student_str:
        if auth.id_group(student_str):
            GroupId = auth.id_group(student_str)
        else:
            GroupId = auth.add_group(role=student_str,description=StudentGroupDesc)
    auth.add_membership(GroupId,id)
######################################################################

#############Callback registrations###################################
db.auth_user._after_insert.append(lambda f,id: give_membership(f,id))
######################################################################
