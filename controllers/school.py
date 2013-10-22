# coding: utf8
# try something like
@auth.requires_login()
def index():
    if auth.has_membership(role=admin_str):
        session.class_id=0
        session.section_id=0
        session.serversearch=1
        redirect(URL('school','admin', vars=dict(function='index')))
    elif auth.has_membership(role=teacher_str):
        session.class_id=0
        session.section_id=0
        redirect(URL('school','teacher', vars=dict(function='index')))
    else:
        redirect(URL('school','user', vars=dict(function='index')))

def holiday():
    grid = SQLFORM.smartgrid(db.holiday)
    return locals()
                                              
def users():
    sectionlist = []
    classes=db(db.class_tbl.school_id==auth.user.school_id).select(db.class_tbl.id)
    for i in classes:
        sections=db(db.section_tbl.class_id==i).count()
        sectionlist.append({'class':int(i.id) ,'sections':sections})
    return dict(mylist=repr(sectionlist))

@auth.requires_login()
def classes():
    if not IsValidClass(request.vars.id):
        redirect(URL('school','index'))
    session.class_id=request.vars.id
    section_records=db(db.section_tbl.class_id == session.class_id).select()
    return dict(records=section_records)
    
    
@auth.requires_login()
def classreport():
    if not IsValidClass(request.vars.id):
        redirect(URL('school','index'))
    return dict()
    
@auth.requires_login()
def sections():
    if not IsValidSection(request.vars.id):
        redirect(URL('school','index'))
    session.section_id=request.vars.id
    class_teacher=db((db.section_tbl.id==request.vars.id) & (db.section_tbl.class_teacher_id==db.teacher_tbl.id) & (db.teacher_tbl.user_id==db.auth_user.id)).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name).first()

    students=db((db.student.section_id==request.vars.id) &(db.student.user_id==db.auth_user.id)).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name)    
    return dict(class_teacher=class_teacher,students=students)
    
@auth.requires_login()
def sectionreport():
    if not IsValidSection(request.vars.id):
        redirect(URL('school','index'))
    return dict()

@auth.requires(auth.has_membership(role=admin_str))
def admin():
    user_school_id = auth.user.school_id
    class_records=db(db.class_tbl.school_id == user_school_id).select()
    return dict(records=class_records, entity=request.vars.entity,id=request.vars.id)

@auth.requires(auth.has_membership(role=teacher_str))
def teacher():
    class_records=db((db.teacher_tbl.user_id==auth.user.id) & (db.teacher_tbl.id==db.section_tbl.class_teacher_id)).select(db.section_tbl.id,db.section_tbl.section_nm)
    return dict(records=class_records)

@auth.requires_login()    
def user():
    if not request.vars.id:
        request.vars.id=auth.user.id
    student_profile=db(db.auth_user.id==request.vars.id).select().first()
    return dict(student_profile=student_profile)

@auth.requires_login()
def message():
    entity_id=request.vars.id
    count=0
    success=1
    retMsg="Message Scheduled"
    entity_type=request.vars.entity
    if auth.has_membership(role=student_str) and (entity_type == class_type or entity_type == section_type):
        retMsg="Sending Message Failed"
        success=0
    elif entity_type == class_type:
        count = db((db.class_tbl.id==entity_id) & (db.class_tbl.school_id==auth.user.school_id)).count()
        if count != 1:
            success=0
            retMsg="Sending Message Failed"
    elif entity_type == section_type:
        count = db((db.section_tbl.id==entity_id) & (db.section_tbl.class_id==db.class_tbl.id) & (db.class_tbl.school_id==auth.user.school_id)).count()
        if count != 1:
            success=0
            retMsg="Sending Message Failed"   
    elif entity_type == user_type:
        count = db((db.auth_user.id==entity_id) & (db.auth_user.school_id==auth.user.school_id)).count()
        if count != 1:
            success=0
            retMsg="Sending Message Failed"
    else:
        success=0
        retMsg="Unhandled"
    if success:
        mail_content=request.vars.msg_content
        status="pending"
        db.mail_queue.insert(entity_id=entity_id, entity_type=entity_type, mail_content=mail_content,status=status)
    return retMsg
    
            
@auth.requires_login()    
def userreport():
    if not request.vars.id:
        request.vars.id=auth.user.id
    return dict()

@auth.requires_login()    
def attendance():
    if not request.vars.class_id:
        request.vars.class_id=1;
    if not request.vars.section_id:
        request.vars.section_id=1;
    sections=db(db.section_tbl.class_id==request.vars.class_id).select(db.section_tbl.class_id,db.section_tbl.id,db.section_tbl.section_nm)
    students=db((db.section_tbl.class_id==request.vars.class_id) & (db.section_tbl.id==request.vars.section_id) & (db.student.section_id==db.section_tbl.id) &(db.student.user_id==db.auth_user.id)).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name)    
    return dict(sections=sections,students=students)

def saveattendance():
        db.attendance.insert(school_id=1)
        db.commit()
        response.flash = T("Success")


def searchusers():
    if not request.vars.searchuser: return ''
    users = db(db.auth_user.first_name.startswith(request.vars.searchuser) | db.auth_user.last_name.startswith(request.vars.searchuser)).select()
    return DIV(*[DIV((user.first_name+" "+user.last_name),
                     _onclick="jQuery('#searchuser').val('%s %s'); jQuery('#searchuserid').val('%s'); jQuery('#test').submit()" % (user.first_name,user.last_name, user.id),
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for user in users])
					     
    
def IsValidClass(record_id):
    record=db((db.class_tbl.class_id==record_id) & (db.class_tbl.school_id==auth.user.school_id)).count()
    if record==1:
        return True
    else:
        return False

def IsValidSection(record_id):
    record=db((db.section_tbl.id==record_id) & (db.section_tbl.class_id==session.class_id)).count()
    if record==1:
        return True
    else:
        return False
