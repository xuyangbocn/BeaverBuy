# -*- coding: utf-8 -*-
# try something like
# from functions import *
from gluon.serializers import json
from gluon.contrib import simplejson
from gluon.tools import fetch
import datetime
DATE_TODAY= request.now.date()#datetime.date(2015, 8, 7)
dict_para_default = dict(scr_date=True,
            r1=True, r2=True, r3=True, r4=True, r5=True, r6=True, r7=True, r8=True,
            r1_1=2, r1_2=1500, r1_3=3, r2_1=2, r2_2=3, r3_1=3, r4_1=3, r5_1=2, r5_2=3, r6_1=2, r6_2=3, r7_1=3, r8_1=500, r8_2=60)




@auth.requires(auth.has_permission('view_violation',''))
def index():
    qry_scr_pre = (db.screening_history.id==db.suspicious_case.scr_hist_id) & (db.suspicious_case.temp_record==False)
    list_scr = [row.screening_history.id for row in db(qry_scr_pre).select()]
    
    list_hist = [dict(day=(row.screening_history.scr_date).isoformat(), ct=int(row.screening_history.count_totSuspCases)) 
                for row in db(qry_scr_pre).select(groupby=db.screening_history.id, orderby=db.screening_history.scr_date)]

    list_scr = list(set(list_scr))
    qry_scr = db.screening_history.id.belongs(list_scr)
    grid_existingScr = buildGridExistScr(qry_scr)
    return dict(grid_existingScr=grid_existingScr, list_hist=list_hist)

def buildGridExistScr(qry_scr):
    grid_existingScr = SQLFORM.grid(qry_scr, 
                    create=False, deletable = False, editable = False, searchable=False, csv = False, user_signature = False, details=False,
                    fields = [db.screening_history.scr_date,
                            db.screening_history.count_r1, #db.screening_history.r1,
                            db.screening_history.count_r2, #db.screening_history.r2,
                            db.screening_history.count_r3, #db.screening_history.r3,
                            db.screening_history.count_r4, #db.screening_history.r4,
                            db.screening_history.count_r5, #db.screening_history.r5,
                            db.screening_history.count_r6, #db.screening_history.r6,
                            db.screening_history.count_r7, #db.screening_history.r7,
                            db.screening_history.count_r8, #db.screening_history.r8,
                            db.screening_history.count_totSuspCases, db.screening_history.count_totSuspTrx,
                            ],
                    orderby=~db.screening_history.scr_date,
                    headers = header(),
                    maxtextlengths=maxTxtLen(),
                    args=request.args[0:4],
                    links=[dict(header='Cases & Charts', body=lambda row: A("Details", _href = URL('viewSuspCases', vars=dict(scrID=row.id, temp=False))))],
                    )

    #grid_existingScr=json(grid_existingScr)
    json_existingScr_pre = [dict(scr_date=castDate(row.scr_date), count_r1=row.count_r1, count_r2=row.count_r2, count_r3=row.count_r3, count_r4=row.count_r4, count_r5=row.count_r5, count_r6=row.count_r6, \
        count_r7=row.count_r7, count_r8=row.count_r8, count_totSuspCases=row.count_totSuspCases, count_totSuspTrx=row.count_totSuspTrx, Cases_Charts=str(URL('viewSuspCases', vars=dict(scrID=row.id, temp=False), extension=False))) for row in db(qry_scr).select()]
    json_existingScr = json(json_existingScr_pre)

    '''json'''
    return json_existingScr
    '''grid'''
    # return grid_existingScr

@auth.requires(auth.has_permission('view_violation',''))
def viewSuspCases():
    scrID = int(request.vars.scrID) if request.vars.scrID else None
    msg = request.vars.msg
    temp = request.vars.temp.upper()=="TRUE" if request.vars.temp else None
    list_caseID = getCaseByScrID(scrID)
    grid_susp = buildGridSusp(list_caseID)

    vio_dist = db(db.screening_history.id==scrID).select().first().as_dict() if scrID else None
    return dict(grid_susp=grid_susp, vio_dist=vio_dist, scrID=scrID, msg=msg, temp=temp)




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