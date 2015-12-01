# -*- coding: utf-8 -*-
# from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime, date, timedelta
db._common_fields.append(auth.signature)

DATETIME_NOW = datetime.now()
DATE_TODAY = date.today()
DATE_FMT = "%d-%m-%Y"
DATE_FMT_TIME = "%d-%m-%Y %H:%M:%S"

db.define_table("violations",
    Field('notation', 'string', label='Rule ID'),
    Field('title','string', label='Violation'),
    Field('description','text', label='Description'),
    format='%(title)s'
    )
if db(db.violations.id>0).isempty():
    db.violations.insert(notation="r1", 
        title="Multiple Low Value Transactions from One Remitter", 
        description="Transactions in a series are structured just below the regulatory threshold for due diligence identity checks.")
    db.violations.insert(notation="r2", 
        title="Multiple Transactions from One Remitter to One Beneficiary", 
        description="Transactions in a series are structured just below the regulatory threshold for due diligence identity checks.")
    db.violations.insert(notation="r3", 
        title="Sudden High Value Transactions", 
        description="Customer remits an unusually large (cash) transaction, 10x average amount of his recent 6-month transactions.")
    db.violations.insert(notation="r4", 
        title="Transactions Involving Tax Haven Countries", 
        description="Customer send or receive (regular) payments from countries which are regarded as \"tax havens\" or non co-operating.")
    db.violations.insert(notation="r5", 
        title="Transactions from One Remitter to Multiple Beneficiaries", 
        description="One legal/natural person transfers sum to many legal/natural persons; Many legal/natural persons (who have no obvious blood/business relations) are beneficial owners of transfers ordered by one legal/natural person.")
    db.violations.insert(notation="r6", 
        title="Transactions from Multiple Remitters to One Beneficiary", 
        description="Two or more customers appear to be trying to avoid reporting requirements and seem to be working together to break one transaction into two or more transactions.")
    db.violations.insert(notation="r7", 
        title="Transactions Involving High AML Risk Countries", 
        description="Money transfers to high AML risk jursidictions without reasonable explanation, which are not consistent with the customer's usual foreign business dealings.")
    db.violations.insert(notation="r8", 
        title="Potential Illegal Money Lending (low value)", 
        description="Customer seems to remit to many parties in small amounts, and receive fund back from similar group of people, which is suspicious for illegal money lending activities through the remittance platform.")



db.define_table("trx_rec_history",
    Field("PayORRec",       "string",       label='Pay/Receive',                requires=IS_IN_SET(('PAY','REC', 'INTERNAL'))),
    Field("str_TrxDate",    "string",       readable=False,                     requires=None),
    Field("TrxDate",        "datetime",     label='Transaction date',           requires=IS_DATETIME(format=DATE_FMT_TIME)),
    Field("AssNO",          "integer",      label='Agent code',                 requires=None),
    Field("AssName",        "string",       label='Agent',                      requires=None),
    Field("RmtID",          "string",       label='Remitter ID',                requires=None),
    Field("RmtCountry",     "string",       label='FROM country',               requires=IS_NOT_EMPTY()),
    Field("RmtName",        "string",       label='Remitter',                   requires=IS_NOT_EMPTY()),
    Field("RmtNric",        "string",       label='Remitter\'s NRIC/FIN No.',   requires=IS_NOT_EMPTY()),
    Field("str_RmtDOB",     "string",       readable=False,                     requires=None),    
    Field("RmtDOB",         "date",         label='Remitter\'s date of birth',  requires=IS_EMPTY_OR(IS_DATE(format=DATE_FMT))),
    Field("BeneID",         "string",       label='Beneficiary ID',             requires=None),
    Field("BeneCountry",    "string",       label='TO country',                 requires=IS_NOT_EMPTY()),
    Field("BeneName",       "string",       label='Beneficiary',                requires=IS_NOT_EMPTY()),
    Field("BeneNric",       "string",       label='Beneficiary\'s NRIC/FIN No.',requires=IS_NOT_EMPTY()),
    Field("str_BeneDOB",     "string",      readable=False,                     requires=None),  
    Field("BeneDOB",        "date",         label='Beneficiary\'s date of birth',requires=IS_EMPTY_OR(IS_DATE(format=DATE_FMT))),
    Field("FrgCurrDesc",    "string",       label='Local currency',             requires=IS_NOT_EMPTY()),
    Field("FrgCurrAmt",     "float",        label='Amount (Local currency)',    requires=IS_FLOAT_IN_RANGE(0.0, None)),
    Field("ExcRate",        "float",        label='Echange rate to S$',         requires=IS_FLOAT_IN_RANGE(0.0, None)),
    Field("SGDAmt",         "float",        label='Amount (S$)',                requires=IS_FLOAT_IN_RANGE(0.0, None)),
    #common_filter = lambda query: db.trx_rec_history.created_on<(DATETIME_NOW-timedelta(minutes=15))
    )

