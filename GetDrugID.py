from __future__ import division
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sys

df=pd.read_csv(sys.argv[1])
from six import string_types

def search(myDict, lookup):
    for key, value in myDict.items():
        if isinstance(value['products'], string_types) and lookup in value['products'].lower():
            return str(key)
df3=df.copy()
drug_dict = eval(open("dict_drugbank.txt").read())
import time
start = time.time()
j=0
for index, row in df.iterrows():
    if (row['drugname'])!="":
        drug_name=row['drugname']
        code=search(drug_dict, drug_name)
        df3.set_value(index,'drugbank_ID',str(code))
        #df4.loc[i,'drugbank_ID']=code
    if j % 1000 == 0:
        now = time.time()
        print (j)
        print (now-start)
    j=j+1
df3.to_csv(sys.argv[1] + ".out", index=False)