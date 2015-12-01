# -*- coding: utf-8 -*-
# try something like
# from functions import *
from gluon.serializers import json
from gluon.contrib import simplejson
from gluon.tools import fetch
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
DATETIME_NOW = datetime.now()
DATE_TODAY = date.today()
dict_para_default = dict(scr_date=True,
            r1=True, r2=True, r3=True, r4=True, r5=True, r6=True, r7=True, r8=True,
            r1_1=2, r1_2=900, r1_3=3, r2_1=2, r2_2=3, r3_1=3, r4_1=3, r5_1=2, r5_2=3, r6_1=2, r6_2=3, r7_1=3, r8_1=500, r8_2=20, r8_3=5)



@auth.requires(auth.has_permission('perform_screening',''))
def index():
    # for i in [r1, r2, r3, r4, r5, r6, r7, r1_1, r1_2, r2_1, r5_1, r6_1]
    dict_para = dict_para_default
    if not db(db.screening_history.id>0).isempty():
        if request.vars['scrID']:
            scrID = int(request.vars['scrID'])
            dict_para_pre = db(db.screening_history.id==scrID).select().first()
        else:
            dict_para_pre = db(db.screening_history.id>0).select(orderby=db.screening_history.created_on).last()

        for key in dict_para:
            if dict_para_pre[key]!=None: dict_para[key] = dict_para_pre[key]
    rules = db(db.violations.id>0).select().as_list()
    past_setup_pre = db(db.para_modify_history.id>0).select(orderby=~db.para_modify_history.modify_time)
    past_setup = [dict(scr_date=castDate(row.scr_hist_id.scr_date), scr_id=int(row.scr_hist_id), url=URL(vars=dict(scrID=row.scr_hist_id))) for row in past_setup_pre]

    return dict(dict_para=dict_para, rules=rules, past_setup=XML(past_setup))


@auth.requires(auth.has_permission('perform_screening',''))
def display_flags():
    dict_para = dict_para_default

    for key in ['r'+str(i) for i in range(1,9)]:
        dict_para[key] = request.vars[key] in ["true", "on"]
    for key in ['r1_1', 'r1_2', 'r1_3', 'r2_1', 'r2_2', 'r3_1', 'r4_1', 'r5_1', 'r5_2', 'r6_1', 'r6_2', 'r7_1', 'r8_1', 'r8_2', 'r8_3']:
        if request.vars[key]: dict_para[key] = int(float(request.vars[key])) #if request.vars.r1_1 else None

    from dateutil import parser
    dict_para['scr_date'] = parser.parse(request.vars['scr_date'])
    #temp: check for existed screening
    existedScr = getScrByDate(dict_para['scr_date'])
    if existedScr['existed']:
        msg = "Screening on "+str(dict_para['scr_date'].date())+" has previously been done and shown below."
        session.flash = msg
        redirect(URL('screeningHistory','viewSuspCases', vars=dict(scrID=existedScr['list_scrID'][0], msg=msg, temp=False)))

    screeningO = processScr(dict_para)
    msg = screeningO['msg']
    if screeningO['outcome']==False:
        redirect(URL('screeningHistory','viewSuspCases', vars=dict(msg=msg, temp=True)))

    vio_dist = screeningO['vio_dist']
    scrID = screeningO['scrID']
    recordCaseO = recordCase(screeningO['list_caseID'], ignoreExistedScr=False)
    list_caseID = recordCaseO['list_caseID']
    msg = response.flash = recordCaseO['msg']
    if para_modified(dict_para):
        db.para_modify_history.insert(modify_time=DATETIME_NOW, scr_hist_id=scrID)

    redirect(URL('screeningHistory','viewSuspCases', vars=dict(scrID=scrID, msg=msg, temp=True)))

    return