db.define_table("screening_history",
    Field("scr_date", "date", label='Screening for'),
    Field("r1", "boolean"),
    Field("r2", "boolean"),
    Field("r3", "boolean"),
    Field("r4", "boolean"),
    Field("r5", "boolean"),
    Field("r6", "boolean"),
    Field("r7", "boolean"),
    Field("r8", "boolean"), 
    Field("r1_1", "integer"),
    Field("r1_2", "integer"),
    Field("r1_3", "integer"),
    Field("r2_1", "integer"),
    Field("r2_2", "integer"),
    Field("r3_1", "integer"),
    Field("r4_1", "integer"),
    Field("r5_1", "integer"),
    Field("r5_2", "integer"),
    Field("r6_1", "integer"),
    Field("r6_2", "integer"),
    Field("r7_1", "integer"),
    Field("r8_1", "integer"),
    Field("r8_2", "integer"),
    Field("r8_3", "integer"),
    Field("count_r1", "integer", label = "Multiple Low Value Transactions from One Remitter"),
    Field("count_r2", "integer", label = "Multiple Transactions from One Remitter to One Beneficiary"),
    Field("count_r3", "integer", label = "Sudden High Value Transactions"),
    Field("count_r4", "integer", label = "Transactions Involving Tax_haven Countries"),
    Field("count_r5", "integer", label = "Transactions from One Remitter to Multiple Beneficiaries"),
    Field("count_r6", "integer", label = "Transactions from Multiple Remitters to One Beneficiary"),
    Field("count_r7", "integer", label = "Transactions Involving High AML Risk Countries"),
    Field("count_r8", "integer", label = "Potential Illegal Money Lending(low value)"),
    Field("count_totSuspCases", "integer", label="Total suspicious cases"),
    Field("count_totSuspTrx", "integer", label="Total suspicious transactions"),
    Field("count_totScrTrx", "integer",),   
    format='%(scr_date)s'
    )

db.define_table("para_modify_history",
    Field("scr_hist_id", "reference screening_history", label='Screen date'),
    Field("modify_time", "datetime", label='Modify Time'),
    format='%(modify_date)s'
    )

db.define_table("suspicious_case",
    Field("date_raised","date", default=date.today(), label='Raise date', writable=False),
    Field("temp_record", "boolean", default=False, label='Temporary record', readable=False, writable=False),
    Field("status", "string",  requires = IS_IN_SET(["UNRESOLVED", "RESOLVED", "FLAGGED"]), default = "UNRESOLVED", label='Status'),
    Field("scr_hist_id", "reference screening_history", label='Screening for', readable=False),
    Field("vio_id", "reference violations", label='Violation', writable=False),
    Field("description", "text", label='Description',),
    Field("annotation", "text", label='Annotation'),
    Field("date_resolved", "date", label='Resolve date', requires=IS_EMPTY_OR(IS_DATE(format=DATE_FMT))),
    #Field.Virtual("trx_rec", lambda row: getTrxByCaseID(row.suspicious_case.id)['list_trxID'], label='Involve transactions'),
    #Field.Virtual("trx_pay", lambda row: listSuspPay(row.suspicious_case.id)),
    )
db.define_table("case_file",
    Field('case_id','reference suspicious_case', requires=IS_IN_DB(db, 'suspicious_case.id', '%(description)s'), required=True),
    Field('docs', 'upload', autodelete=True, uploadseparate=True, label='Suspicious case documents'),
    Field('name', requires=IS_NOT_EMPTY(), default='NoName'),
    )



db.define_table("suspicious_trx",
    Field("case_id", "reference suspicious_case", label='From suspicious case'),
    Field("trx_id", "reference trx_rec_history", label='Transaction number'),
    )

