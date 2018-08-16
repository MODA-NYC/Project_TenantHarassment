import pandas as pd

import sys
sys.path.insert(0,'/home/deena/Documents/data_munge/ModaCode/')
import moda

def gather311():
    ''' returns 311 complaints tied to a BBL from 2011 to 2014'''
    query = '''
    with complaints as 
    (select 
     upper(org.LVL8ANC_NAME) as agency,
     srvreq_d.X_BBL as BBL,
     srvreq_d.X_BIN as BIN,
     srvreq_md.TYPE_CD_I,
     srvreq_md.AREA,
     srvreq_md.SUB_AREA,
     srvreq_d.SR_NUM,
     day_d.DAY_DT,
     extract(year from day_dt) as YEAR_DT

    from 
     (SELECT * FROM anaprd.W_ORG_DH WHERE TOP_LVL_NAME <> 'DSNY' 
        and (X_AGENCY_ACRONYM IS NOT NULL OR TOP_LVL_ID <> LVL8ANC_ID OR FIXED_HIER_LEVEL <> 9)) org,
     anaprd.W_SRVREQ_MD srvreq_md,
     anaprd.W_DAY_D day_d,
     anaprd.W_SRVREQ_D srvreq_d, 
     anaprd.W_SRVREQ_F srvreq_f
     
    where  (
         org.ROW_WID = srvreq_f.ACCNT_WID and 
         srvreq_d.ROW_WID = srvreq_f.SR_WID and
         srvreq_d.integration_id = srvreq_f.integration_id and
         srvreq_f.OPEN_DT_WID = day_d.ROW_WID and 
         srvreq_f.X_SR_ATTR_WID = srvreq_md.ROW_WID and 
         day_d.ROW_WID >= 20110101.0 and
         day_d.ROW_WID < 20150101.0
        ) 
    )
    select BBL,
        BIN,
        agency, 
        type_cd_i, 
        area, 
        sub_area, 
        count(sr_num) as count, 
        year_dt 
    from complaints
    group by BBL, BIN, agency, type_cd_i,area,sub_area, year_dt
    '''

    complaints = moda.databridge(query)
    print '311 initial pull',complaints.shape

    #convert to float and drop non positive BBLs
    complaints.BBL = pd.to_numeric(complaints.BBL,errors='coersive')
    complaints = complaints[complaints.BBL>0]
    print '311 after dropping non positive BBLs', complaints.shape

    complaints.BIN = pd.to_numeric(complaints.BIN,errors='coersive')
    complaints.fillna('-',inplace=True)

    return complaints

