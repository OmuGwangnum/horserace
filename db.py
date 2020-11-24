# coding: utf-8

import mysql.connector
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.utils import np_utils

conn = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'horse',
    password = '1q2w3e4r',
    database = 'horse',
    charset = 'utf8mb4'
);

cur = conn.cursor(buffered=True)

sql = "\
select blood_number, horse_name, date, distance, race_type, left_right, corse_condition, \
order_of_arrival, race_time, idm, drawback, race_pace, horse_pace \
from result \
where date > '2019-01-01' \
and date < '2020-01-01' \
order by id asc \
"
cur.execute(sql)

rows = cur.fetchall()
length = len(rows)

x_train = []
y_train = []

count = 0
for row in rows:
    dataSql = "\
select distance, race_type, left_right, corse_condition, order_of_arrival, \
race_time, idm, drawback, start_late, top_time_diff, race_pace, horse_pace \
from result \
where blood_number = '" + str(row[0]) + "' order by date desc \
limit 5"
    if(row[7] <= 3):
        y_train.append(1)
    else:
        y_train.append(0)
        
    cur.execute(dataSql)
    datas = cur.fetchall()
    list = []
    for data in datas:
        list.append(data)
    x_train.append(list)

    count += 1
    print(count)
    
x_train = np.array(x_train)
y_train = np.array(y_train)

sql = "\
select blood_number, horse_name, date, distance, race_type, left_right, corse_condition, \
order_of_arrival, race_time, idm, drawback, race_pace, horse_pace \
from result \
where date > '2020-01-01' \
order by id asc \
"
cur.execute(sql)

x_test = []
y_test = []

rows = cur.fetchall()
for row in rows:
    dataSql = "\
select distance, race_type, left_right, corse_condition, order_of_arrival, \
race_time, idm, drawback, start_late, top_time_diff, race_pace, horse_pace \
from result \
where blood_number = '" + str(row[0]) + "' order by date desc \
limit 5"
    if(row[7] <= 3):
        y_test.append(1)
    else:
        y_test.append(0)

    cur.execute(dataSql)
    datas = cur.fetchall()
    list = []
    for data in datas:
        list.append(data)
    x_test.append(list)

x_test = np.array(x_test)
y_test = np.array(y_test)
    
cur.close()
conn.close()

model = Sequential([
    Dense(30, input_shape=(60)),
    Activation('sigmoid'),
    Dense(2),
    Activation('softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=200, verbose=1, epochs=20, validation_split=0.1)

score = model.evaluate(x_test, y_test, verbose=1)
print('accuracy:', score[1])
