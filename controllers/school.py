# coding: utf8
# try something like
def attendance():
    from collections import defaultdict
    rows=db().select(db.class_tbl.class_nm.with_alias('class_nm'),db.class_tbl.id.with_alias('class_id'),db.section_tbl.id.with_alias('id'),db.section_tbl.section_nm.with_alias('section_nm'),db.student.id.with_alias('studentid'),db.auth_user.first_name.with_alias('firstname'),db.auth_user.last_name.with_alias('lastname'),left=[db.section_tbl.on(db.section_tbl.class_id==db.class_tbl.id),db.student.on(db.student.section_id==db.section_tbl.id),db.auth_user.on(db.student.user_id==db.auth_user.id)])
    print rows
    sections=[[r.class_nm,r.class_id,r.id,r.section_nm,r.studentid,r.firstname,r.lastname] for r in rows]
    classsection = defaultdict(list)
    classsection1 = defaultdict(list)
    for class_nm, classid, sectionid, sectionname,studentid,firstname,lastname in sections: 
        classsection[classid,class_nm,sectionid,sectionname].append({"studentid":int(studentid if studentid else 0),"firstname":str(firstname),"lastname":str(lastname)})
    for classid,students in classsection.items():
        classsection1[classid[0],classid[1]].append({"sectionid":int(classid[2] if classid[2] else 0),"sectionname":str(classid[3]),"students":students})
    classsection=[{"classid":int(classid[0]),"classname":str(classid[1]),"section":sections} for classid,sections in classsection1.items()]           
    print classsection
    return dict(classsection=XML(classsection))
    
@auth.requires_login()
def index():
    if auth.has_membership(role=admin_str):
        session.class_id=0
        session.subgroup_id=0
        session.section_id=0
        session.serversearch=1
        redirect(URL('school','admin', vars=dict(function='index')))
    elif auth.has_membership(role=teacher_str):
        session.class_id=0
        session.section_id=0
        redirect(URL('school','teacher', vars=dict(function='index')))
    else:
        redirect(URL('school','user', vars=dict(function='index')))
                                              
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
    subgroup_records=db(db.subjectgroup_tbl.class_id==session.class_id).select()
    return dict(records=section_records, subgroup_records=subgroup_records)

@auth.requires_login()
def subgroup():
    if not IsValidSubGroup(request.vars.id):
        redirect(URL('school','index'))
    return
    
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
    class_teacher=db((db.section_tbl.id==request.vars.id) & (db.section_tbl.class_teacher==db.teacher_tbl.id) & (db.teacher_tbl.user_id==db.auth_user.id)).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name).first()

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
    class_records=db((db.teacher_tbl.user_id==auth.user.id) & (db.teacher_tbl.id==db.section_tbl.class_teacher)).select(db.section_tbl.id,db.section_tbl.section_nm)
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
        mail.send(to=['ranjith2041@gmail.com'],subject='hello', message='hi there')
    return retMsg
    
            
@auth.requires_login()    
def userreport():
    if not request.vars.id:
        request.vars.id=auth.user.id
    return dict()

@auth.requires_login()    
def attendance1():
    from collections import defaultdict
    rows=db(db.section_tbl.class_id==db.class_tbl.id).select(db.class_tbl.class_nm.with_alias('class_nm'),db.section_tbl.class_id.with_alias('class_id'),db.section_tbl.id.with_alias('id'),db.section_tbl.section_nm.with_alias('section_nm'))
    print rows
    sections=[[r.class_nm,r.class_id,r.id,r.section_nm] for r in rows]
    classsection = defaultdict(list)
    for class_nm, classid, sectionid, sectionname in sections: 
        classsection[(classid,class_nm)].append({"sectionid":int(sectionid),"sectionname":str(sectionname)})
    classsection=[{"classid":int(classid[0]),"classname":str(classid[1]),"section":sections} for classid,sections in classsection.items()]       
    print classsection
    return dict(classsection=XML(classsection))
    
def getstudents():
    sectionid=request.post_vars['sectionid']
    students=db((db.section_tbl.id==sectionid) & (db.student.section_id==db.section_tbl.id) &(db.student.user_id==db.auth_user.id)).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name)    
    return response.json(students)



def saveattendance():
    retMsg = T("Success")
    message = request.post_vars['message'];
    print message
    if message == 'true':
        retMsg="Message yes"
    else:
        retMsg="Message No"
    absentees = request.post_vars['absenteeslistIDs[]'];
    print absentees
    #db.attendance.insert(school_id=1,AbsenteesListFN=absentees,AbsenteesListAN=absentees)
    #db.commit()
    return retMsg



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

def IsValidSubGroup(record_id):
    record=db((db.subjectgroup_tbl.id==record_id) & (db.subjectgroup_tbl.class_id==session.class_id)).count()
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