def categorize311(complaints):
    ''' categorize 311 data '''
    complaints['ComplaintType'] = 'Other' #initialize
    # DOB
    complaints.loc[(complaints['AGENCY']=='DOB'),'ComplaintType'] = 'DOB'

    # DEP
    complaints.loc[complaints['AREA'].str.contains('Construction'),'ComplaintType'] = 'Construction'

    complaints.loc[complaints['TYPE_CD_I']=='Air Quality','ComplaintType'] = 'Air Quality - NonConstruction'

    complaints.loc[(complaints['AREA']=='Air: Dust, Construction/Demolition (AE4)') |
               (complaints['AREA']=='Air: Dust, Construction/Demolition - For Dep Internal Use Only (YAE4)'),
               'ComplaintType'] = 'Dust - Construction DEP'

    # DEP DOHMH
    complaints.loc[(complaints['TYPE_CD_I']=='Asbestos') |
               (complaints['AREA'].str.contains('ASBESTOS')),
               'ComplaintType'] = 'Asbestos'

    complaints.loc[(complaints['TYPE_CD_I']=='Hazardous Materials') ,
               'ComplaintType'] = 'Hazardous Materials'

    # DOHMH DSNY
    complaints.loc[complaints['AREA']=='Dust from Construction','ComplaintType'] = 'Dust - Construction DOHMH'
    complaints.loc[(complaints['TYPE_CD_I']=='Rodent') |
               (complaints['TYPE_CD_I']=='Mold') |
               (complaints['TYPE_CD_I'].str.contains('Unsanitary')) |
               (complaints['TYPE_CD_I']=='Standing Water') |
               (complaints['TYPE_CD_I']=='Vector') |
               (complaints['TYPE_CD_I']=='Sanitation Condition') |
               (complaints['TYPE_CD_I']=='Dirty Conditions'),
               'ComplaintType'] = 'Dirty Conditions'

    # HPD
    complaints.loc[complaints['AGENCY']=='HPD','ComplaintType'] = 'HPD'

    complaints.loc[(complaints['SUB_AREA'].str.contains('NO GAS')) |
        (complaints['SUB_AREA']=='MISSING, DEFECTIVE OR INOPERABLE') | # refridgerator
        (complaints['SUB_AREA']=='UNIT IS INOPERATIVE/ DEFECTIVE - MEDICAL NECESSITY') | # refridgerator
        (complaints['AREA']=='ELECTRIC-SUPPLY') |
        (complaints['AREA']=='NO LIGHTING') |
        (complaints['AREA']=='POWER OUTAGE') |
        (complaints['TYPE_CD_I']=='HEAT/HOT WATER') |
        (complaints['TYPE_CD_I']=='HEATING') |
        (complaints['AREA']=='WATER SUPPLY') | 
        (complaints['AREA']=='GAS') | #gas shut-off
        (complaints['AREA']=='COOKING GAS'), #cooking gas shut-off
        'ComplaintType'] = 'HPD - No Services'

    # DOB illegal work
    complaints.loc[(complaints['AGENCY']=='DOB')&
                (complaints['AREA'].str.contains('Illegal|Unsafe|Safety|Permit')),
               'ComplaintType'] = 'DOB Illegal Work'


    # Not Applicable - has nothing to do with tenenat harrasment apartment conditions
    complaints.loc[complaints.AGENCY.isin(['DOE','TLC','EDC','DCA','DOITT']),'ComplaintType'] = 'NA'
    complaints.loc[complaints.TYPE_CD_I.isin(['Food Establishment','Beach/Pool/Sauna Complaint',
                                          'Mobile Food Vendor','Street Light Condition','New Tree Request',
                                          'Broken Muni Meter','Broken Parking Meter',
                                          'City Vehicle Placard Complaint','Literature Request','CFC Recovery',
                                          'Collection Truck Noise','DSNY Spillage','Employee Behavior','Snow',
                                          'Snow Removal','Storm','Missed Collection (All Materials)',
                                          'Bike Rack Condition','Bus Stop Shelter Complaint',
                                          'Street Sign - Damaged','Street Sign - Dangling',
                                          'Street Sign - Missing','Traffic']),'ComplaintType'] = 'NA'
   
    return complaints

def gatherSale():
    '''query DOF sale, change of ownership data, 2011-2014, no 1 or 2 family homes'''
    query = '''
    SELECT DOF_OWNR_NAME_UPDTD, BBL
    FROM anafic.wc_dof_ownership_f LEFT OUTER JOIN anafic.wc_location_d 
        ON wc_dof_ownership_f.location_wid = wc_location_d.row_wid
    WHERE dof_ownr_name_updtd <= sysdate --don't include dates from dec 31 9999
    AND dof_ownr_name_updtd >= TO_DATE('2011-01-01' , 'YYYY-MM-DD HH24:MI:SS')
    AND dof_ownr_name_updtd < TO_DATE('2015-01-01' , 'YYYY-MM-DD HH24:MI:SS')
    AND BBL > 0 --to remove null BBLs
    AND bldg_class NOT LIKE 'A%' --to remove single family homes
    AND bldg_class NOT LIKE 'B%' --to remove 2 family homes'''

    own = moda.databridge(query)

    # convert to ints
    own.BBL = pd.to_numeric(own.BBL,errors='coersive')

    # extracting out the year from the sales date
    own['saleYear'] = pd.to_datetime(own.DOF_OWNR_NAME_UPDTD).apply(lambda x: x.year)

    own.drop_duplicates(inplace=True)

    print 'DOF',own.shape
    return own