'''
#########################
### FOR DEMO PURPOSES ###
#########################
'''
# 1. clearAll 2. csvImport [& convertDate] 3.quickRun
@auth.requires_login()
def clearAll():
    db.trx_rec_history.truncate()
    db.screening_history.truncate()
    msg = "success"
    return msg

@auth.requires_login()
def csvImport():
    import os
    import csv
    msg=""
    try:
        db.trx_rec_history.import_from_csv_file(open(os.path.join(request.folder, "daily", "ATHENA_TEST_CSV_AUG.csv"), "r"))
        convertDate()
    except:
        db.rollback()
        msg = "Format error"
    else:
        msg = "success"
    return msg


@auth.requires_login()
def quickRun():
    dict_para = dict_para_default
    try:
        for i in range(1,20):    
            d = date(2015,8,i)
            dict_para['scr_date'] = d
            screeningO = processScr(dict_para)
            recordCaseO = recordCase(screeningO['list_caseID'], ignoreExistedScr=False)
    except:
        db.rollback()
        msg = "Failed"
    else:
        msg = "success"
    return msg





def setup_test_data():
    #warning: this function may decrease your IQ, sorry#
    #RULES ARE SEPERATED, SO SUPPOSEDLY ITS EASIER FOR YOU TO CHANGE#
    #OR NOT#
    #HAHA#
    #SHABI#####
    #db.trx_rec_history.truncate()
    VERY_SPECIAL_DAY = datetime(2015, 6, 8, 12,12,12)
    OTHER_VARS = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3,]
    DOLLAR_VARS = [6500, 6500, 6500, 6500, 6500, 6500, 6500, 100,100, 20000]
    REMIT_NAME_VARS = ["Xu Yang Bo", "Xu Yang Bo", "Xu Yang Bo", "Xu Yang Bo", "Xu Yang Bo", "Xu Yang Bo", "Xu Yang Bo", "Abhishesh Sharma", "Abhishesh Sharma", "Xu Yang Bo",]
    BENE_NAME_VARS= ["Ooi Gene Yan"]*10

    ####set up historic data###
    for i in range(0,10):
        db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            SGDAmt= DOLLAR_VARS[i],
            FrgCurrDesc= " Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= DOLLAR_VARS[i]*2.78 if OTHER_VARS[i] == 2 else DOLLAR_VARS[i]*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "Singapore",
            TrxDate= VERY_SPECIAL_DAY)

    ###set up to trigger rule 1 and rule 5##

    for i in range(0,2):
        db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 1499,
            FrgCurrDesc= " Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= 1499*2.78 if OTHER_VARS[i] == 2 else 1499*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= BENE_NAME_VARS[i] if i == 0 else "Kong Hee Fat Choi",
            BeneCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            TrxDate= DATETIME_NOW)

    ###set up to trigger rule 2####

    for i in range(0,2):
        db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 2600,
            FrgCurrDesc= " Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= 2600*2.78 if OTHER_VARS[i] == 2 else 2600*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            TrxDate= DATETIME_NOW)

    ##testing for rule 3, average for vars 1 is 1600#
    db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 6900,
            FrgCurrDesc= "Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= 6900*2.78 if OTHER_VARS[i] == 2 else 6900*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            TrxDate= DATETIME_NOW)
    #testing for rule 8
    db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 6900,
            FrgCurrDesc= "Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= 6900*2.78 if OTHER_VARS[i] == 2 else 6900*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            TrxDate= DATETIME_NOW)
    db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= BENE_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 6900,
            FrgCurrDesc= "Malaysian Ringgit" if OTHER_VARS[i] == 2 else "Thai Baht",
            FrgCurrAmt= 6900*2.78 if OTHER_VARS[i] == 2 else 6900*25.63,
            ExcRate= 2.78 if OTHER_VARS[i] == 2 else 25.63,
            BeneName= REMIT_NAME_VARS[i],
            BeneCountry= "Malaysia" if OTHER_VARS[i]==2 else "Thailand",
            TrxDate= DATETIME_NOW)

    #testing for rule 4, use a non-coop country la shabi#
    db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 2500,
            FrgCurrDesc= "Swiss Franc",
            FrgCurrAmt= 2500 * 0.70,
            ExcRate= 0.70,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "Switzerland",
            TrxDate= DATETIME_NOW)

    ##testing for rule 7###
    db.trx_rec_history.insert(str_TrxDate= OTHER_VARS[i],
            PayORRec = 'REC',
            AssNO= 69,
            AssName= "Friendly remmitance firm",
            RmtName= REMIT_NAME_VARS[i],
            RmtNric= "S1269291X",
            RmtDOB= date(1992, 6, 8),
            RmtCountry= "Singapore",
            SGDAmt= 2500,
            FrgCurrDesc= "North Korea Won",
            FrgCurrAmt= 2500 * 654.12,
            ExcRate= 654.12,
            BeneName= BENE_NAME_VARS[i],
            BeneCountry= "North Korea",
            TrxDate= DATETIME_NOW)