db.define_table('post',
    Field('case_id', 'reference suspicious_case', writable=False, readable=False),
    Field('trx_id','reference trx_rec_history', writable=False, readable=False),
    Field('body', 'text', requires=IS_NOT_EMPTY(), label="Comment"),
    auth.signature,
    )


db.define_table('helpReport',
                Field('company','string', requires=IS_NOT_EMPTY()),
                Field('subject','string', requires=IS_NOT_EMPTY()),
                Field('description', 'text', requires=IS_NOT_EMPTY()),
                Field('userName','string', writable=False, readable=False, default=(session.auth.user.last_name + " " + session.auth.user.first_name) if session.auth else 'NotLoggedIn'),                
                Field('userAcctEmail','string', writable=False, readable=False, default=session.auth.user.email if session.auth else 'NotLoggedIn'),
                Field('date_raised','datetime', writable=False, readable=False, default=request.now,requires=IS_DATE(format=DATE_FMT)),
                Field('status','string', requires = IS_IN_SET(('Raised','Processing','Responsed','Archirved')), default='Raised', writable=False, readable=False, ),
                Field('response','text', writable=False, readable=False,),
                Field('date_responsed','datetime', writable=False, readable=False,requires=IS_EMPTY_OR(IS_DATE(format=DATE_FMT)))
                )

def header():
    headers={
    'violations.notation':'Rule ID',
    'violations.title':'Violations',
    'violations.description':'Violation description',

    'trx_rec_history.PayOrRec':'Pay/Receive',   
    'trx_rec_history.TrxDate':'Time of transaction',    
    'trx_rec_history.AssNo':'Remittance company code',  
    'trx_rec_history.AssName':'Remittance company', 
    'trx_rec_history.RmtCountry':'From country',    
    'trx_rec_history.RmtName':'Remitter', 
    'trx_rec_history.RmtNric':'Remitter\'s NRIC/FIN No.',   
    'trx_rec_history.RmtDOB':'Remitter\'s date of birth',
    'trx_rec_history.BeneCountry':'To country',    
    'trx_rec_history.BeneName':'Beneficiary',   
    'trx_rec_history.BeneNric':'Beneficiary\'s NRIC/FIN No.',   
    'trx_rec_history.BeneDOB':'Beneficiary\'s date of birth',   
    'trx_rec_history.SGDAmt':'Amount (S$)', 
    'trx_rec_history.FrgCurrDesc':'Local currency', 
    'trx_rec_history.FrgCurrAmt':'Amount (local currency)',
    'trx_rec_history.ExcRate':'Exchange rate to S$',

    'screening_history.scr_date':'Screening for',
    "screening_history.count_r1":"Multiple Low Value Transactions from One Remitter",
    "screening_history.count_r2":"Multiple Transactions from One Remitter to One Beneficiary",
    "screening_history.count_r3":"Sudden High Value Transactions",
    "screening_history.count_r4":"Transactions Involving Tax_haven Countries",
    "screening_history.count_r5":"Transactions from One Remitter to Multiple Beneficiaries",
    "screening_history.count_r6":"Transactions from Multiple Remitters to One Beneficiary",
    "screening_history.count_r7":"Transactions Involving High-AML-risk Countries",
    "screening_history.count_r8":"Potential Illegal Money Lending(low value)",
    "screening_history.count_totSuspCases": "Total suspicious cases",
    "screening_history.count_totSuspTrx":"Total suspicious transactions",
    # "screening_history.count_r1":"#",
    # "screening_history.count_r2":"#",
    # "screening_history.count_r3":"#",
    # "screening_history.count_r4":"#",
    # "screening_history.count_r5":"#",
    # "screening_history.count_r6":"#",
    # "screening_history.count_r7":"#",
    # "screening_history.count_r8":"#",

    'suspicious_case.temp_record':'Temporary record',
    'suspicious_case.vio_id':'Violation',
    'suspicious_case.scr_hist_id':'Screening for',
    'suspicious_case.description':'Details',
    'suspicious_case.status':'Status',
    'suspicious_case.date_raised':'Raise date',
    'suspicious_case.date_resolved':'Resolve date',
    'suspicious_case.annotation':'Annotation',
    'suspicious_case.trx_rec':'Involve transactions',   

    'suspicious_trx.case_id':'From suspicious case',
    'suspicious_trx.trx_id':'Transaction number',
    }
    return headers
