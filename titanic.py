import numpy as np
import pandas as pd
import re

data = pd.read_csv("C:/Users/dv.zhilenkov/Downloads/titanic.csv", index_col='PassengerId')

print(data.head())

def sepfun():
    print()
    print("--------------")
    print()

sepfun()

print("t1")
print(data['Sex'].value_counts())

#--------0
sepfun()

print("t2")
print(np.round(data["Survived"].sum() / data["Survived"].count() * 100, decimals=2))

#--------0
sepfun()

print("t3")
print(np.round(data[data.Pclass == 1].Pclass.count() / data["Name"].count() * 100, decimals=2))

#--------0
sepfun()

print("t4")
print(np.round(data["Age"].mean(), 2), data["Age"].median())

#--------0
sepfun()

print("t5")
print("Pearson correlation: ", data[["SibSp", "Parch"]].corr(method='pearson').Parch.values[0])

#--------0
sepfun()

print("t6")
tmp = [i.split() for i in data[data["Sex"] == "female"]["Name"]]
lstlsts = []
for s in tmp:
    s = [x for x in s if '"' not in x]
    lstlsts.append(s)

lstnames = []
for s in lstlsts:
    nm = [x for x in s if '(' in x]
    if len(nm) > 0:
        lstnames += nm
    if 'Miss.' in s:
        if len(s[-1]) > 1:
            lstnames.append(s[-1])
        else:
            lstnames.append(s[-2])


ansnms = []
for s in lstnames:
    s = re.sub('[)()]', '', s)
    ansnms.append(s)

print(ansnms[:20])
#print(data[data["Sex"] == "female"]["Name"][:20])

sepfun()