"""
#########################################
###  FUNCTIONS FOR RULES              ###
#########################################
"""


def n_same_day_below_x(db, date, n=2, x=1500, dur=1):
    list_case,list_suspTrx = [], []
    check = "r1"
    vioID = db(db.violations.notation==check).select().first().id
    #pre: db contains a table of all transactions on the same day
    #post: flags all remitors who have remitted n or more transactions of sgd amount < x dollars in the same day
    # NEW
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date)) & (db.trx_rec_history.SGDAmt<x)
    list_remitters = db(qry_filterTrx).select(db.trx_rec_history.RmtName, 
                                            db.trx_rec_history.id.count(),
                                            groupby = db.trx_rec_history.RmtName, 
                                            having = db.trx_rec_history.id.count()>n)
    for remitter in list_remitters:
        list_rec, list_pay = [], []
        description = " "
        qry_remits = qry_filterTrx & (db.trx_rec_history.RmtName==remitter.trx_rec_history.RmtName)
        for trx in db(qry_remits).select():
            list_rec.append(trx.id)
            if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = description.join(("Remitter",str(remitter.trx_rec_history.RmtName), "sent more than", str(n), "low value transactions (below S$",str(x),") in past", str(dur) ,"days." ))
        # flagSuspicious(vioID, description, list_rec, list_pay)
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))

    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

def n_same_day_same_bene(db, date, n=2, dur=1):
    list_case,list_suspTrx = [], []
    check = "r2"
    vioID = db(db.violations.notation==check).select().first().id

    #pre: db contains a table of all transactions on the same day
    #post: flags all remitors who have remitted 2 of more transactions to the same beneficiary on the same day
    # NEW
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date))
    list_pair = db(qry_filterTrx).select(db.trx_rec_history.RmtName, db.trx_rec_history.BeneName, distinct=True)
    for pair in list_pair:
        list_rec, list_pay = [], []
        description = " "
        qry_remits = qry_filterTrx & (db.trx_rec_history.RmtName==pair.RmtName) & (db.trx_rec_history.BeneName==pair.BeneName)
        if db(qry_remits).count()<=n: continue
        for trx in db(qry_remits).select():
            list_rec.append(trx.id)
            if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = description.join(("More than", str(n), "transactions in past", str(dur),"days between remitter", str(pair.RmtName), "and beneficiary", str(pair.BeneName)))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))

    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

