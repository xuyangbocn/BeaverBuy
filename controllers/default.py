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
    