# coding: utf-8

import numpy as np
from db import horseDb

class Data:
    summary = None

    def __init__(self):
        db = horseDb()
        self.summary = db.getRaceTimeSummary()
    
    def __getDummyRaceData(self):
        return [0]*13

    def __makeDataFromRaceKey(self, raceKey, date):
        # raceKey is (racekey, none) tuple
        db = horseDb()
        results = db.getResultFromRacekey(raceKey)
        count = len(results)

        data = []
        label = []
        # TODO: 過去走情報だけでなく、競走条件も入れる
        # 競走条件に対する過去5走という見方をする方がよさげ？
        for result in results:
            horseData = db.getResultListForBloodId(result[0], date)

            for horse in horseData:
                data.append(self.__engineeringData(horse))

            # 5走以下の場合は、足りないレース分を0埋め
            if(len(horseData) < 5):
                for i in range(len(horseData), 5):
                    data.append(self.__getDummyRaceData())

            if(result[2] > 3):
                label.append(0)
            else:
                label.append(1)

        # 18頭以下の場合は足りない分を0埋め
        if(count < 18):
            for i in range(count, 18):
                label.append(0)
                for j in range(5):
                    data.append(self.__getDummyRaceData())
                
        return data, label

    def __engineeringData(self, data):
        data = list(data)

        data[0] = float(data[0])

        # order_of_arrivalが1ならtop_time_diffは0
        if(data[4] == 1):
            data[9] = 0

        # order_of_arrivalが3以内なら1, それ以外は0
        if(data[4] < 4):
            data[4] = 1
        else:
            data[4] = 0
            # race_time標準化
            data[5] = (data[5] - float(self.summary[1]))/self.summary[0]

        # top_time_diff
        data[9] = float(data[9])/100

        # race_type
        data[1] -= 1
        # left_right
        data[2] -= 1
        # corse_condition
        data[3] = float(data[3])/100
        # idm
        data[6] = float(data[6])/100
        # place_code TODO:標準化かEmbedding
        data[10] = float(data[10])/10
        # first_time
        data[11] = (data[11] - float(self.summary[3]))/self.summary[2]
        # last_time
        data[12] = (data[12] - float(self.summary[5]))/self.summary[4]

        return data

    def __getGlassShortRaceKeys(self, date, minDate):
        db = horseDb()
        raceKeys = db.getRaceKeys(date, 1, maxDistance=1600, minDate=minDate)
        return raceKeys

    def __getGlassMiddleRaceKeys(self, date, minDate):
        db = horseDb()
        raceKeys = db.getRaceKeys(date, 1, minDistance=1800, maxDistance=2400, minDate=minDate)
        return raceKeys

    def __getGlassLongRaceKeys(self, date, minDate):
        db = horseDb()
        raceKeys = db.getRaceKeys(date, 1, minDistance=2400, minDate=minDate)
        return raceKeys

    def __getDirtShortRaceKeys(self, date, minDate):
        db = horseDb()
        raceKeys = db.getRaceKeys(date, 2, maxDistance=1600, minDate=minDate)
        return raceKeys

    def __getDirtMiddleRaceKeys(self, date, minDate):
        db = horseDb()
        raceKeys = db.getRaceKeys(date, 2, minDistance=1800, minDate=minDate)
        return raceKeys

    def getRaceDataFromRaceKey(self, racekey, date):
        db = horseDb()
        data, label = self.__makeDataFromRaceKey(racekey, date)
        return data, label
    
    def getGlassShortTrainData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-01-01', '2015-01-01')

        retData = []
        retLabel = []
        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            retData.append(data)
            retLabel.append(label)

        return retData, retLabel

    def getGlassShortTestData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-09-01', '2020-01-01')

        retData = []
        retLabel = []
        print("create test data.")
        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            retData.append(data)
            retLabel.append(label)

        print("finish test data.")
        return retData, retLabel
        
    def getDirtShortTrainData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-01-01', '2014-01-01')
        retData = []
        retLabel = []

        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            data = np.array(data)
            data = np.reshape(data, 900)
            label = np.array(label)

        return retData, retLabel

    def getDirtShortTestData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-09-01', '2020-01-01')

        retData = []
        retLabel = []
        print("create test data.")
        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            retData.append(data)
            retLabel.append(label)

        print("finish test data.")
        return retData, retLabel
        
    def getGlassMiddleTrainData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-01-01', '2015-01-01')

        retData = []
        retLabel = []
        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            retData.append(data)
            retLabel.append(label)

        return retData, retLabel

    def getGlassMiddleTestData(self):
        raceKeys = self.__getGlassShortRaceKeys('2020-09-01', '2020-01-01')

        retData = []
        retLabel = []
        print("create test data.")
        for key in raceKeys:
            data, label = self.__makeDataFromRaceKey(key[0], key[1])
            retData.append(data)
            retLabel.append(label)

        print("finish test data.")
        return retData, retLabel
    