def sudden_increase_value_check(db, date, dur=1):
    list_case,list_suspTrx = [], []
    check = "r3"
    vioID = db(db.violations.notation==check).select().first().id

    #pre: db contains a table of all transactions on the same day AND a table of at lea{'month': of h'is':o}ic trx
    # NEW
    date_year_ago = date - relativedelta(years=1)
    qry_pastTrx = (db.trx_rec_history.TrxDate > dateToTime(date_year_ago))
    temp_sum = db.trx_rec_history.SGDAmt.sum()
    temp_count = db.trx_rec_history.id.count()
    rows = db(qry_pastTrx).select(db.trx_rec_history.RmtName, temp_sum, temp_count, groupby=db.trx_rec_history.RmtName)
    startDate = date - relativedelta(days=dur)
    for row in rows:
        qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date)) & (db.trx_rec_history.RmtName==row.trx_rec_history.RmtName)
        if db(qry_filterTrx).isempty(): continue
        for trx in db(qry_filterTrx).select():
            description = " "
            if trx.SGDAmt > 10*(row._extra[temp_sum]/row._extra[temp_count]):
                list_rec, list_pay = [trx.id], []
                if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
                description = description.join(("Sudden high value transaction by remitter", str(trx.RmtName), "(amount=S$", str(trx.SGDAmt),")"))
                list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))
    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

def tax_haven_non_coop_check(db, date, dur=1):
    list_case,list_suspTrx = [], []
    check = "r4"
    vioID = db(db.violations.notation==check).select().first().id
    #pre: requires a set containing all tax haven/ non-complying countries, and a db containing a table of daily trx_date
    #post: flags all transactions to/from tax haven/non-complying countries
    SET_BAD_BOYS = ["ANDORRA", "ANGUILLA", "ANTIGUA", "BARBUDA", "AUSTRIA", "BARBADOS",
        "INDONESIA", "ISRAEL", "SAINT LUCIA", "TURKEY", "BRITISH VIRGIN ISLANDS", "CYPRUS",
        "LUXEMBOURG", "SEYCHELLES", "BRUNEI DARUSSALAM", "MARSHALL ISLANDS", "DOMINICA",
        "FEDERATED STATES OF MICRONESIA", "GUATEMALA", "LEBANON", "LIBERIA", "PANAMA",
        "NAURU", "SWITZERLAND", "TRINIDAD AND TOBAGO, VANUATA"]
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date)) 
    qry_filterTrx &= (db.trx_rec_history.BeneCountry.upper().belongs(SET_BAD_BOYS)) | (db.trx_rec_history.RmtCountry.upper().belongs(SET_BAD_BOYS))

    for trx in db(qry_filterTrx).select():
        list_rec, list_pay = [trx.id], []
        if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = " "
        description = description.join(("Transaction remits from",str(trx.RmtCountry),"to", str(trx.BeneCountry), ", which involves tax haven country."))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))
    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

def more_than_n_bene(db, date, n=1, dur=1):
    list_case,list_suspTrx = [], []
    check = "r5"
    vioID = db(db.violations.notation==check).select().first().id

    #pre: requires a table of daily trx_date
    #post: flags senders that send to more than one(TODO: configurable) beneficiary
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date))
    bene_count = db.trx_rec_history.BeneName.count()
    list_remitters = db(qry_filterTrx).select(db.trx_rec_history.RmtName, bene_count, groupby=db.trx_rec_history.RmtName)
    for remitter in list_remitters:
        if remitter._extra[bene_count]<=n: continue
        list_rec, list_pay = [], []
        description = " "
        qry_remits = qry_filterTrx & (db.trx_rec_history.RmtName==remitter.trx_rec_history.RmtName)
        for trx in db(qry_remits).select():
            list_rec.append(trx.id)
            if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = description.join(("Remitter", str(remitter.trx_rec_history.RmtName), "remitted to more than", str(n), "beneficiaries in past", str(dur), "days."))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))

    return dict(list_case=list_case,list_suspTrx=list_suspTrx)



