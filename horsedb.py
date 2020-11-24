# coding: utf-8

import pymysql.cursors

class horseDb:
    host = 'localhost'
    user = 'horse'
    password = '1q2w3e4r'
    database = 'horse'
    charset = 'utf8mb4'

    conn = None

    def __init__(self):
        self.conn = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            charset = self.charset
        )

    def getTrainDataForGlassShort(self):
        sql = "\
select blood_number, horse_name, date, distance, race_type, left_right, \
corse_condition, order_of_arrival, race_time, idm, drawback, race_pace, \
horse_pace \
from result \
where date < '2020-01-01' \
and date > '2015-01-01' \
and race_type != 1 \
and distance >= 1000 and distance <= 1600 \
order by date desc \
"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def getResultList(self):
        cur = self.conn.cursor()
        sql = "\
select blood_number, horse_name, date, distance, race_type, left_right, \
corse_condition, order_of_arrival, race_time, idm, drawback, race_pace, \
horse_pace \
from result \
where date < '2020-01-01' \
and date > '2019-01-01' \
and race_type != 3 \
order by date desc \
limit 10000 \
"
        cur.execute(sql)
        return cur.fetchall()

    def getTestResultList(self):
        cur = self.conn.cursor()
        sql = "\
select blood_number, horse_name, date, distance, race_type, left_right, \
corse_condition, order_of_arrival, race_time, idm, drawback, race_pace, \
horse_pace \
from result \
where date > '2020-01-01' \
and race_type != 3 \
order by date desc \
limit 10 \
"
        cur.execute(sql)
        return cur.fetchall()

    def getResultListForBloodId(self, id, date):
        sql = "\
select \
(distance - 1000)/2600 as dist, \
race_type, left_right, corse_condition, order_of_arrival, \
race_time, idm, drawback, start_late, top_time_diff \
from result \
join race on result.race_key = race.race_key \
where blood_number = '" + str(id) + "' \
and race.date < '" + date.strftime('%Y-%m-%d') + "' \
and race_type != 3 \
order by date desc \
limit 5"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def getRaceTimeSummary(self):
        sql = "\
select stddev(race_time) as std, avg(race_time) as avg \
from result"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def getRaceKeys(self, date, raceType, distance, minDate = None, limit=None):
        sql = "\
select race_key, date from race \
where date < '" + date + "'"
        if(minDate != None):
            sql += " and date > '" + minDate + "'"

        sql += " \
and race_type = " + str(raceType) + " \
and distance <= " + str(distance) + " \
order by date desc, race_count asc \
"
        if(limit != None):
            sql += "limit " + str(limit)

        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def getResultFromRacekey(self, race_key):
        sql = "\
select blood_number, horse_name, order_of_arrival, date from result \
join race on result.race_key = race.race_key \
where result.race_key = '" + race_key + "' \
order by horse_number"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