def maxTxtLen():
    maxTxtLen = {'suspicious_case.description':200, 
            'suspicious_case.vio_id':200,
            'suspicious_case.annotation':200, 
            'trx_rec_history.AssName':200,
            }
    return maxTxtLen


def castDate(date):
    '''convert yyyy-mm-dd to dd-mm-yyyy'''
    date=str(date)
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    cDate = "-".join([day, month, year])
    return cDate

def para_modified(dict_para):
    modified=False
    if db(db.para_modify_history.id>0).isempty():
        modified=True
    else:
        curr_para = db((db.para_modify_history.id>0) & (db.screening_history.id==db.para_modify_history.scr_hist_id)).select(orderby=db.para_modify_history.created_on).last().as_dict()
        print curr_para
        for key in dict_para:
            if key!="scr_date" and dict_para[key]!=curr_para['screening_history'][key]:
                modified=True
                break
    return modified
"""#########################################
###  API_1: Take in transactions information ###
#########################################"""
def inputTrx(dict_trx):
    from dateutil import parser
    try:
        trxID = db.trx_rec_history.insert(PayORRec=dict_trx["PayORRec"],
            str_TrxDate=dict_trx["str_TrxDate"],
            TrxDate=parser.parse(dict_trx["TrxDate"]),
            AssNO=dict_trx["AssNO"],
            AssName=dict_trx["AssName"],
            RmtCountry=dict_trx["RmtCountry"],
            RmtName=dict_trx["RmtName"],
            RmtNric=dict_trx["RmtNric"],
            str_RmtDOB=dict_trx["str_RmtDOB"],
            RmtDOB=parser.parse(dict_trx["RmtDOB"]),
            BeneCountry=dict_trx["BeneCountry"],
            BeneName=dict_trx["BeneName"],
            BeneNric=dict_trx["BeneNric"],
            FrgCurrDesc=dict_trx["FrgCurrDesc"],
            FrgCurrAmt=float(dict_trx["FrgCurrAmt"]),
            ExcRate=float(dict_trx["ExcRate"]),
            SGDAmt=float(dict_trx["SGDAmt"]),
            )
        convertDate([trxID])
    except:
        trxID = None
        msg = "Please check your input data format and try again."
        outcome = False
    else:
        trxID = trxID
        msg = "Transaction is successfully added."
        outcome = True
    return dict(trxID=trxID, msg=msg, outcome=outcome)

def convertDate(*list_trxID):
    qry_trx = db.trx_rec_history.id>0
    if list_trxID: qry_trx &= db.trx_rec_history.id.belongs(list_trxID)
    
    from dateutil import parser
    for row in db(qry_trx, ignore_common_filters=True).select():
        row.update_record(TrxDate=parser.parse(row['str_TrxDate'], dayfirst=False), RmtDOB=parser.parse(row['str_RmtDOB'], dayfirst=False))
    return

"""#########################################
###  API_2: Process screening request ###
#########################################"""
def processScr(dict_para):
    '''
    for API purposes:
    dict_para = simplejson.loads(INPUT PARAMETER: JSON FORMAT)
    '''
    list_caseID=list_case=list_suspTrx=[]
    vio_dist = None
    new_scrID=None
    outcome = False
    if getTrxByAttr(dict_para['scr_date'])['list_trxID'] != []:
        # new_scrID = addScreeningRecord(dict_para)
        startScreeningO = startScreening(dict_para)
        new_scrID = startScreeningO['scrID']
        list_case = startScreeningO['list_case']
        list_suspTrx = startScreeningO['list_suspTrx']
        vio_dist = startScreeningO['vio_dist']
        list_caseID = flagSuspiciousCases(list_case, new_scrID, True)
        msg = "Screening is done."
        outcome = True
    else:
        msg = "Screening is not done. There is no transactions in the selected period."

    return dict(list_caseID=list_caseID, list_case=list_case, scrID=new_scrID, vio_dist=vio_dist, msg=msg, outcome=outcome)


"""#########################################
###  API_3: Look for transactions by attribute ###
#########################################"""
def dateToTime(date):
    return datetime.combine(date, datetime.min.time())

