# -*- coding: utf-8 -*-
# try something like
# from functions import *
import json
#from gluon.contrib import simplejson
from gluon.tools import fetch
from datetime import datetime, date
DATETIME_NOW = datetime.now()
DATE_TODAY = date.today()
ERR_MSG = dict(StatusCode = "Exepect status code to be 200.", 
            Token = "Token used for authentication failed.",
            Permission = "Permission not granted for this action.",
            Database = "Database is not accessible.", 
            TableName = "Table name should be trx_rec_history.",
            Pattern = "No matching pattern.",)



def token_failed():
    # Token verification failed
    rtn = dict(errors=dict(),id=None)
    rtn["errors"]["Token"] = ERR_MSG['Token']
    return rtn

def permission_failed():
    # Permission verification failed
    rtn = dict(errors=dict(),id=None)
    rtn["errors"]["Permission"] = ERR_MSG['Permission']
    return rtn


@auth.requires_login()
def index():
    return locals()


@request.restful()
def api():
    response.view = "generic.json"
    def GET(*args,**vars):
        patterns = [#":auto[trx_rec_history]",
            # single filter
            "/trx[trx_rec_history]/id/{trx_rec_history.id}",
            "/trx[trx_rec_history]/RmtID/{trx_rec_history.RmtID}",
            "/trx[trx_rec_history]/RmtCountry/{trx_rec_history.RmtCountry}",
            "/trx[trx_rec_history]/RmtName/{trx_rec_history.RmtName.contains}",
            "/trx[trx_rec_history]/RmtNric/{trx_rec_history.RmtNric}",
            "/trx[trx_rec_history]/RmtDOB/{trx_rec_history.RmtDOB.year}",

            "/trx[trx_rec_history]/BeneID/{trx_rec_history.BeneID}",
            "/trx[trx_rec_history]/BeneCountry/{trx_rec_history.BeneCountry}",
            "/trx[trx_rec_history]/BeneName/{trx_rec_history.BeneName.contains}",
            "/trx[trx_rec_history]/BeneNric/{trx_rec_history.BeneNric}",
            "/trx[trx_rec_history]/BeneDOB/{trx_rec_history.BeneDOB.year}",
            
            "/trx[trx_rec_history]/SGDAmt/{trx_rec_history.SGDAmt.ge}/{trx_rec_history.SGDAmt.lt}",
            "/trx[trx_rec_history]/TrxDate/{trx_rec_history.TrxDate.year}",
            "/trx[trx_rec_history]/TrxDate/{trx_rec_history.TrxDate.year}/{trx_rec_history.TrxDate.month}",
            "/trx[trx_rec_history]/TrxDate/{trx_rec_history.TrxDate.year}/{trx_rec_history.TrxDate.month}/{trx_rec_history.TrxDate.day}",
            ]
        patterns_field = [p+'/:field' for p in patterns]
        patterns += patterns_field

        rtn = dict(errors=dict(),id=None)
        try:
            rtn = api_getFunction(patterns, args,vars)
        except:
            rtn["errors"]["StatusCode"] = ERR_MSG['StatusCode']
        return rtn


    def POST(tablename, **vars):
        rtn = dict(errors=dict(),id=None)
        try:
            rtn = api_postFunction(tablename, **vars)
        except:
            rtn["errors"]["StatusCode"] = ERR_MSG['StatusCode']
        return rtn
    
    return dict(GET=GET, POST=POST)



@auth.requires_login_or_token(otherwise=token_failed)
def api_getFunction(patterns, *args,**vars):
    if auth.has_permission('view_trx','')!=True:
        return permission_failed()

    rtn = dict(errors=dict(),id=None)
    parser = db.parse_as_rest(patterns,*args,**vars)
    if parser.status == 200:
        return dict(content=parser.response)
    # Pattern validation
    elif parser.status == 400 and parser.error == "no matching pattern":
        rtn["errors"]["Pattern"] = ERR_MSG['Pattern']
        return rtn
    else:
        raise HTTP(parser.status, parser.error)


@auth.requires_login_or_token(otherwise=token_failed)
def api_postFunction(tablename, **vars):
    if auth.has_permission('upload_trx','')!=True:
        return permission_failed()

    rtn = dict(errors=dict(),id=None)
    # Table name validation
    if tablename != "trx_rec_history": 
        rtn["errors"]["TableName"] = ERR_MSG['TableName']
    # Field validation
    else:
        try:
            rtn.update(db[tablename].validate_and_insert(**vars).as_dict())
        except:
            rtn["errors"]["Database"] = ERR_MSG['Database']
    return rtn