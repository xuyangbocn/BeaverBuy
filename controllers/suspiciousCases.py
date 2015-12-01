# -*- coding: utf-8 -*-
# try something like
# from functions import *
from gluon.serializers import json
from gluon.contrib import simplejson
from gluon.tools import fetch
import datetime
DATE_TODAY=request.now.date()
dict_para_default = dict(scr_date=True,
            r1=True, r2=True, r3=True, r4=True, r5=True, r6=True, r7=True, r8=True,
            r1_1=2, r1_2=1500, r1_3=3, r2_1=2, r2_2=3, r3_1=3, r4_1=3, r5_1=2, r5_2=3, r6_1=2, r6_2=3, r7_1=3, r8_1=500, r8_2=60)



@auth.requires(auth.has_permission('view_violation',''))
def index():
    list_status = ["UNRESOLVED", "RESOLVED", "FLAGGED"]
    list_caseID = getCaseByAttr(None, None, False, None) 
    grid_filteredSuspCase = buildGridSusp(list_caseID)
    return dict(list_status=list_status, grid_filteredSuspCase=grid_filteredSuspCase)


@auth.requires(auth.has_permission('view_violation',''))
def LoadFilterSuspCases():
    from dateutil import parser
    status = request.vars.status if (request.vars.status and request.vars.status!='All') else None
    scr_date_pre = request.vars.scr_date if (request.vars.scr_date) else None
    scr_date = parser.parse(scr_date_pre).date() if scr_date_pre else None
    list_caseID = getCaseByAttr(scr_date, scr_date, False, status)#vio_id, scr_hist_id, 
    grid_filteredSuspCase = buildGridSusp(list_caseID)

    return dict(grid_filteredSuspCase=grid_filteredSuspCase)

@auth.requires(auth.has_permission('assess_violation',''))
def assessSuspCase():
    caseID = request.args(0, cast=int)
    vio = db.suspicious_case[caseID].vio_id.title
    scrID = db.suspicious_case[caseID].scr_hist_id
    # form to edit the details regarding the case
    form_thisSusp = SQLFORM(db.suspicious_case, caseID, deletable=False, showid=False,
                   fields = ['date_raised','vio_id','description','annotation','status','date_resolved'],
                   )
    if form_thisSusp.process().accepted:
        session.flash = 'Suspicious case saved.'
        #redirect(URL('suspiciousCases','index'))
        redirect(URL('screeningHistory', 'viewSuspCases', vars=dict(scrID=scrID, temp=False)))
    elif form_thisSusp.errors:
        response.flash = 'Please double check your input.'\
    # grid to list all transactions that involved in the case
    grid_trx = buildGridTrx(caseID)
    # grid to list all uploaded documents
    grid_caseFile = buildGridCaseFile(caseID)
    # form to upload more document
    form_uploader = FORM(
        INPUT(_name='suspicious_case_document',_type='file', requires=IS_NOT_EMPTY()),)
    if form_uploader.accepts(request.vars, formname='form_uploader'):
        # file name
        fileName1 = str(db.suspicious_case[caseID].id)
        fileName2 = str(db(db.case_file.case_id ==caseID).count()+1)
        fileName = fileName1+"_"+fileName2
        #if request.vars.suspicious_case_document:
            # check if pdf or jpg and <3mb
        # if not request.vars.suspicious_case_document.filename.split('.')[-1] in ['jpeg','jpg','pdf', 'JPEG', 'JPG', 'PDF', 'PNG']:
        #     session.flash= "Sorry, Suspicious case documents must be in JPEG or PDF format."
        #     redirect(URL(args=request.args))
        # insertion
        t=db.case_file.docs.store(form_uploader.vars.suspicious_case_document.file, form_uploader.vars.suspicious_case_document.filename)
        db.case_file.insert(case_id=caseID,
            docs=t,
            name=fileName)
        # else:
        #   session.flash = ("Please select a file to submit")

        redirect(URL(args=request.args))
    elif form_uploader.errors:
        response.flash = ("Please select a file to submit")    
    return dict(grid_trx=grid_trx, caseID=caseID, scrID=scrID, form_thisSusp=form_thisSusp, grid_caseFile=grid_caseFile, form_uploader=form_uploader, vio=vio)