def getTrxByAttr(date): # filter and search to be enhanced.
    list_trxID = []
    qry_filterTrx = (db.trx_rec_history.TrxDate>=dateToTime(date)) & (db.trx_rec_history.TrxDate<=dateToTime(date+timedelta(days=1)))
    if not db(qry_filterTrx).isempty():
        list_trxID = [trx.id for trx in db(qry_filterTrx).select()]

    return dict(list_trxID=list_trxID)



def startScreening(dict_para):
    list_case = []
    list_suspTrx = []
    vio_dist = {'count_r1':0, 'count_r2':0, 'count_r3':0, 'count_r4':0, 'count_r5':0, 'count_r6':0, 'count_r7':0, 'count_r8':0, 'count_totSuspCases':0, 'count_totSuspTrx':0, 'count_totScrTrx':0}

    # date_24 = datetime.date(2015, 6, 24)
    if dict_para['r1']:
        # dict_para['r1_1'] = int(request.vars.r1_1)
        # dict_para['r1_2'] = float(request.vars.r1_2)
        r1 = n_same_day_below_x(db,dict_para['scr_date'], dict_para['r1_1'], dict_para['r1_2'], dict_para['r1_3'])
        list_case += r1['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r1['list_suspTrx']))
        vio_dist['count_r1'] += len(r1['list_case'])
    if dict_para['r2']:
        # dict_para['r2_1'] = int(request.vars.r2_1)
        r2 = n_same_day_same_bene(db, dict_para['scr_date'], dict_para['r2_1'], dict_para['r2_2'])
        list_case += r2['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r2['list_suspTrx']))
        vio_dist['count_r2'] += len(r2['list_case'])
    if dict_para['r3']:
        r3 = sudden_increase_value_check(db, dict_para['scr_date'], dict_para['r3_1'])
        list_case += r3['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r3['list_suspTrx']))
        vio_dist['count_r3'] += len(r3['list_case'])
    if dict_para['r4']:
        r4 = tax_haven_non_coop_check(db, dict_para['scr_date'], dict_para['r4_1'])
        list_case += r4['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r4['list_suspTrx']))
        vio_dist['count_r4'] += len(r4['list_case'])
    if dict_para['r5']:
        # dict_para['r5_1'] = int(request.vars.r5_1)
        r5 = more_than_n_bene(db, dict_para['scr_date'], dict_para['r5_1'], dict_para['r5_2'])
        list_case += r5['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r5['list_suspTrx']))
        vio_dist['count_r5'] += len(r5['list_case'])
    if dict_para['r6']:
        # dict_para['r6_1'] = int(request.vars.r6_1)
        r6 = more_than_n_remit(db, dict_para['scr_date'], dict_para['r6_1'], dict_para['r6_2'])
        list_case += r6['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r6['list_suspTrx']))
        vio_dist['count_r6'] += len(r6['list_case'])
    if dict_para['r7']:
        r7 = transfers_to_high_risk(db, dict_para['scr_date'], dict_para['r7_1'])
        list_case += r7['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r7['list_suspTrx']))
        vio_dist['count_r7'] += len(r7['list_case'])
    if dict_para['r8']:
        r8 = potential_low_value_money_lending(db, dict_para['scr_date'], dict_para['r8_1'], dict_para['r8_2'], dict_para['r8_3'])
        list_case += r8['list_case']
        list_suspTrx = list(set(list_suspTrx) | set(r8['list_suspTrx']))
        vio_dist['count_r8'] += len(r8['list_case'])

    vio_dist['count_totScrTrx'] = len(set(list_suspTrx) | set(getTrxByAttr(dict_para['scr_date'])['list_trxID']))    
    vio_dist['count_totSuspCases'] = vio_dist['count_r1'] + vio_dist['count_r2'] + vio_dist['count_r3'] + vio_dist['count_r4'] +\
                                     vio_dist['count_r5'] + vio_dist['count_r6'] + vio_dist['count_r7'] + vio_dist['count_r8']
    vio_dist['count_totSuspTrx'] = len(list_suspTrx)

    scrID = db.screening_history.insert(scr_date=dict_para['scr_date'],
        r1=dict_para['r1'], r2=dict_para['r2'], r3=dict_para['r3'], r4=dict_para['r4'], r5=dict_para['r5'], r6=dict_para['r6'], r7=dict_para['r7'], r8=dict_para['r8'], 
        r1_1=dict_para['r1_1'], r1_2=dict_para['r1_2'], r1_3=dict_para['r1_3'], 
        r2_1=dict_para['r2_1'], r2_2=dict_para['r2_2'], 
        r3_1=dict_para['r3_1'], 
        r4_1=dict_para['r4_1'], 
        r5_1=dict_para['r5_1'], r5_2=dict_para['r5_2'], 
        r6_1=dict_para['r6_1'], r6_2=dict_para['r6_2'],
        r7_1=dict_para['r7_1'], 
        r8_1=dict_para['r8_1'], r8_2=dict_para['r8_2'], r8_3=dict_para['r8_3'],
        count_r1=vio_dist['count_r1'], count_r2=vio_dist['count_r2'], count_r3=vio_dist['count_r3'], count_r4=vio_dist['count_r4'], 
        count_r5=vio_dist['count_r5'], count_r6=vio_dist['count_r6'], count_r7=vio_dist['count_r7'], count_r8=vio_dist['count_r8'], 
        count_totSuspCases=vio_dist['count_totSuspCases'], count_totSuspTrx=vio_dist['count_totSuspTrx'], count_totScrTrx=vio_dist['count_totScrTrx'], )

    return dict(list_case=list_case, list_suspTrx=list_suspTrx, vio_dist=vio_dist, scrID=scrID)

def flagSuspiciousCases(list_case, scr_hist_id, isTemp=True):
    list_caseID = []
    for case in list_case:
        vioID, description, list_rec, list_pay = case['vioID'], case['description'], case['list_rec'], case['list_pay']
        caseID = db.suspicious_case.insert(temp_record=isTemp, scr_hist_id=scr_hist_id, vio_id = vioID, description=description)
        for i in range(0, len(list_rec)):
            db.suspicious_trx.insert(case_id=caseID, trx_id=list_rec[i])
        list_caseID.append(caseID)
    return list_caseID

"""#########################################
###  API_4: Record suspicious case found  ###
#########################################"""
def recordCase(list_caseID, ignoreExistedScr=False):
    if len(list_caseID)==0:
        msg = "No suspicious case is found."
        outcome = False
    else:
        if not ignoreExistedScr:
            for caseID in list_caseID:
                bool_scrExisted = otherScrExisted(caseID)
                if bool_scrExisted:
                    msg = "Screening on this day had been done previously. Suspicious cases are listed below, but not officially added and tracked."
                    outcome = False
                    return dict(list_caseID=list_caseID, msg=msg, outcome=outcome)                
        db(db.suspicious_case.id.belongs(list_caseID)).update(temp_record=False)
        msg = "Suspicious cases are successfully added."
        outcome = True

    return dict(list_caseID=list_caseID, msg=msg, outcome=outcome)


def getScrDate(caseID):
    qry_scr = (db.suspicious_case.scr_hist_id==db.screening_history.id) & (db.suspicious_case.id==caseID)
    scr_date = db(qry_scr).select().first().screening_history.scr_date
    return scr_date

def otherScrExisted(caseID):
    scrID = db.suspicious_case[caseID].scr_hist_id
    scrDate = db.screening_history[scrID].scr_date
    screeningExistedO = getScrByDate(scrDate)
    if scrID in screeningExistedO['list_scrID'] and len(screeningExistedO['list_scrID'])==1:
        existed = False
    else:
        existed = True
    return existed

"""#########################################
###  API_5: Look for screening record by screening date  ###
#########################################"""
def getScrByDate(scr_date):
    existed = False
    list_scrID = []
    qry_screen = db.screening_history.id>0
    if scr_date:
        qry_screen &= db.screening_history.scr_date==scr_date
    if not db(qry_screen).isempty(): 
        existed = True
        list_scrID = [scr.id for scr in db(qry_screen).select(orderby=db.screening_history.created_on)]

    return dict(existed=existed, list_scrID=list_scrID)

"""#########################################
###  API_6: Show screening detail  ###
#########################################"""
def getScrDetailByID(scrID):
    if db(db.screening_history.id==scrID).isempty():
        scrID=scrID
        msg = "Screening record is not found, please double check if the screening ID entered is valid"
        outcome = False
    else:
        dict_Scr = db.screening_history[scrID].as_dict()
        dict_Scr['scrID'] = scrID
        dict_Scr['msg'] = "Details shown"
        dict_Scr['outcome'] = True

    return dict_Scr


"""#########################################
###  API_7: List cases  ###
#########################################"""
def getCaseByAttr(startDate, endDate, includeTemp, status, **kwargs): #vio_id, scr_hist_id, 
    qry_susp = (db.suspicious_case.id>0) & (db.suspicious_case.scr_hist_id==db.screening_history.id)
    if startDate and endDate:
        qry_susp &= (db.screening_history.scr_date>=startDate)
        qry_susp &= (db.screening_history.scr_date<=endDate)
    if includeTemp==False:
        qry_susp &= (db.suspicious_case.temp_record==False)
    if kwargs and hasattr(kwargs,'vioID'):
        qry_susp &= (db.suspicious_case.vio_id==kwargs['vioID'])
    if status:#kwargs and hasattr(kwargs,'status'):
        qry_susp &= (db.suspicious_case.status==status)
    if kwargs and hasattr(kwargs,'scrID'):
        qry_susp &= (db.suspicious_case.scr_hist_id==kwargs['scrID'])
    
    list_caseID = [susp.suspicious_case.id for susp in db(qry_susp).select()]

    return list_caseID

"""#########################################
###  API_8: List cases from scr ID ###
#########################################"""
def getCaseByScrID(scrID):
    #scrID = request.args(0,default=0,cast=int)
    list_caseID = [case.id for case in db(db.suspicious_case.scr_hist_id==scrID).select()]
    return list_caseID



"""#########################################
###  API_9: Show suspicious case detail ###
#########################################"""
def getCaseDetailByID(caseID):
    if db(db.suspicious_case.id==caseID).isempty():
        caseID=caseID
        msg = "Suspsicous case is not found, please double check if the case entered is valid"
        outcome = False
    else:
        dict_suspCase = db.suspicious_case[caseID].as_dict()
        dict_suspCase['caseID'] = caseID
        dict_suspCase['msg'] = "Details shown"
        dict_suspCase['outcome'] = True

    return dict_suspCase #dict(caseID=caseID, description=description, annotation=annotation, date_resolved=date_resolved, status=status, vio=vio, msg=msg, outcome=outcome)


"""#########################################
###  API_10: EditSuspCase ###
#########################################"""
def editCase(caseID, description, annotation, date_resolved, status):
    if status not in ["UNRESOLVED", "RESOLVED", "FLAGGED"]:
        msg = "Status should be RESOLVED, UNRESOLVED, FLAGGED"
        outcome = False
    elif db(db.suspicious_case.id==caseID).isempty():
        msg = "Suspsicous case is not found, please double check if the case entered is valid"
        outcome = False
    else:
        db.suspicious_case[caseID] = dict(description=description, annotation=annotation, status=status, date_resolved=date_resolved)
        msg = None
        outcome = True
    return dict(caseID=caseID, outcome=outcome, msg=msg)


"""#########################################
###  API_11: Look for suspicious transactions by suspCaseID  ###
#########################################"""
def getTrxByCaseID(caseID, *PayORRec): #getTrxByCaseID
    list_trxID=[]
    q_rec = (db.suspicious_trx.case_id==caseID) & (db.trx_rec_history.id==db.suspicious_trx.trx_id)
    if PayORRec and PayORRec.upper() in ['REC','PAY']:
        q_rec &= db.trx_rec_history.PayORRec==PayORRec.upper()
    if db(q_rec).count()>0: 
        list_trxID = [row.suspicious_trx.trx_id for row in db(q_rec).select()]

    return dict(list_trxID=list_trxID)


"""#########################################
###  API_12: Look for suspicious transactions by suspCaseID  ###
#########################################"""
def getTrxDetailByID(trxID):
    if db(db.trx_rec_history.id==trxID).isempty():
        trxID=trxID
        msg = "Suspsicous case is not found, please double check if the case entered is valid"
        outcome = False
    else:
        dict_trx = db.trx_rec_history[trxID].as_dict()
        dict_trx['trxID'] = trxID
        dict_trx['msg'] = "Details shown"
        dict_trx['outcome'] = True

    return dict_trx