import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn import metrics


df=pd.read_csv('fda2.csv')
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)
df2=df.drop(['primaryid','caseid','drug_seq'], axis=1)
df3=df2.dropna()
df3=MultiColumnLabelEncoder(columns = ['indi_pt','drugname','reporter_country','pt']).fit_transform(df3)
df3['output']=0.0
df3.loc[df3['de']==1, 'output']=1
df3.loc[df3['lt']==1, 'output']=2
df3.loc[df3['ho']==1, 'output']=3
df3.loc[df3['ds']==1, 'output']=4
df3.loc[df3['ca']==1, 'output']=5
df3.loc[df3['ri']==1, 'output']=6
df3.loc[df3['ot']==1, 'output']=7
df4=df3.sample(1000000)
y=df4['output']
X=df4.drop(['output','de','lt','ho','ds','ca','ri','ot'], axis=1)
# Create support vector classifier
svc = svm.SVC(kernel='linear', class_weight='balanced', C=1.0, random_state=0)

clf = OneVsRestClassifier(SVC(kernel='linear', probability=True, class_weight='balanced'), n_jobs=-1)
clf.fit(X, y)

svc.fit(X_train, y_train)
print metrics.accuracy_score(y_test, svc.predict(X_test))
print metrics.confusion_matrix(y_test, svc.predict(X_test))