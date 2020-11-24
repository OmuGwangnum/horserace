# coding: utf-8

from horsedb import horseDb

class MakeData:

    db = None

    def __init__(self):
        self.db = horseDb()

    def getGlassShortTrainData(self):
        
