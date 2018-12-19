# Importing pandas
import pandas as pd
import json
import time
import warnings
import sys

def get_values(dict, columns):
    result = ""
    for col in columns:
        try:
            result = result + ",\"" + str(dict[col]).strip() +"\""
        except KeyError:
            result = result + ",\"\""
    return str(result)


warnings.filterwarnings('ignore')


df=pd.read_csv(sys.argv[1])
df['pt']=df['pt'].fillna('')
df['age']=df['age'].fillna('')
df['wt']=df['wt'].fillna('')
df['gndr_cod']=df['gndr_cod'].fillna('')
df['reporter_country']=df['reporter_country'].fillna('')

#df=pd.concat([df[col].fillna('') for col in df.columns], axis=1)
with open("dict.txt", 'r') as f:
    z= f.read().decode("utf-8")
dictionary = json.loads(z)
start = time.time()
#dc = df.set_index('caseid').to_dict('index')
j = 0
headers = [str(i) for i in df.columns]
with open(sys.argv[1] + '.csv', 'w') as f:
    for index, row in df.iterrows():
		if str(row['caseid'])!='nan':
			k =  str(row['caseid'])
			cid = str(k)
			row['age'] = dictionary[cid]['age']
			row['wt'] = dictionary[cid]['wt']
			row['gndr_cod'] = str(dictionary[cid]['gndr_cod'])
			row['reporter_country'] = str(dictionary[cid]['reporter_country'])
		pt = row['pt'].split(",")
		k =  str(row['caseid'])
		if type(pt) == list and len(pt) > 0:
			row['pt'] = ''
			for el in pt:
				f.write(str(k) + get_values(row,headers) +"," + el + "\n")
		else:
			f.write(str(k) + get_values(row,headers) + ",\n")
		if j % 100000 == 0:
			now = time.time()
			print j
			print now-start
		j=j+1

#df.to_csv(sys.argv[1] + '.csv',index=False)
		
#df2 = pd.DataFrame(dc)
#df2 = df2.transpose()
#df2['caseid'] = df2.index
#df2.reset_index(drop=True).head()
#df2.to_csv(sys.argv[1] + '.csv',index=False)

