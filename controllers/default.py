# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon.contrib import simplejson


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL('d1'))
   # response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def result():

    return locals()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()




'''
######################################
### Initialize acct and permission ###
######################################
'''

def initialize():
    db(db.auth_user).delete()
    db(db.auth_group).delete()
    db(db.permission_list).delete()

    ## initialize users ##
    db.auth_user.update_or_insert((db.auth_user.email=='admin@athena.com'),first_name='admin',last_name='user',email='admin@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='admin2@athena.com'),first_name='admin2',last_name='user',email='admin2@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='alerts@toastme.com'),first_name='toast',last_name='athena',email='alerts@toastme.com',password=db.auth_user.password.validate('toast11@33')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='upload@athena.com'),first_name='up',last_name='load',email='upload@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='upload2@athena.com'),first_name='up2',last_name='load',email='upload@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='screen@athena.com'),first_name='screen',last_name='user',email='screen@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='screen2@athena.com'),first_name='screen2',last_name='user',email='screen2@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='view@athena.com'),first_name='view',last_name='user',email='view@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='view2@athena.com'),first_name='view2',last_name='user',email='view2@athena.com',password=db.auth_user.password.validate('athena')[0])
    db.auth_user.update_or_insert((db.auth_user.email=='assesser@athena.com'),first_name='assesser',last_name='user',email='assesser@athena.com',password=db.auth_user.password.validate('athena')[0])

    
    # initialize groups ##
    db.auth_group.update_or_insert((db.auth_group.role=="ATHENA Administrator"),role="ATHENA Administrator",description="ATHENA Administrator")
    db.auth_group.update_or_insert((db.auth_group.role=="Upload Transactions"),role="Upload Transactions",description="Upload Transactions")
    db.auth_group.update_or_insert((db.auth_group.role=="Screen Transactions"),role="Screen Transactions",description="Screen Transactions")
    db.auth_group.update_or_insert((db.auth_group.role=="View Violations"),role="View Violations",description="View Violations")
    db.auth_group.update_or_insert((db.auth_group.role=="Assess Violations"),role="Assess Violations",description="Assess Violations")

    ## initialize permission_list ##
    db.permission_list.update_or_insert((db.permission_list.name=="athena_administration"),name="athena_administration")
    db.permission_list.update_or_insert((db.permission_list.name=="upload_trx"),name="upload_trx")
    db.permission_list.update_or_insert((db.permission_list.name=="view_trx"),name="view_trx")
    db.permission_list.update_or_insert((db.permission_list.name=="perform_screening"),name="perform_screening")
    db.permission_list.update_or_insert((db.permission_list.name=="view_violation"),name="view_violation")
    db.permission_list.update_or_insert((db.permission_list.name=="raise_help"),name="raise_help")
    db.permission_list.update_or_insert((db.permission_list.name=="assess_violation"),name="assess_violation")


    ## initialize permissions ##
    db(db.auth_permission).delete()
    test = '[{"ATHENA Administrator":       ["raise_help", "athena_administration"]                                                 }, \
            {"Upload Transactions":         ["raise_help", "upload_trx"]                                                            }, \
            {"Screen Transactions":         ["raise_help", "view_trx", "perform_screening", "view_violation"]                       }, \
            {"View Violations":             ["raise_help", "view_trx", "view_violation"]                                            }, \
            {"Assess Violations":           ["raise_help", "view_trx", "perform_screening", "view_violation", "assess_violation"]   }]'
    permissions = simplejson.loads(test)
    for permission in permissions:
        for i in permission.keys():
            groupid = db(db.auth_group.role==i).select(db.auth_group.id).first()
            for x in permission[i]:
                auth.add_permission(groupid, x, '', 0)

    ## initialize membership ##
    db(db.auth_membership).delete()
    test = '[{"admin@athena.com":           ["ATHENA Administrator", "Assess Violations"]   }, \
            {"admin2@athena.com":           ["ATHENA Administrator", "Assess Violations"]   }, \
            {"upload@athena.com":           ["Upload Transactions"]                         }, \
            {"upload2@athena.com":          ["Upload Transactions"]                         }, \
            {"screen@athena.com":           ["Screen Transactions"]                         }, \
            {"screen2@athena.com":          ["Screen Transactions"]                         }, \
            {"view@athena.com":             ["View Violations"]                             }, \
            {"view2@athena.com":            ["View Violations"]                             }, \
            {"assesser@athena.com":         ["Assess Violations"]                           }, \
            {"fin-alerts@toastme.com":      ["Upload Transactions", "Screen Transactions", "View Violations", "Assess Violations"]      }]'

    members = simplejson.loads(test)
    for member in members:
        for i in member.keys():
            userid = db(db.auth_user.email==i).select(db.auth_user.id).first()
            for x in member[i]:
                groupid = db(db.auth_group.role==x).select(db.auth_group.id).first()
                auth.add_membership(groupid, userid)

    session.flash = T('initialization complete')
    redirect(URL('default','index'))

def testing():
    return locals()

# @auth.requires(auth.has_permission('raise_help',''))
def help():
    response.page_title = 'Help'    
    from gluon.tools import Mail
    form_raiseHelp = SQLFORM(db.helpReport, 
                showid=False, submit_button = 'send')

    if form_raiseHelp.process().accepted:
        helpID = form_raiseHelp.vars.id
        
        message = "From: " +  db.helpReport[helpID].userAcctEmail + "\n" + \
                    "Username: " + db.helpReport[helpID].userName + "\n" + \
                    "Time filed: " + request.now.strftime("%d-%m-%Y %H:%M:%S") + "\n" + \
                    "Type of issue: " + db.helpReport[helpID].subject +  "\n" + \
                    "Brief description: " + db.helpReport[helpID].description + "\n"
        # print message
        # full_name = (session.auth.user.last_name + " " + session.auth.user.first_name) if session.auth else "NotLoggedIn"
        # emailAddr = session.auth.user.email if session.auth else "NotLoggedIn"
       


        if mail:
            
            if mail.send(to=['info@cynopsis-solutions.com'],    
                subject='Athena support required' + ' [' + db.helpReport[helpID].company + ']',
                message=message
            ):
                response.flash = 'Mail sent, issue will be resolved as soon as possible.'
            else:
                response.flash = 'Failed to send Email, please check your internet connection.'
        else:
            response.flash = 'Unable to send the email : email parameters not defined'





    return dict(form = form_raiseHelp)



'''
######################################
### DUMMY CONTROLLER ###
######################################
'''
# main landing
def d1():
    return locals()

def d1_1():
    return locals()

def d1_2():
    return locals()

def d1_3():
    return locals()

# how it works
def d2():
    return locals()

# buy/ship for me
def d3():
    return locals()    

def d3_1():
    return locals()

def d3_2B():
    return locals()

def d3_2B_a():
    return locals()

def d3_2S():
    return locals()

def d3_3():
    return locals()

def d3_4():
    return locals()

def d3_5():
    return locals()

# ware house
def d4():
    return locals()
# rate of delivery
def d5():
    return locals()

# registration
def d6():
    return locals()
# where to shop
def d7():
    return locals()
# forum
def d8():
    return locals()
# FAQ
def d9():
    return locals()
# Track order
def d10():
    return locals()
# MY PROFILE
def d11():
    return locals()
    