import os
import pandas as pd
import datetime as dt

from transformers.BasicDataFrameTransformer import BasicDataFrameTransformer
from models.DfModel import DfModel
from maps.QuantHockeyMap import QuantHockeyMap

class FantasyHockeyController:
    season = str(dt.datetime.now().year - 1) + str(dt.datetime.now().year)
    dataTypes = ["players", "goalies"]
    dataSource = "QuantHockey"
    sheetName = "QuantHockey"
    transformer = BasicDataFrameTransformer
    dataModel = DfModel

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.key = key
            self.value = kwargs[key]
        
        self.dataPath = os.getcwd() + "/data/" + self.season + "/"
        self.resultsPath = os.getcwd() + "/results/" + self.season + "/"

        self.map = self.getMap(self.dataSource)

    def getData(self, dataType):
        dataList = []
        rawDataFiles = os.listdir(self.dataPath + dataType)

        for fileName in rawDataFiles:
            filePath = self.dataPath + dataType + "/" + fileName
            data = self.dataModel(filePath, self.sheetName)

            dataList.append(data)

        return dataList

    def consolidateData(self, dataModelList):

        consolidatedData = self.dataModel()

        for dataModel in dataModelList:
            consolidatedData.append(dataModel)

        return consolidatedData

    def cleanData(self, dataModel):
        return dataModel

    def validateProcess(self):
        
        # Required params are set
        if not self.season or len(self.season) != 8:
            return [False, "No Season Specified."]

        # Required data is present
        playerFiles = os.listdir(self.dataPath + "players/")
        if len(playerFiles) < 1:
            return [False, "No Player Data Available."]

        goalieFiles = os.listdir(self.dataPath + "goalies/")
        if len(goalieFiles) < 1:
            return [False, "No Goalie Data Available."]

        return [True, ""]

    def transformToCsv(self, dataModel):
        return dataModel.transformToCsv()

    def saveCsv(self, csvFile, dataType):
        path = self.resultsPath
        if not os.path.isdir(path):
            os.mkdir(path)
        fileName = dataType + self.season + ".csv"
        f = open(path + fileName, "w")
        f.write(csvFile)
        f.close()

    def transformData(self, data, dataType):
        transformer = self.transformer(dataType, self.map)
        transformedData = transformer.transform(data)
        return transformedData

    def buildCsv(self):

        isValid = self.validateProcess()
        if not isValid[0]:
            return
        else:
            for dataType in self.dataTypes:
                dataList = self.getData(dataType)
                data = self.consolidateData(dataList)
                data = self.cleanData(data)
                data = self.transformData(data, dataType)
                csv = self.transformToCsv(data)
                self.saveCsv(csv, dataType)

    def getMap(self, dataSource):
        if dataSource == "QuantHockey":
            return QuantHockeyMap
        else:
            return {}