def more_than_n_remit(db, date, n=1, dur=1):
    list_case,list_suspTrx = [], []
    check = "r6"
    vioID = db(db.violations.notation==check).select().first().id

    #pre: requires a table of daily trx_date
    #post: flags beneficiaries that recieve from more than one (TODO: configurable) sender
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date))
    remitter_count = db.trx_rec_history.RmtName.count()
    list_benes = db(qry_filterTrx).select(db.trx_rec_history.BeneName, remitter_count, groupby=db.trx_rec_history.BeneName)
    for bene in list_benes:
        if bene._extra[remitter_count]<=n: continue
        list_rec, list_pay = [], []
        description = " "
        qry_remits = qry_filterTrx & (db.trx_rec_history.BeneName==bene.trx_rec_history.BeneName)
        for trx in db(qry_remits).select():
            list_rec.append(trx.id)
            if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = description.join(("Beneficiary", str(bene.trx_rec_history.BeneName), "received transactions from more than", str(n), "remitters in past", str(dur), "days."))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))

    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

def transfers_to_high_risk(db, date, dur=1):
    list_case,list_suspTrx = [], []
    check = "r7"
    vioID = db(db.violations.notation==check).select().first().id

    SET_OF_HIGH_RISK = ["IRAN", "NORTH KOREA", "ALGERIA", "ECUADOR", "MYANMAR", "AFGHANISTAN",
        "ANGOLA", "GUYANA", "INDONESIA", "IRAQ", "LAOS", "PANAMA", "PAPUA NEW GUINEA", "SUDAN", "SYRIA",
        "YEMEN", "UGANDA", "ALBANIA", "CAMBODIA", "KUWAIT", "NICARAGUA", "PAKISTAN", "ZIMBABWE"] 
    startDate = date - relativedelta(days=dur)
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(startDate)) & (db.trx_rec_history.TrxDate<=dateToTime(date)) & (db.trx_rec_history.BeneCountry.upper().belongs(SET_OF_HIGH_RISK))

    for trx in db(qry_filterTrx).select():
        list_rec, list_pay = [trx.id], []
        if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = " "
        description = description.join(("Transaction goes to a high AML risk country:", str(trx.BeneCountry)))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))
    
    return dict(list_case=list_case, list_suspTrx=list_suspTrx)

def potential_low_value_money_lending(db, date, x=1000, dur=60, ctBene=5):
    list_case,list_suspTrx = [], []
    check = "r8"
    vioID = db(db.violations.notation==check).select().first().id
    
    startDate = date - relativedelta(days=dur)
    list_suspLender_pre = more_than_n_bene(db, date, ctBene, dur)['list_suspTrx']
    list_suspLender = list(set([r.RmtName for r in db(db.trx_rec_history.id.belongs(list_suspLender_pre)).select()]))

    lender = db.trx_rec_history.with_alias('lender')
    borrower = db.trx_rec_history.with_alias('borrower')
    qry_filterTrx = (lender.TrxDate>=dateToTime(startDate)) & (lender.TrxDate<=dateToTime(date)) & (lender.SGDAmt<=x)
    qry_filterTrx &= (borrower.TrxDate>=dateToTime(startDate)) & (borrower.TrxDate<=dateToTime(date)) #& (borrower.SGDAmt<=x)
    qry_filterTrx &= (lender.BeneName==borrower.RmtName) & (lender.RmtName==borrower.BeneName)

    for suspLender in list_suspLender:
        qry_lendingTrans = qry_filterTrx & ((lender.RmtName==suspLender) | (lender.BeneName==suspLender))
        if db(qry_lendingTrans).isempty(): continue
        list_rec, list_pay = [], []
        description = " "
        for trx in db(qry_lendingTrans).select(lender.id, distinct=True):
            list_rec.append(trx.id)
            if trx.id not in list_suspTrx: list_suspTrx.append(trx.id)
        description = description.join(("Money lending pattern observed for remitter", str(suspLender), "in the past", str(dur), "days with more than", str(ctBene), "potential borrowers."))
        list_case.append(dict(vioID=vioID, description=description, list_rec=list_rec, list_pay=list_pay))    

    return dict(list_case=list_case,list_suspTrx=list_suspTrx)

