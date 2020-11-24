# coding: utf-8

import pymysql.cursors
import numpy as np
import time
import sys

from horsedb import horseDb
from model import model

db = horseDb()
rows = db.getTrainDataForGlassShort()
print(len(rows))

x_train = []
y_train = np.array([])
count = 0

summary = db.getRaceTimeSummary()

for row in rows:
    data = db.getResultListForBloodId(row[0], row[2])

    if(len(data) != 5):
        continue

    rep = []
    for d in data:
        ret = list(d)
        if(ret[4] == 1):
            ret[9] = 0
            
        if(ret[4] < 4):
            ret[4] = 1
        else:
            ret[4] = 0
        ret[5] = (ret[5] - float(summary[1]))/summary[0]

        if(ret[9] < 10):
            ret[9] = float(ret[9])/10
        else:
            ret[9] = 1

        ret[1] -= 1
        ret[2] -= 1
        ret[3] = float(ret[3])/100
        ret[6] = float(ret[6])/100
        rep.append(ret)

    x_train.append(rep)
    if(row[7] < 4):
        y_train = np.append(y_train, 1)
    else:
        y_train = np.append(y_train, 0)

    count+=1

print('create training data OK!')
dl = model()
dl.train(np.array(x_train), y_train)

x_test = []
y_test = np.array([])
test_rows = db.getTestResultList()
for row in rows:
    data = db.getResultListForBloodId(row[0], row[2])

    if(len(data) != 5):
        continue

    
    x_test.append(data)
    if(row[7] < 4):
        y_test = np.append(y_test, 1)
    else:
        y_test = np.append(y_test, 0)
    
print('create test data OK!')

score = dl.eval(np.array(x_test), y_test)
print(score)

dl.save('glass_short')