def buildGridCaseFile(caseID):
    qry_caseFile = (db.case_file.case_id ==caseID)
    db.case_file.created_on.readable=True
    grid_caseFile = SQLFORM.grid(qry_caseFile, create=False, editable=False, details=False, searchable=False, csv=False, user_signature=False,
                        fields=[db.case_file.created_on, db.case_file.docs],
                        orderby=~db.case_file.created_on,
                        upload=URL('download'),
                        args=request.args[0:2],
                        )
    grid_caseFile.element('.web2py_counter', replace=None)
    json_caseFile_pre = [dict(Created_on=row.created_on, Case_documents=row.docs, 
        DeleteLink="/"+request.application+"/"+request.controller+"/assessSuspCase/"+str(caseID)+"/delete/case_file/"+str(row.id)) for row in db(qry_caseFile).select()]
    json_caseFile = json(json_caseFile_pre) 
    '''json'''
    # return json_caseFile
    '''grid'''
    return grid_caseFile


def buildGridSusp(list_caseID):
    qry_susp = (db.suspicious_case.id.belongs(list_caseID)) & (db.suspicious_case.scr_hist_id==db.screening_history.id)
    grid_susp = SQLFORM.grid(qry_susp, create=False, deletable = False, details=False, editable = False, searchable=False, csv = False, user_signature = False,
                        fields=[db.screening_history.scr_date,
                            db.suspicious_case.vio_id,
                            db.suspicious_case.description,
                            db.suspicious_case.status,
                            ],
                        field_id = db.suspicious_case.id,
                        args=request.args[0:4],
                        maxtextlengths=maxTxtLen(),
                        links=[dict(header='Show relevent transactions', 
                            body=lambda row: A("Involve " + str(len(getTrxByCaseID(row.suspicious_case.id)['list_trxID'])) + " transactions", 
                                _href = URL('suspiciousCases', 'assessSuspCase', args=[row.suspicious_case.id], extension=False)))],
                        )
    #grid_susp=json(grid_susp)
    json_susp_pre = [dict(id=row.suspicious_case.id,date_screened=castDate(row.screening_history.scr_date),status=row.suspicious_case.status,
        vio_id=row.suspicious_case.vio_id.title, description=row.suspicious_case.description, date_resolved=castDate(row.suspicious_case.date_resolved),
        ctTrx=str(len(getTrxByCaseID(row.suspicious_case.id)['list_trxID'])), details=str(URL('suspiciousCases', 'assessSuspCase', 
            args=[row.suspicious_case.id], extension=False))) for row in db(qry_susp).select()]
    json_susp = json(json_susp_pre) 
    '''json'''
    return json_susp
    '''grid'''
    # return grid_susp


def buildGridTrx(caseID):
    qry_trx = db.trx_rec_history.id>0
    if caseID: 
        list_trxID = getTrxByCaseID(caseID)['list_trxID']
        qry_trx = db.trx_rec_history.id.belongs(list_trxID)

    grid_trx = SQLFORM.grid(qry_trx, create=False, deletable = False, editable = False, details=False, searchable=False, csv = False, user_signature = False,
                        args=request.args[0:4],
                        maxtextlengths=maxTxtLen(),
                        )
    #grid_trx=json(grid_trx)
    json_trx_pre = [row.as_dict() for row in db(qry_trx).select()]
    json_trx = json(json_trx_pre) 
    '''json'''
    return json_trx
    '''grid''' 
    # return grid_trx



@auth.requires_signature()
def post():
    """allows to see and post notifcations, ajax loaded"""
    caseID = int(request.vars.caseID) if request.vars.caseID else None
    trxID = int(request.vars.trxID) if request.vars.trxID else None
    # attr = request.args(1, default=None)
    db.post.case_id.default = caseID
    db.post.trx_id.default = trxID
    db.post.case_id.readable = db.post.case_id.writable = db.post.trx_id.readable = db.post.trx_id.writable = False
    form = SQLFORM(db.post).process()
    response.flash=None
    if trxID:
        qry_post = (db.post.trx_id==trxID)
    if caseID:
        qry_post = (db.post.case_id==caseID)

    posts = db(qry_post).select(orderby=db.post.created_on)
    items = DIV()
    for post in posts:
        items.append(DIV(B("On %s, %s %s says" % (post.created_on,
                                                  post.created_by.first_name,
                                                  post.created_by.last_name)),
                         MARKMIN(post.body),_class="comment"))
    return DIV(items,form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)