def gatherConst():
    ''' query contsruction data, 2011-2014
    return alt 1-3 jobs on multiple floors '''
    query = '''
    SELECT J_BORO||J_BLOCK||J_LOT AS BBL, 
        J_BIN_NUMBER as BIN, 
        J_PRE_FILING_DATE, 
        J_FLOOR,
        J_JOB_TYPE_DESC
    FROM anafic.wc_dob_job_f
    WHERE J_PRE_FILING_DATE >= TO_DATE('2007-01-01' , 'YYYY-MM-DD HH24:MI:SS')
    AND J_PRE_FILING_DATE < TO_DATE('2016-01-01' , 'YYYY-MM-DD HH24:MI:SS')
    '''

    jobs = moda.databridge(query)
    jobs.drop_duplicates(inplace=True)

    # extracting out the year from the job filing date
    jobs['jobYear'] = jobs.J_PRE_FILING_DATE.apply(lambda x: x.year)

    # converting to ints
    jobs.BBL = pd.to_numeric(jobs.BBL,errors='coersive')
    jobs.BIN = pd.to_numeric(jobs.BIN,errors='coersive')
    jobs = jobs[jobs.BBL>1]
    jobs = jobs[jobs.BIN>1]

    # only keeping ALT 1-3
    altjobs = jobs[jobs['J_JOB_TYPE_DESC'].str.contains('Alteration')]

    # only keeping jobs with work on multiple floors (J_FLOOR contains a comma or dash)
    jobsMultFl = altjobs.fillna('0')[altjobs.fillna('0')['J_FLOOR'].str.contains('-|,')]
    print 'jobs',jobs.shape
    return jobsMultFl

def gatherDOBcomp():
    ''' DOB complaints 2011 to 2014 '''
    query = '''
    select *
    from anafic.wc_dob_complaints_f
    where DATE_ENTERED >= to_date('2011-01-01','YYYY-MM-DD')
    and DATE_ENTERED < to_date('2015-01-01','YYYY-MM-DD')
    '''

    dob = moda.databridge(query)
    print 'dob complaints',dob.shape

    # extract the year of the complaint
    dob['DOBYear'] = dob['DATE_ENTERED'].apply(lambda x: x.year) 
    
    # change to date format
    dob['INSPECTION_DATE'] = pd.to_datetime(dob['INSPECTION_DATE'],errors='coerce')

    #combine to get BBL
    dob['BBL']=dob.BORO+dob.BLOCK+dob.LOT

    #convert BIN,BBL to numbers
    dob['BBL'] = pd.to_numeric(dob.BBL,errors='coersive')
    dob['BIN'] = pd.to_numeric(dob.BIN,errors='coersive')

    # illegal work complaints
    dobIllWorkCat = ['05','83','86','66','71','90','12','5G','76','5A','3A']
    dobIllWork = dob[dob['COMPLAINT_CATEGORY'].isin(dobIllWorkCat)]
    dobIllWork.groupby(['COMPLAINT_CATEGORY','COMPLAINT_CATEGORY_DESCRIPTION']).count()[['BBL']]

    # drop complaints where the last disposition code states no violation was found
    dropcodes = ['I2','XX','I1','H1']
    dobIWC = dobIllWork[~dobIllWork.LAST_DISPOSITION_CODE.isin(dropcodes)]
    
    print 'dob illegal work',dobIWC.shape
    return dobIWC

def gatherRentStab():
    '''rent stabilized data from http://taxbills.nyc/'''
    # read in the rent stabilization data, gives the number of units that are rent stab by BBL
    stab = pd.read_csv("../RentStab/RentStabilizationCounts_JohnKrauss/joined.csv")

    #rows are unique bbls
    # define unit loss
    for year in range(2008,2015):
        stab[str(year)+'loss'] = stab.dropna(subset=[str(year-1)+'uc',str(year)+'uc'])[str(year-1)+'uc']-\
                                                     stab.dropna(subset=[str(year-1)+'uc',str(year)+'uc'])[str(year)+'uc']

    # only keep useful columns
    stab = stab.filter(regex='uc|loss')
        
    # define yearly percent unit loss
    for year in range(2008,2015):
        stab[str(year)+'losspct'] = 100*stab[str(year)+'loss'] \
                                    / (stab[str(year-1)+'uc'].apply(lambda x:float(x)+.0000001))
    print 'rent stab',stab.shape
    return stab


