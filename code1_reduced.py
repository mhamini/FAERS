from __future__ import division
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


df_total=pd.read_csv('fda.tsv', sep="\t")
df=df_total[['primaryid','drug_seq','caseid','indi_pt','drugname','age','age_cod','gndr_cod','wt','wt_cod','reporter_country','dt.1','lt','ho','ds','ca','ri','ot','reactions']]
df.rename(columns={'reactions': 'pt', 'dt.1': 'de'}, inplace=True)

df=pd.concat([df[col].astype(str).apply(lambda x: x.lower()) for col in df.columns], axis=1)
df.loc[df['de']!='nan', 'de'] = 'death'
df.loc[df['lt']!='nan', 'lt'] = 'life_threat'
df.loc[df['ho']!='nan', 'ho'] = 'hospitalization'
df.loc[df['ds']!='nan', 'ds'] = 'disability'
df.loc[df['ca']!='nan', 'ca'] = 'congenital_anomaly'
df.loc[df['ri']!='nan', 'ri'] = 'required_intervention'
df.loc[df['ot']!='nan', 'ot'] = 'other_serious'
df.loc[df['age_cod']=='85', 'age'] = 85
df = df[df.age_cod != 'dec'].reset_index(drop=True)
indx=df.index[df['age_cod']=='mon']
for i in indx:
    df['age'][i]=float(df['age'][i])*(1/12)
indx=df.index[df['age_cod']=='dy']
for i in indx:
    df['age'][i]=float(df['age'][i])*(1/365)

indx=df.index[df['age_cod']=='wk']
for i in indx:
    df['age'][i]=float(df['age'][i])*(1/52)

indx=df.index[df['age_cod']=='min']
for i in indx:
    df['age'][i]=float(df['age'][i])*(1/525600)
df[df['age_cod'] == 'dec']
df=df.drop(['age_cod'], axis=1)

indx=df.index[df['wt_cod']=='lbs']
for i in indx:
    df['wt'][i]=float(df['wt'][i])*(0.453592)

indx=df.index[df['wt_cod']=='gms']
for i in indx:
    df['wt'][i]=float(df['wt'][i])*(0.001)
df = df[df.wt_cod != '20050308']
df = df[df.wt_cod != '20060127']
df = df[df.wt_cod != '20060330']
df = df[df.wt_cod != '20080808']
df = df[df.wt_cod != 'lg']
df = df[df.wt_cod != 'years']
df = df[df.wt_cod != 'l']
df = df[df.wt_cod != 'y']
df = df[df.wt_cod != 'm']
df=df.drop(['wt_cod'], axis=1) #Droping weight code column
df['gndr_cod']=df['gndr_cod'].str.replace('ns','') # Data Cleaning
df['gndr_cod']=df['gndr_cod'].str.replace('unk','') # Data Cleaning
df = df[df.gndr_cod != 'y']
df = df[df.gndr_cod != 'yr']
df = df[df.gndr_cod != 'n']

df.to_csv('fda_clean1.csv', index=False)


#df=pd.concat([df[col].fillna('') for col in df.columns], axis=1)
#Adding weight, gender_code and weight to patients from a filled visits
for i in df['caseid'].unique():
    dfn=df[df['caseid']==i]
    if dfn['age'].max() is not None:
        age=dfn['age'].max()
        df.loc[df['caseid']==i, 'age'] = age
    if dfn['gndr_cod'].max() is not None:
        gndr=dfn['gndr_cod'].max()
        df.loc[df['caseid']==i, 'gndr_cod'] = gndr
    if dfn['wt'].max() is not None:
        wt=dfn['wt'].max()
        df.loc[df['caseid']==i, 'wt'] = wt
    if dfn['reporter_country'].max() is not None:
        country=dfn['reporter_country'].max()
        df.loc[df['caseid']==i, 'reporter_country'] = country
df.to_csv('fda_cleaned2.csv',index=False)
df2=(df.set_index(df.columns.drop('pt',1).tolist()).pt.str.split(',', expand=True).stack().reset_index().rename(columns={0:'pt'}).loc[:, df.columns])
df2.to_csv('fda_cleaned3.csv',index=False)
